# Academic homepage

ASP.NET Core Razor Pages homepage based on [Yuyang Li's AcademicPageDotNet](https://github.com/YuyangLee/AcademicPageDotNet), template commit `4c8ab438c115d9fefa70639fbe4b92e58c5c7084`. The original Beer-Ware license is retained in `LICENSE`. The website still contains the template's example identity and publications.

## Local development

Requires a .NET 8 SDK (selected by `global.json`). Bootstrap and jQuery are included in `wwwroot/lib`; Node.js/npm and a separate database server are unnecessary. SQLite runs in-process.

```bash
./scripts/dotnet.sh restore AcademicPageDotNet.sln --locked-mode
./scripts/dotnet.sh build AcademicPageDotNet.sln -c Release --no-restore
./scripts/dotnet.sh run --project AcademicPageDotNet --no-launch-profile --urls http://127.0.0.1:5080
```

Open http://127.0.0.1:5080 and http://127.0.0.1:5080/Research. The wrapper keeps SDK state and NuGet packages in ignored local folders. Stop with Ctrl+C.

## Content

- `AcademicPageDotNet/appsettings.json`: name, affiliation, contact details, links, avatar, title.
- `AcademicPageDotNet/Data/Bio.md` and `News.md`: biography and news.
- `AcademicPageDotNet/Data/pubs.json`: publications.
- `AcademicPageDotNet/Data/Authors.db`: author metadata in SQLite.
- `AcademicPageDotNet/Pages` and `wwwroot`: page templates, CSS, JavaScript and assets.

The local original checkout is preserved in `.template-source/`, which is ignored and is not required by the application. The main repository contains its own editable copy of the source. Dependency versions are recorded in `packages.lock.json`; regenerate the lock file intentionally when updating packages.

## Publishing later to Tencent Cloud

```bash
./scripts/dotnet.sh publish AcademicPageDotNet/AcademicPageDotNet.csproj -c Release -o artifacts/publish
cd artifacts/publish
dotnet AcademicPageDotNet.dll --urls http://127.0.0.1:5080
```

Run from the published directory because the template uses relative data paths. Publishing includes the Markdown, publication JSON, and SQLite database. The service account needs write access to the SQLite data directory. Preserve the live database when deploying subsequent releases.

A Linux Tencent Cloud VM can host this behind Nginx with HTTPS and a systemd service, using a compatible ASP.NET Core runtime. Server configuration, domain, and TLS are deferred until deployment; no server has been contacted. .NET 8 support ends November 10, 2026, so upgrade to a supported LTS before a deployment beyond that date. The template also references external image/font services; their availability is separate from the local build.
