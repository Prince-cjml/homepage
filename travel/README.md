# Xiyao Tian's Travel Map

Source for https://xiyaotian.tech/travel/, integrated into the academic homepage.
The public site is read-only. Visited places come from Xiyao’s supplied list;
no trip dates or photographs are invented. The page is accessible directly at
`/travel/` but is not linked from the academic homepage navigation.

## Edit trips and photos locally

Requires Node.js 20.19+ (tested with Node 24).

```bash
cd travel
npm ci
npm run dev
```

Open the loopback URL printed by Vite (normally http://127.0.0.1:5173).
Choose places on the globe or flat map, light them up, and add trips and photos.
Changes save to `travel/data/` automatically. That folder is Git-ignored; back it
up separately. The editor binds to localhost and is never deployed to Cloudflare.
The title is configured in `scripts/site-config.js`; an optional local
`data/site.json` can override it. `TRAVEL_DATA_DIR` can select another data folder.

## Publish

From the **homepage repository root**:

```bash
python3 scripts/export-static.py
git diff --stat
git add travel site AcademicPageDotNet/Pages/Shared/_Layout.cshtml scripts/export-static.py
git commit -m "Update travel map"
git push origin main
```

The exporter builds `travel/site/` and copies it into the committed `site/travel/`.
Cloudflare Pages continues to deploy the root `site` directory with `exit 0` as
its build command. `/travel` redirects to `/travel/`; bundles, map geometry,
travel data and photos all use the `/travel/` prefix.

Only reviewed trips, notes, thumbnail and display images are published. Original
photos, original filenames, upload timestamps, settings and the editor API are
not included in the public snapshot. There is no analytics service or account
connection. Photo display copies are re-encoded by the local editor without EXIF.
Public snapshots are committed in Git history: deleting a published photo later
does not erase historical commits. Review your data before pushing.

On another computer, restore your backed-up `data/` folder before publishing new
travel changes. The exporter refuses to replace a nonempty public map when the
local editor data is missing. `npm run build:site` only builds the travel app;
it does not update the homepage's deployable `site/travel/` by itself.

## Upstream and license

Adapted from the travel-map project at commit
`8e65f4ff6819b096c7577ebd9f58c5369fcfb250`.
The upstream source contained no creator profile, trips, photos or credentials.
No upstream Git history, deployment scripts or account configuration were imported.
The MIT notice is preserved in `LICENSE`; map geometry is Natural Earth public-domain data.
