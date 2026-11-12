# JagX Pulse — The world, in one pulse.

**A JagX & JRILICENSE newsroom.** Fast, factual, calm coverage of world news, Africa, Nigeria, business & markets, technology, sports, entertainment, health and science.

This repository is a **static site** — plain HTML, CSS and JavaScript. There is no server, no build step and no dependencies. Push it to GitHub, import it on Vercel, and it is live.

---

## What's in here

```
.
├── index.html          # The whole app: front page, category filters, search, article pages
├── styles.css          # Design system — near-black #0a0a0a base, gold #c4a574 accent
├── sw.js               # Service worker — offline reading + install
├── manifest.json       # PWA manifest — home-screen install on Android / iOS / desktop
├── vercel.json         # Vercel config — static build, image rewrites, caching + security headers
├── data/
│   └── stories.json    # The edition's stories — the single source of truth
├── images/             # One real image per story
└── icons/              # JagX crest app icons (SVG, any + maskable)
```

## Features

- **Hero lead story** with the newest headline, its summary, source and both dates.
- **Category filters** — World, Africa, Nigeria, Business, Tech, Sports, Entertainment, Health, Science.
- **Search** across every headline, summary and article body in the edition.
- **Latest rail** — newest first, horizontally scrollable.
- **Most read rail** — ranked by read count.
- **Article pages** — full body, image with caption, source, publication date, date added, and related stories.
- **Every card shows** a real image, the source, the publication date **and** the date it was added, so a reader can always tell how old a story is.
- **Installable PWA** — add to home screen on Android, iOS or desktop; the edition reads offline once loaded.
- **Advertise / Contact block** on every page → **jrilicense@gmail.com** and JagX WhatsApp **+234 916 065 4415**.
- **Responsive** — mobile-first, works on phone, tablet and desktop.

## Dates

Every story carries two timestamps:

| Field | Meaning |
|---|---|
| `published` | When the source published the story |
| `added` | When it was added to JagX Pulse |

Older stories are labelled with their age ("3 days ago") and are **never deleted** — readers can go back and read an earlier edition and see exactly when it ran.

## Images

Story photos live in `images/` as WebP. `vercel.json` also rewrites each `/images/*.webp` path to the original source photo, so a photo still resolves if a file is ever missing from the repo. To bundle a photo locally instead, drop the file into `images/` and delete its rewrite entry.

## Running locally

No build step. Serve the folder over HTTP (the service worker needs `http://` or `https://`, not `file://`):

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploying to Vercel

1. Push this repository to GitHub.
2. Go to [vercel.com/new](https://vercel.com/new) and **Import** the repository.
3. Framework preset: **Other**. Build command: **leave empty**. Output directory: **leave empty** (the site is at the repo root).
4. Click **Deploy**. Vercel serves the static files and applies `vercel.json`.

Every later `git push` to the default branch redeploys automatically.

## Refreshing the edition

1. Gather the new stories and cross-check each against at least two credible sources.
2. Add them to `data/stories.json`.
3. Update `lastUpdated` and `edition` in `data/stories.json`.
4. Bump `CACHE_VERSION` in `sw.js` so installed apps pick up the new edition.
5. Keep every older story in place, with its original dates.

## Editorial rules

- Never fabricate a headline, date, source or image.
- Cross-check each story against at least two credible outlets before publishing.
- If a fact cannot be verified, say so in the article text or omit it.
- No clickbait, no sensationalism, no invented quotes.

## Licence

Code and design © JagX Pulse. **Powered by JagX. Licensed by JRILICENSE.**

Advertising, syndication and support: **jrilicense@gmail.com**
