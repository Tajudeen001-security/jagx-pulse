# JagX Pulse API + X Sync

A companion app to the JagX Pulse news site. It gives developers a **free, no-signup API key** for
the JagX Pulse edition, and it keeps an honest ledger of what the newsroom has posted to X.

- **API keys are open to anyone** — no account, no login. Every key lives in one shared pool.
- **The News API** serves the current edition as JSON: headline, summary, section, source, both
dates, and the photo URL.
- **X posting** runs from the scheduled newsroom refresh (7× a day) against `@jagxjrilicense`.

Live app: publish it from the platform (the **Publish** button). The static news site in the repo
root is the separate, Vercel-hosted site.

---

## Getting a key

Open the app's `/keys` page and press **Generate key**. The raw key is shown **once** — copy it then.
It looks like:

```
jxp_3GUnHUDUQbO3sOKdPlSN0keJx5ZmFr8U
```

Only a SHA-256 hash is stored, so the full key cannot be displayed again. If you lose it, generate a
new one and revoke the old from the same page.

Because the pool is shared, anyone with the `/keys` link can see the list (prefixes only) and revoke
a key. Treat a key as a shared credential, not a private one.

---

## The News API

Base URL: `<your-app-url>/trpc`

Every request carries the key as a Bearer token:

```
Authorization: Bearer jxp_YOUR_KEY_HERE
```

Inputs travel as a JSON-encoded `input` query parameter, **nested under a `json` key** — that is how
tRPC's superjson transformer carries typed arguments over GET.

### Endpoints

| Endpoint | What it returns | Input |
|---|---|---|
| `news.stories` | The edition, newest first | `section?`, `search?`, `limit` (1–100) |
| `news.latest` | The newest N across every section | `limit` (1–100) |
| `news.story` | One story by slug | `slug` |

### Sections

`world` · `africa` · `nigeria` · `business` · `tech` · `sports` · `entertainment` · `health` · `science`

### curl

```bash
# Latest 5
curl -s "https://YOUR-APP/trpc/news.stories?input=%7B%22json%22%3A%7B%22limit%22%3A5%7D%7D" \
  -H "Authorization: Bearer jxp_YOUR_KEY_HERE"

# Sports only
curl -s "https://YOUR-APP/trpc/news.stories?input=%7B%22json%22%3A%7B%22section%22%3A%22sports%22%2C%22limit%22%3A10%7D%7D" \
  -H "Authorization: Bearer jxp_YOUR_KEY_HERE"

# Search headlines and summaries
curl -s "https://YOUR-APP/trpc/news.stories?input=%7B%22json%22%3A%7B%22search%22%3A%22Chelsea%22%2C%22limit%22%3A5%7D%7D" \
  -H "Authorization: Bearer jxp_YOUR_KEY_HERE"
```

### JavaScript

```js
const KEY = "jxp_YOUR_KEY_HERE";
const BASE = "https://YOUR-APP/trpc";

async function jagx(path, input) {
  const url = new URL(BASE + path);
  url.searchParams.set("input", JSON.stringify({ json: input }));

  const res = await fetch(url, { headers: { Authorization: `Bearer ${KEY}` } });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body?.error?.json?.message ?? `HTTP ${res.status}`);
  }
  return (await res.json()).result.data.json;
}

const { stories, total, updated } = await jagx("/news.stories", {
  section: "nigeria",
  limit: 10,
});

console.log(`${total} stories, edition updated ${updated}`);
for (const s of stories) console.log(s.sectionLabel, "—", s.title, `(${s.source})`);
```

### Response shape

```json
{
  "edition": 1,
  "updated": "2026-11-12T13:22:29.562295+01:00",
  "updatedLabel": "12 Nov 2026 · 13:22 WAT",
  "total": 132,
  "stories": [
    {
      "slug": "photos-palmer-three-chelsea-stars-receive-guinness-world-records-certi",
      "title": "PHOTOS: Palmer, three Chelsea stars receive Guinness World Records certificates",
      "summary": "Four Chelsea players, including Cole Palmer and Estevão Willian, have been recognised…",
      "section": "sports",
      "sectionLabel": "Sports",
      "source": "Punch",
      "sourceUrl": "https://punchng.com/photos-palmer-three-chelsea-stars…/",
      "imageUrl": "/images/photos-palmer-three-chelsea-stars….webp",
      "publishedAt": "2026-11-12T13:08:28+01:00",
      "addedAt": "2026-11-12T13:22:29.562295+01:00"
    }
  ]
}
```

Both dates are deliberate: `publishedAt` is when the **source** published the story, `addedAt` is
when it entered the JagX Pulse edition. Show both and your readers always know how old a story is.

### Errors

| Status | Meaning |
|---|---|
| `401` | No key, or the key is invalid or revoked |
| `404` | No story with that slug in the current edition |
| `400` | The input did not validate — unknown section, or a limit outside 1–100 |

---

## X posting

Posting runs from the scheduled newsroom refresh, not from this app — the app holds no X token, so
it never claims a post happened unless a post id was recorded afterwards.

- **Account:** [@jagxjrilicense](https://x.com/jagxjrilicense) ("JagX and JRILICENSE")
- **Cadence:** seven times a day, alongside each edition refresh
- **Idempotency:** a story is posted once; its slug and post id are recorded, and the next run skips it

Post format (fits X's counter, which counts every link as 23 characters):

```
<headline>

<one-sentence summary>

<SECTION> · JagX Pulse
<url of the original source article>
```

Recording a post in the ledger:

```bash
curl -s -X POST "https://YOUR-APP/trpc/x.markPosted" \
  -H "Content-Type: application/json" \
  -d '{"json":{"slug":"<slug>","tweetId":"<post-id>","title":"<title>","section":"<section>"}}'
```

---

## Notes

- The edition changes **seven times a day**. Cache responses for a few minutes; do not poll continuously.
- `imageUrl` is a path onto the app's own bundled photos. Resolve it against your app origin, or cache
  the photo on your side if you need it to be permanent.
- Each story names its original publisher in `source` and links to it in `sourceUrl`. **Link back**
  when you republish — the reporting is theirs.

---

## Contact

Advertising, sponsorships and API partnerships: **jrilicense@gmail.com** · WhatsApp **+234 916 065 4415**

Powered by JagX · Licensed by JRILICENSE
