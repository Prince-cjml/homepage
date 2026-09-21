# Editing your homepage

All paths below are relative to the repository root. Edit `AcademicPageDotNet/`, not the archived `.template-source/` checkout. The site currently mixes your profile settings with the collaborator's sample biography, news, publications, and portrait; replace those sample files before sharing it.

## Name, affiliation, email and profile links

Edit `AcademicPageDotNet/appsettings.json`:

- `WebsiteTitle`: browser title and name in the navigation.
- `Personal.Name`: main heading and footer name.
- `Personal.Institute`: affiliation below the main heading. `Personal.Role` is retained in settings but not displayed.
- `Personal.Email`: Email link.
- `Personal.AvatarUrl`: portrait URL. For a local image, put `portrait.jpg` in `AcademicPageDotNet/wwwroot/images/` (create the folder) and set this to `/images/portrait.jpg`. An empty string hides the portrait.
- `Personal.Links`: CV, GitHub, GoogleScholar, ORCID, LinkedIn, etc. Empty values are hidden. Additional keys automatically appear as text links.
- `Personal.Phone`: retained in the settings but not displayed by the current design.

For a local CV, put `cv.pdf` in `AcademicPageDotNet/wwwroot/files/` and set `Personal.Links.CV` to `/files/cv.pdf`.

Keep JSON valid: double quotes around keys/strings, commas between entries, and no trailing comma. Restart the site after editing configuration if changes do not appear.

## Biography

Edit `AcademicPageDotNet/Data/Bio.md`. Use ordinary Markdown with short paragraphs:

```markdown
I am an undergraduate student at [Peking University](https://www.pku.edu.cn/).

My interests include **your research areas**. I work on ...
```

Only write your actual affiliations and research claims. Markdown links, emphasis and lists work; embedded HTML is rendered directly, so use content you trust.

## News

Edit `AcademicPageDotNet/Data/News.md`. Each top-level list item becomes a row. Put the newest item first; dates are written manually:

```markdown
- **September 2026** — Started a new research project on ...
- **June 2026** — Presented our work at ...
```

## Acknowledgement

Edit `AcademicPageDotNet/Data/Acknowledgement.md` using Markdown. It appears in its own block directly below News. Save and refresh to update the text.

## Publications and preprints

Edit `AcademicPageDotNet/Data/pubs.json`. It is an array of publication objects; `[]` shows a clean empty state. Entries retain file order within each section. Example (replace all placeholders):

```json
[
  {
    "Title": "Your paper title",
    "Authors": {
      "Xiyao Tian": 5,
      "Coauthor Name": 2
    },
    "PublishDate": "2026-09-01",
    "PublicationName": "Conference or Journal, 2026",
    "State": "Accepted",
    "Links": {
      "Paper": "https://example.org/paper",
      "Code": "https://github.com/your-account/your-project"
    },
    "Introduction": "A short explanation of the problem and contribution.",
    "TeaserUrl": "/images/paper-teaser.jpg",
    "Highlight": true,
    "Preprint": false
  }
]
```

- `Preprint`: explicitly set `true` for the Preprints section or `false` for Publications. Omitting it excludes the entry under the template's existing loader.
- `Highlight`: adds a restrained “Selected” label.
- `TeaserUrl`: local `/images/...` path or remote URL; use `""` for a text-only entry. Publication images are contained without cropping; portraits are cropped to fit.
- `Links`: any nonempty resource URLs appear as keyboard-accessible links. Add PDF, Project, Slides, etc. as needed.
- `PublicationName`: venue and year shown above the title. Preprints show “Preprint” instead.
- `PublishDate` and `State`: stored by the template, but currently neither displayed nor used for sorting.
- Author numbers are flags: `0` ordinary author, `1` equal contribution, `2` corresponding author, `4` website owner (bold). Add flags to combine them: `5` = website owner + equal contribution, `6` = website owner + corresponding author.

Authors do **not** need database entries to appear. Names absent from the database render as plain text. Optional author website links are read from the `authors` table in `AcademicPageDotNet/Data/Authors.db`; edit `Name`, `Url` and `Description` using a SQLite editor such as DB Browser for SQLite. Match `Name` exactly to the publication JSON. Back up the database before editing. The website owner's name is bold rather than linked.

Markdown and publication JSON are read on requests; refresh the page after saving.

## Design and page structure

- `AcademicPageDotNet/wwwroot/css/site.css`: all active styles. Edit the variables at the top for colors; media queries control tablet/mobile layout.
- `AcademicPageDotNet/Pages/Index.cshtml`: profile and news layout.
- `AcademicPageDotNet/Pages/Research.cshtml`: publication layout.
- `AcademicPageDotNet/Pages/Shared/_Layout.cshtml`: shared navigation, page title and footer.

The redesigned pages use local CSS and system fonts. Legacy Bootstrap/theme files remain in the template assets but are not loaded by the layout. External portraits and publication images still need their respective hosts to be available.

For automatic rebuilds while editing Razor or CSS:

```bash
./scripts/dotnet.sh watch --project AcademicPageDotNet run --no-launch-profile --urls http://127.0.0.1:5080
```

Alternatively stop and rerun the normal development command in `README.md` after editing Razor files. Published deployments use a copy of the content, so republish/redeploy your edits when updating the server.

## Current portrait and favicon

Edit `AcademicPageDotNet/wwwroot/images/tianxiyao.jpg` for the live portrait and `AcademicPageDotNet/wwwroot/images/logo.png` for the browser icon. Files in `Data/` are separate originals, not the served images. Save and refresh. Both image URLs include a content version to avoid stale browser caching.
