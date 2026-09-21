#!/usr/bin/env python3
"""Publish Razor pages, then export a standalone Cloudflare Pages site.
Requires .NET 8, Python 3, and Pillow. Never touches an existing dev host.
"""
import hashlib
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import tempfile
import time
from urllib.parse import urlsplit, unquote
from urllib.request import build_opener, ProxyHandler
from html.parser import HTMLParser
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'site'

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src'):
            if key in attrs:
                self.urls.append(attrs[key])

with tempfile.TemporaryDirectory(prefix='homepage-export-') as temporary:
    work = Path(temporary)
    published = work / 'published'
    subprocess.run([str(ROOT / 'scripts/dotnet.sh'), 'publish',
                    'AcademicPageDotNet/AcademicPageDotNet.csproj', '-c', 'Release',
                    '--no-restore', '-o', str(published)], cwd=ROOT, check=True)
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    base = f'http://127.0.0.1:{port}'
    opener = build_opener(ProxyHandler({}))
    env = dict(os.environ, ASPNETCORE_ENVIRONMENT='Production',
               DOTNET_CLI_HOME=str(ROOT / '.dotnet-home'))
    with (work / 'server.log').open('w+') as log:
        server = subprocess.Popen(['dotnet', 'AcademicPageDotNet.dll', '--urls', base],
                                  cwd=published, env=env, stdout=log, stderr=log)
        try:
            for attempt in range(100):
                try:
                    opener.open(base, timeout=1).close()
                    break
                except OSError:
                    if server.poll() is not None:
                        raise RuntimeError('Export server exited; inspect the build output.')
                    time.sleep(.1)
            else:
                raise RuntimeError('Export server did not start.')
            pages = {}
            for route, destination in [('/', 'index.html'), ('/Research', 'research/index.html')]:
                with opener.open(base + route, timeout=15) as response:
                    html = response.read().decode()
                if 'Failed to load' in html:
                    raise RuntimeError(f'Missing content on {route}')
                html = re.sub(r'href="/(?:Index)?"', 'href="/"', html)
                html = html.replace('href="/Research"', 'href="/research/"')
                if 'aspnetcore-browser-refresh' in html or 'browserLink' in html:
                    raise RuntimeError('Development script found in export')
                pages[destination] = '\n'.join(line.rstrip() for line in html.splitlines()) + '\n'
        finally:
            server.terminate()
            server.wait(timeout=15)

    staging = work / 'site'
    staging.mkdir()
    # Copy only resources actually used by these pages, never Data/config/database.
    for html in pages.values():
        refs = References()
        refs.feed(html)
        for url in refs.urls:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path or parts.path in ('/', '/research/'):
                continue
            relative = unquote(parts.path).lstrip('/')
            source = (published / 'wwwroot' / relative).resolve()
            if not source.is_relative_to((published / 'wwwroot').resolve()) or not source.is_file():
                raise RuntimeError(f'Unresolved local resource: {url}')
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

    # Resize just the exported profile assets; retain original editing files.
    for name, size in [('tianxiyao.jpg', 840), ('logo.png', 128)]:
        path = staging / 'images' / name
        if path.exists():
            with Image.open(path) as source:
                image = ImageOps.exif_transpose(source)
                image.thumbnail((size, size), Image.Resampling.LANCZOS)
                if name.endswith('.jpg'):
                    image.convert('RGB').save(path, quality=88, optimize=True)
                else:
                    image.save(path, optimize=True)

    def versioned(match):
        url = match.group(2)
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or not parts.path.startswith('/'):
            return match.group(0)
        asset = staging / unquote(parts.path).lstrip('/')
        if not asset.is_file():
            return match.group(0)
        digest = hashlib.sha256(asset.read_bytes()).hexdigest()[:16]
        return f'{match.group(1)}="{parts.path}?v={digest}"'

    for destination, html in pages.items():
        target = staging / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(re.sub(r'(href|src)="([^"]+)"', versioned, html))

    (staging / '404.html').write_text('''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found</title><link rel="stylesheet" href="/css/site.css"></head>
<body><main class="shell page-heading"><h1>Page not found.</h1>
<p>The page may have moved. <a href="/">Return home</a>.</p></main></body></html>
''')
    (staging / '_redirects').write_text('/Index / 301\n/Research /research/ 301\n/Research/ /research/ 301\n')
    (staging / '_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Cache-Control: public, max-age=0, must-revalidate\n')
    (staging / 'robots.txt').write_text(
        'User-agent: *\n'
        'Allow: /\n'
        '\n'
        'Sitemap: https://xiyaotian.tech/sitemap.xml\n'
    )
    (staging / 'sitemap.xml').write_text('''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://xiyaotian.tech/</loc>
  </url>
  <url>
    <loc>https://xiyaotian.tech/research/</loc>
  </url>
</urlset>
''')
    for path in staging.rglob('*'):
        if path.is_file() and path.stat().st_size >= 25 * 1024 * 1024:
            raise RuntimeError(f'Asset exceeds Cloudflare Pages 25 MiB limit: {path}')
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(staging, OUTPUT)
    print(f'Exported {len(pages)} pages to {OUTPUT}')
