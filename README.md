# JagX Pulse

**The world, in one pulse.** — a JagX & JRILICENSE newsroom.

A static, installable news site. No build step, no server, no dependencies: the files in this
repository are the site. Deploy it anywhere that serves static files.

---

## What it is

JagX Pulse carries world, Africa, Nigeria, business, technology, sport, entertainment, health and
science reporting. Every story card shows a real photo, the source, the publication date **and**
the date it was added to the site, so a reader always knows how old a story is. Older editions stay
online with their original dates — nothing is deleted.

- **Front page** — hero lead story, category filters, search, a *Latest* rail and a *Most read* rail.
- **Article pages** — full headline, the summary of what the story is about, the photo, the source
  link, publication date, date added, and related stories from the same section.
- **Installable PWA** — `manifest.json` + `sw.js`. Installs to the home screen on Android, iOS and
  desktop, and reads the cached edition offline.
- **Mobile-first** — 3 columns on desktop, 2 on tablet, 1 on phone.

## Files

| File | Purpose |
|---|---|
| `index.html` | The shell: masthead, rails, feed, article view, advertise block, footer |
| `styles.css` | Near-black `#0a0a0a` + gold `#c4a574`, Fraunces + Figtree |
| `app.js` | Loads the edition, renders sections/search/rails, hash routing, PWA install |
| `data/stories.json` | **The edition** — the single source of truth for every story |
| `sw.js` | Service worker: offline reading, cache versioning |
| `manifest.json` | PWA manifest |
| `icons/` | JagX crest (SVG) and app icons (PNG) |
| `images/` | Story photos (WebP) |
| `images/ig/` | JPEG derivatives of every photo — Instagram only accepts JPEG |
| `scripts/social.py` | Social pipeline: WebP→JPEG, caption composer, posted-ledger |
| `vercel.json` | Vercel config: clean URLs, cache + security headers. No build, no rewrites |

## The edition file

`data/stories.json` drives everything. Each story carries:

```json
{
  "slug": "unique-url-slug",
  "title": "Headline",
  "summary": "Two to three sentences on what the story is about.",
  "section": "world",
  "sectionLabel": "World",
  "source": "BBC News",
  "url": "https://…",
  "published": "2026-11-12T05:59:18+01:00",
  "added": "2026-11-12T13:20:00+01:00",
  "image": "images/slug.webp"
}
```

`published` is when the source published it. `added` is when it entered this edition. Both are
shown on every card and article page.

## Refresh schedule

**Twenty-eight refreshes a day, every hour on the hour** (`0 * * * *`, WAT) — roughly 12 new
stories per refresh, about 330 a day, building the archive toward **500 stories**. Each refresh:

1. gathers new stories from the sources and cross-checks each across at least two,
2. **appends** them to `data/stories.json` (older stories keep their original dates and stay visible),
3. updates the `updated` / `updatedLabel` fields and the edition number,
4. bumps `VERSION` in `sw.js` so installed apps pick up the new edition,
5. converts each new photo to JPEG for Instagram (`scripts/social.py convert --new`),
6. posts every new story to **X** and **Instagram**,
7. records the returned post ids in `data/stories.json` so nothing is ever posted twice,
8. pushes to this repository, which redeploys Vercel automatically.

## Social publishing

Every story that goes on the site also goes out on the connected accounts:

| Account | Handle | What it posts |
|---|---|---|
| X (Twitter) | [@jagxjrilicense](https://x.com/jagxjrilicense) | Headline, one-sentence summary, section, source link — under 280 weighted characters |
| Instagram | [@jagxpulse](https://www.instagram.com/jagxpulse/) | The story photo as a feed image, with headline, summary, source credit and site link |

`scripts/social.py` does the deterministic work so nothing is guessed:

```bash
python3 scripts/social.py convert --new    # WebP -> JPEG for new stories
python3 scripts/social.py captions --new   # ready-to-post captions + public image URLs
python3 scripts/social.py mark --slug S --x ID --ig ID   # record post ids
python3 scripts/social.py status           # edition, posted counts, distance to 500
```

**Why JPEG derivatives exist:** Instagram's Graph API only accepts JPEG, and it must fetch the
image from a **public** URL. The `/sites/` artifact URLs are token-gated (403 to an anonymous
fetcher), so the JPEGs are committed to this public repo and served by Vercel at
`https://jagx-pulse.vercel.app/images/ig/<slug>.jpg`. That is the URL Meta fetches.

**Double-posting is prevented by the ledger**, not by memory: a story with a `tweetId` is skipped
on X, and one with an `igMediaId` is skipped on Instagram.

### Instagram limits

Instagram allows **100 API-published posts per rolling 24 hours** per account. At 28 refreshes a
run posting every story would exceed that, so the runbook caps Instagram at **3 posts per refresh**
(84/day), choosing the lead story plus the strongest sports and Nigeria stories. X has no such
practical cap at this volume.

## Deploying on Vercel

1. **vercel.com/new** → Import this repository.
2. Framework preset: **Other**. Leave **Build command** and **Output directory** empty — the site is
   at the repository root.
3. **Deploy**.

Every later push to `main` redeploys automatically.

## Contact

Advertising, sponsorship and brand partnerships: **jrilicense@gmail.com** · WhatsApp **+234 916 065 4415**

---

Powered by **JagX** · Licensed by **JRILICENSE**
