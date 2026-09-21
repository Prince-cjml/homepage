# Deploy the static homepage to Cloudflare Pages

The committed `site/` directory is the ready-to-deploy website. It contains HTML,
CSS, images, Cloudflare redirects/headers, and a real 404 page. No .NET runtime,
SQLite database, secrets, or server configuration is needed on Cloudflare.

## Connect the GitHub repository

In Cloudflare, open **Workers & Pages**, create a **Pages** project, and select
**Import an existing Git repository** (wording may vary). Choose
`Prince-cjml/homepage` and configure:

| Setting | Value |
| --- | --- |
| Production branch | `main` |
| Framework preset | None |
| Build command | `exit 0` |
| Build output directory | `site` |
| Root directory | Leave blank (repository root) |
| Environment variables | None |

Deploy, then add your domain under the project's **Custom domains** tab if desired.
Use Pages, not the Worker deployment flow that asks for a Wrangler deploy command.
Only the contents of `site/` are publicly served. Subsequent pushes to `main`
redeploy the committed snapshot automatically. The repository itself retains the
editable .NET source and template license.

Alternatively, upload `artifacts/homepage-static.zip` via a Pages Direct Upload
project. Git integration is preferable for future updates.

## Refresh the static export after editing

The dev host still renders the .NET source, but Cloudflare renders the committed
snapshot. Edits are not published until you export and push again:

```bash
# From the repository root; requires Python 3 with Pillow and the .NET 8 SDK.
./scripts/dotnet.sh restore AcademicPageDotNet.sln --locked-mode
python3 scripts/export-static.py
python3 -m http.server 8090 --directory site
```

Preview `http://localhost:8090/` and `/research/`. Stop only this optional preview
server when finished. The exporter creates and stops its own temporary server;
it does not touch your running development host.

Review, commit, and push your edited source files together with `site/`:

```bash
git add AcademicPageDotNet site docs scripts README.md
git commit -m "Update homepage content and static export"
git push origin main
```

The exporter uses the current Razor pages, copies their referenced local assets,
and optimizes the exported portrait/favicon using Pillow. It never modifies the
source images. New CSS-referenced resources (for example custom fonts or CSS
background images) must also be included in the exporter before deployment.
External links and externally hosted images stay external.

Routes: `/` is Home, `/research/` is Research. `_redirects` preserves the old
`/Research` and `/Index` URLs on Cloudflare. Plain Python's preview server does
not interpret Cloudflare's `_redirects` or `_headers` files.
