#!/usr/bin/env python3
"""Re-fit X captions to a safe weighted length (<=268) using the same
structure as scripts/social.py, then print them for posting."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "stories.json")
IG_IMG = os.path.join(ROOT, "images", "ig")
PUBLIC_BASE = "https://jagx-pulse.vercel.app"
X_URL_WEIGHT = 23
SAFE = 268

TARGETS = [
    "zambia-mundubile-treason-indictment",
    "ndlea-enugu-meth-lab-five-mexicans",
    "sanofi-acquires-insmed-41-billion",
    "wisconsin-third-measles-death-920-cases",
    "cia-odni-osint-system-breach",
    "somalia-uganda-al-shabaab-offensive-communique",
    "ethiopia-abiy-sudan-dialogue-initiative",
    "eu-extends-mozambique-military-mission-2028",
    "us-tariffs-china-industrial-subsidies",
    "kospi-tumbles-ai-selloff-softbank",
    "anthropic-openai-staff-unreleased-models-alarm",
    "real-madrid-5-1-psv-bellingham-mbappe",
    "arsenal-dortmund-1-1-gyokeres",
    "nba-cup-mavericks-nuggets-celtics-wizards",
    "hunger-games-sunrise-reaping-monday-record",
    "oldest-compact-quasar-pair-cosmic-dawn",
    "deere-q4-2026-results-2027-outlook",
    "relativity-collapses-triple-bond-cbi",
]


def wlen(text):
    urls = re.findall(r"https?://\S+", text)
    stripped = text
    for u in urls:
        stripped = stripped.replace(u, "", 1)
    return len(stripped) + X_URL_WEIGHT * len(urls)


def fit(story):
    headline = story["title"].strip()
    section = story["section"].upper()
    url = story["url"]
    summary = (story.get("summary") or "").strip()
    tail = f"\n\n{section} \u00b7 JagX Pulse\n"
    fixed = len(headline) + len(tail) + X_URL_WEIGHT
    room = SAFE - fixed
    if room <= 0:
        keep = SAFE - (len(tail) + X_URL_WEIGHT) - 1
        headline = headline[:keep].rsplit(" ", 1)[0].rstrip(" ,.;:") + "\u2026"
        summary = ""
    elif len(summary) > room:
        cut = summary[: room - 1].rsplit(" ", 1)[0].rstrip(" ,.;:")
        summary = cut + "\u2026"
    parts = [headline]
    if summary:
        parts.append(summary)
    parts.append(f"{section} \u00b7 JagX Pulse")
    return "\n\n".join(parts) + "\n" + url


def main():
    with open(DATA, encoding="utf-8") as f:
        doc = json.load(f)
    by = {s["slug"]: s for s in doc["stories"]}
    out = []
    for slug in TARGETS:
        s = by.get(slug)
        if not s:
            print(f"MISSING {slug}", file=sys.stderr)
            continue
        if s.get("tweetId"):
            print(f"ALREADY POSTED {slug}", file=sys.stderr)
            continue
        cap = fit(s)
        jpg = os.path.join(IG_IMG, slug + ".jpg")
        out.append({
            "slug": slug,
            "section": s["section"],
            "x": cap,
            "x_len": wlen(cap),
            "has_jpg": os.path.exists(jpg),
            "ig_image_url": f"{PUBLIC_BASE}/images/ig/{slug}.jpg",
        })
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
