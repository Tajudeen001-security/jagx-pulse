#!/usr/bin/env python3
"""Refit X captions so the RAW length (full URL counted) stays under 275.

The endpoint counts the full raw URL, so we measure len() of the whole caption
and trim the summary (then the headline) until it fits.
"""
import json, os

REPO = "/workspace/repo"
DATA = os.path.join(REPO, "data", "stories.json")
LIMIT = 275


def assemble(headline, summary, section, url):
    parts = [headline]
    if summary:
        parts.append(summary)
    parts.append(f"{section} · JagX Pulse")
    return "\n\n".join(parts) + "\n" + url


def build(story):
    headline = story["title"].strip()
    section = story["section"].upper()
    url = story["url"]
    summary = (story.get("summary") or "").strip()

    cap = assemble(headline, summary, section, url)
    if len(cap) <= LIMIT:
        return cap

    # 1) shrink the summary word by word
    words = summary.split()
    while words:
        words.pop()
        cand = assemble(headline, " ".join(words) + "…", section, url)
        if len(cand) <= LIMIT:
            return cand
    # 2) summary gone: shrink the headline
    hw = headline.split()
    while hw:
        hw.pop()
        cand = assemble(" ".join(hw) + "…", "", section, url)
        if len(cand) <= LIMIT:
            return cand
    return assemble(headline[:40], "", section, url)


def main():
    d = json.load(open(DATA))
    out, bad = {}, []
    for s in d["stories"]:
        if s.get("tweetId"):
            continue
        cap = build(s)
        if len(cap) > LIMIT:
            bad.append((s["slug"], len(cap)))
        out[s["slug"]] = cap
    json.dump(out, open("/workspace/xcaps20.json", "w"), ensure_ascii=False, indent=1)
    lens = sorted(len(v) for v in out.values())
    print("captions:", len(out), "| over limit:", len(bad), "| min", lens[0], "max", lens[-1])
    for slug, n in bad[:10]:
        print("  OVER", n, slug)


if __name__ == "__main__":
    main()
