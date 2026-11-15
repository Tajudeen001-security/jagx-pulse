#!/usr/bin/env python3
"""
JagX Pulse — social publishing helper.

Handles the parts of social posting that are deterministic and must never be
guessed: image format conversion, caption composition against each platform's
real character budget, and the posted-ledger that stops double-posting.

The actual network calls are made by the agent through its connected MCP tools
(Twitter / Instagram); this script prepares and records.

Usage:
  python3 scripts/social.py convert            # webp -> jpg for every story
  python3 scripts/social.py convert --new      # only stories missing a jpg
  python3 scripts/social.py captions --new     # print ready-to-post captions
  python3 scripts/social.py mark --slug S --x ID --ig ID
  python3 scripts/social.py status
"""

import argparse
import json
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "stories.json")
IMG = os.path.join(ROOT, "images")
IG_IMG = os.path.join(IMG, "ig")

# Public base for images. Vercel serves the repo root, so a committed
# images/ig/<slug>.jpg is reachable by Meta's fetcher with no token.
PUBLIC_BASE = os.environ.get("JAGX_PUBLIC_BASE", "https://jagx-pulse.vercel.app")

# X counts every URL as 23 characters regardless of real length.
X_URL_WEIGHT = 23
X_LIMIT = 280
# Instagram captions allow 2200 characters; we stay well inside it.
IG_LIMIT = 2200


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def save(doc):
    tmp = DATA + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DATA)


def jpg_path(slug):
    return os.path.join(IG_IMG, slug + ".jpg")


def convert_one(story):
    """Convert a story's WebP photo to the JPEG Instagram requires."""
    src = story.get("image")
    if not src:
        return None, "no image"
    src_path = os.path.join(ROOT, src)
    if not os.path.exists(src_path):
        return None, "source missing"
    dst = jpg_path(story["slug"])
    os.makedirs(IG_IMG, exist_ok=True)
    try:
        im = Image.open(src_path).convert("RGB")
        # Instagram's feed favours 4:5 to 1.91:1. Pad rather than crop so we
        # never cut a subject out of a news photo.
        w, h = im.size
        target = 4 / 5
        if w / h > target:
            new_h = int(w / target)
            canvas = Image.new("RGB", (w, new_h), (10, 10, 10))
            canvas.paste(im, (0, (new_h - h) // 2))
            im = canvas
        elif w / h < 0.8:
            new_w = int(h * target)
            canvas = Image.new("RGB", (new_w, h), (10, 10, 10))
            canvas.paste(im, ((new_w - w) // 2, 0))
            im = canvas
        if im.size[0] > 1440:
            im = im.resize((1440, int(im.size[1] * 1440 / im.size[0])), Image.LANCZOS)
        im.save(dst, "JPEG", quality=88, optimize=True, progressive=True)
        return dst, None
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


def public_jpg_url(slug):
    return f"{PUBLIC_BASE}/images/ig/{slug}.jpg"


def x_caption(story):
    """Compose an X post that fits the weighted 280-character counter."""
    headline = story["title"].strip()
    section = story["section"].upper()
    url = story["url"]
    summary = (story.get("summary") or "").strip()

    # Fixed cost: headline + blank lines + section line + URL weight.
    fixed = len(headline) + len(f"\n\n{section} · JagX Pulse\n") + X_URL_WEIGHT
    room = X_LIMIT - fixed

    if room <= 0:
        # Headline alone is too long: trim it at a word boundary.
        keep = X_LIMIT - (len(f"\n\n{section} · JagX Pulse\n") + X_URL_WEIGHT) - 1
        headline = headline[:keep].rsplit(" ", 1)[0].rstrip(" ,.;:") + "…"
        summary = ""
    elif len(summary) > room:
        # Shorten the summary at a word boundary, never the headline.
        cut = summary[: room - 1].rsplit(" ", 1)[0].rstrip(" ,.;:")
        summary = cut + "…"

    parts = [headline]
    if summary:
        parts.append(summary)
    parts.append(f"{section} · JagX Pulse")
    body = "\n\n".join(parts)
    return f"{body}\n{url}"


def x_weighted_len(text):
    """Approximate X's weighted length: URLs count as 23."""
    import re

    urls = re.findall(r"https?://\S+", text)
    stripped = text
    for u in urls:
        stripped = stripped.replace(u, "", 1)
    return len(stripped) + X_URL_WEIGHT * len(urls)


def ig_caption(story):
    """Compose an Instagram caption: headline, summary, credit, link in bio."""
    section = story["section"].upper()
    summary = (story.get("summary") or "").strip()
    source = story.get("source", "")
    cap = f"{story['title'].strip()}\n\n{summary}\n\n{section} · JagX Pulse"
    if source:
        cap += f"\nSource: {source}"
    cap += "\n\nFull story and more at jagx-pulse.vercel.app"
    cap += "\n\nPowered by JagX · Licensed by JRILICENSE"
    if len(cap) > IG_LIMIT:
        cap = cap[: IG_LIMIT - 1].rsplit(" ", 1)[0] + "…"
    return cap


def cmd_convert(args):
    doc = load()
    done = skipped = failed = 0
    for s in doc["stories"]:
        if args.new and os.path.exists(jpg_path(s["slug"])):
            skipped += 1
            continue
        path, err = convert_one(s)
        if path:
            done += 1
        else:
            failed += 1
            print(f"  FAIL {s['slug']}: {err}", file=sys.stderr)
    print(f"converted {done}, skipped {skipped}, failed {failed}")


def cmd_captions(args):
    doc = load()
    out = []
    for s in doc["stories"]:
        if args.new and (s.get("tweetId") or s.get("igMediaId")):
            continue
        x = x_caption(s)
        out.append(
            {
                "slug": s["slug"],
                "title": s["title"],
                "section": s["section"],
                "x": x,
                "x_len": x_weighted_len(x),
                "ig": ig_caption(s),
                "ig_image_url": public_jpg_url(s["slug"]),
                "source_url": s["url"],
            }
        )
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_mark(args):
    doc = load()
    hit = None
    for s in doc["stories"]:
        if s["slug"] == args.slug:
            hit = s
            break
    if not hit:
        print(f"no story with slug {args.slug}", file=sys.stderr)
        return 1
    if args.x:
        hit["tweetId"] = args.x
        hit["postedToX"] = True
    if args.ig:
        hit["igMediaId"] = args.ig
        hit["postedToIG"] = True
    save(doc)
    print(f"marked {args.slug}: x={hit.get('tweetId')} ig={hit.get('igMediaId')}")
    return 0


def cmd_status(args):
    doc = load()
    st = doc["stories"]
    print(f"edition {doc.get('edition')} · {len(st)} stories · updated {doc.get('updatedLabel')}")
    print(f"  posted to X : {sum(1 for s in st if s.get('tweetId'))}")
    print(f"  posted to IG: {sum(1 for s in st if s.get('igMediaId'))}")
    print(f"  jpg ready   : {sum(1 for s in st if os.path.exists(jpg_path(s['slug'])))}")
    print(f"  missing jpg : {sum(1 for s in st if not os.path.exists(jpg_path(s['slug'])))}")
    print(f"  target 500  : {max(0, 500 - len(st))} to go")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("convert")
    c.add_argument("--new", action="store_true")
    c.set_defaults(func=cmd_convert)

    cp = sub.add_parser("captions")
    cp.add_argument("--new", action="store_true")
    cp.set_defaults(func=cmd_captions)

    m = sub.add_parser("mark")
    m.add_argument("--slug", required=True)
    m.add_argument("--x")
    m.add_argument("--ig")
    m.set_defaults(func=cmd_mark)

    s = sub.add_parser("status")
    s.set_defaults(func=cmd_status)

    args = p.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
