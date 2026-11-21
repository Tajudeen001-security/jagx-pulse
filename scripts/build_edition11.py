#!/usr/bin/env python3
"""Append edition 11 stories to data/stories.json and convert photos to webp."""
import json, os, sys
from datetime import datetime, timezone, timedelta
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAND = "/workspace/cand11"
WAT = timezone(timedelta(hours=1))
NOW = datetime.now(WAT)

# (slug, title, summary, section, source, url, published, photo)
STORIES = [
 ("poland-russia-missiles-airspace-incursion",
  "Poland says Russian missiles and a drone violated its airspace",
  "Poland's Defence Minister Wladyslaw Kosiniak-Kamysz said two Russian missiles and a suspected jet-powered drone crossed into Polish territory on Friday, with a Kh-101 cruise missile among them. Prime Minister Donald Tusk called it an intentional provocation timed to coincide with the Koalicja 2026 exercises involving 11 countries. NATO Secretary-General Mark Rutte called it a grave violation of Polish airspace; nobody was hurt and no damage was reported.",
  "world", "PBS NewsHour / AP",
  "https://www.pbs.org/newshour/world/nato-calls-russian-missiles-landing-in-poland-a-grave-violation-of-airspace",
  "2026-11-20T18:00:00+00:00", "poland1.jpg"),

 ("unicef-1144-children-killed-injured-ukraine",
  "UNICEF says 1,144 children killed or injured in Ukraine this year",
  "UNICEF said at least 1,144 children were killed or injured in Ukraine between January and October 2026, the highest verified toll in nearly four years, with 114 killed and 1,030 injured. In October alone at least 146 children were killed or injured, a 150% increase on the same month last year. The agency said verified strikes on energy infrastructure are 78% higher than in all of 2025.",
  "world", "Kyiv Independent",
  "https://kyivindependent.com/at-least-1-144-children-killed-or-injured-in-ukraine-during-russias-war-this-year-unicef-says",
  "2026-11-20T14:00:00+00:00", "ukraine1.jpg"),

 ("mlambo-ngcuka-dies-71",
  "Phumzile Mlambo-Ngcuka, South Africa's first female deputy president, dies at 71",
  "Phumzile Mlambo-Ngcuka, who served as South Africa's deputy president from 2005 to 2008 and later headed UN Women from 2013 to 2021, has died at 71. Her family said she passed away on Friday evening following complications from a medical procedure she underwent about two weeks ago. President Cyril Ramaphosa said the country's hearts were sad and broken at losing a dynamic woman leader.",
  "africa", "AP",
  "https://apnews.com/article/mlambongcuka-south-africa-deputy-president-obituary-ce72144fd0991768e9cb466daa95dfe5",
  "2026-11-21T10:00:00+00:00", "mlambo2.jpg"),

 ("nigeria-military-21-iswap-fighters-borno",
  "Nigerian air strikes kill 21 ISWAP fighters in Borno, military says",
  "Precision air strikes by Operation Hadin Kai between 16 and 17 November killed 21 Islamic State West Africa Province fighters and severely injured 10 others around Monguno and the South Lake Chad area of Borno State. The military said the strikes hit ISWAP's improvised explosive device network and killed two senior commanders, including a Shura Council member. Troops also rescued kidnapped victims and intercepted bomb-making materials in nationwide operations.",
  "nigeria", "Daily Post Nigeria",
  "https://dailypost.ng/2026/11/21/military-neutralises-21-iswap-fighters-rescues-kidnap-victims-in-nationwide-operations",
  "2026-11-21T08:00:00+00:00", "iswap1.jpg"),

 ("wall-street-ai-rout-correction-nasdaq",
  "S&P 500 and Dow close in correction as AI selloff deepens",
  "The S&P 500 fell 3.7% to 6,910.39 and the Dow dropped 949.73 points to 48,147.33 on Friday, both closing more than 10% below their records, while the Nasdaq sank 5.28% to 22,617.73 and turned negative for the year. Nvidia plunged 14% and ended the week down 23%, its worst week since the financial crisis, and Anthropic slipped close to its IPO price. For the week the S&P lost 8.6%, the Dow 8% and the Nasdaq 10%.",
  "business", "CNBC",
  "https://www.cnbc.com/2026/11/19/stock-market-today-live-updates.html",
  "2026-11-20T21:00:00+00:00", "wallst1.jpg"),

 ("naira-steepest-decline-parallel-market",
  "Naira posts steepest parallel-market decline in more than two years",
  "The naira weakened by N100 between 3 October and 18 November, sliding from N1,360 to N1,460 per dollar in the parallel market, a 7.35% depreciation. BusinessDay reported the move was driven by pre-election spending and rising dollar demand ahead of the festive season, exposing the limits of Central Bank interventions as liquidity tightened. The official rate moved far less, from N1,330.09 to N1,363.23 over the same period.",
  "business", "BusinessDay",
  "https://businessday.ng/news/article/nigerias-1-trillion-economy-impossible-without-northern-capital-umar-faruk",
  "2026-11-20T06:16:00+00:00", "naira1.jpg"),

 ("fugaku-supercomputer-cyberattack-riken",
  "Japan takes Fugaku supercomputer offline after cyberattack",
  "RIKEN shut down Japan's flagship Fugaku supercomputer on 14 November after intruders used a public operating-status dashboard to reach its internal network between 10 and 13 November. Information belonging to up to 4,222 Fugaku users and 375 users of the AI research system RIKYU may have been exposed, including names, email addresses and private SSH keys. RIKEN said it found no evidence research results were exfiltrated and has no restart date.",
  "tech", "BleepingComputer",
  "https://www.bleepingcomputer.com/news/security/japan-takes-fugaku-supercomputer-offlline-after-cyberattack",
  "2026-11-20T12:00:00+00:00", "fugaku2.jpg"),

 ("ireland-beat-south-africa-20-17-nations-championship",
  "Ireland beat South Africa 20-17 in the Nations Championship",
  "Robert Baloucoune scored two first-half tries as Ireland beat world champions South Africa 20-17 at the Aviva Stadium in Dublin. Ronan Kelleher also crossed before half-time, and despite Malcolm Marx's 58th-minute try the Springboks led for only four minutes. A losing bonus point still sent South Africa through to next Saturday's final at Twickenham, where they will face England or France.",
  "sports", "Sky Sports",
  "https://www.skysports.com/rugby-union/news/13614348/ireland-20-17-south-africa-springboks-downed-as-andy-farrells-side-hold-on-for-big-victory-in-nations-championship",
  "2026-11-21T18:52:00+00:00", "ireland1.jpg"),

 ("new-mexico-ncaa-cross-country-title-kipruto",
  "New Mexico win first NCAA men's cross country title as Kipruto takes individual crown",
  "New Mexico claimed its first-ever team championship at the 2026 NCAA Division I Cross Country Championships in Terre Haute, Indiana, placing three runners in the top 10. Louisville's Elsingi Kipruto won the individual 10K title in 28:27.7, becoming the first Cardinal to do so, ahead of Alabama's Dismus Lokira in 28:30.8. Oklahoma State's Denis Kipngetich finished third.",
  "sports", "NCAA.com",
  "https://www.ncaa.com/video/cross-country-men/2026-11-21/2026-di-mens-ncaa-cross-country-championship-full-race",
  "2026-11-21T17:00:00+00:00", "ncaa1.jpg"),

 ("hunger-games-sunrise-on-the-reaping-box-office",
  "'The Hunger Games: Sunrise on the Reaping' opens to $120M-plus",
  "The Hunger Games: Sunrise on the Reaping took $56 million from 4,018 North American theatres on its opening day and is heading for around $120 million by Sunday, far above the studio's cautious $85 million projection. It is the fifth-biggest opening in Lionsgate history and the highest-grossing launch of the careers of Glenn Close, Jesse Plemons, Kieran Culkin and Elle Fanning. The franchise's global box office now stands at roughly $3.437 billion.",
  "entertainment", "The Hollywood Reporter",
  "https://www.hollywoodreporter.com/movies/movie-news/hunger-games-sunrise-on-the-reaping-box-office-opening-win-2-1236760511",
  "2026-11-21T15:00:00+00:00", "hunger2.jpg"),

 ("ethiopia-polio-campaign-11-million-children",
  "Ethiopia launches polio campaign targeting 11.3 million children",
  "Ethiopia began a polio vaccination campaign on 21 November aimed at protecting more than 11.3 million children across five regions including Addis Ababa, Oromia and Central Ethiopia. The first round runs from 21 to 24 November with a second from 18 to 21 December, delivered house-to-house by health workers and community volunteers. WHO deployed 28 staff, saying circulating variant poliovirus type 1 was reported this year in Gambella, Oromia and South Ethiopia.",
  "health", "WHO Regional Office for Africa",
  "https://www.afro.who.int/countries/ethiopia/news/ethiopia-launches-polio-vaccination-campaign-protect-more-11-million-children-who-deployed-28-staff",
  "2026-11-21T09:00:00+00:00", "polio2.jpg"),

 ("jwst-andromeda-stellar-merger-bao",
  "Webb captures first direct view of a star swallowing its companion",
  "Astronomers using the James Webb Space Telescope have confirmed the first recorded act of a giant star swallowing its companion, in a binary system nicknamed Bao at the edge of the Andromeda galaxy. The supergiant, about seven times the Sun's mass, dragged in a star slightly smaller than the Sun over roughly seven years, releasing a huge burst of energy. The study was published on 18 November in the journal Nature.",
  "science", "Live Science",
  "https://www.livescience.com/space/astronomers-spot-giant-star-swallowing-its-companion-in-first-ever-observations-of-a-stellar-merger",
  "2026-11-18T00:00:00+00:00", "webb1.jpg"),
]


def main():
    path = os.path.join(REPO, "data", "stories.json")
    d = json.load(open(path))
    existing = {s["slug"] for s in d["stories"]}
    imgdir = os.path.join(REPO, "images")
    os.makedirs(imgdir, exist_ok=True)

    added = []
    for slug, title, summary, section, source, url, published, photo in STORIES:
        if slug in existing:
            print("SKIP duplicate:", slug); continue
        src = os.path.join(CAND, photo)
        if not os.path.exists(src):
            print("SKIP no photo:", slug); continue
        dst = os.path.join(imgdir, slug + ".webp")
        im = Image.open(src).convert("RGB")
        w, h = im.size
        if w > 1600:
            im = im.resize((1600, int(h * 1600 / w)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=82, method=6)
        added.append({
            "slug": slug, "title": title, "summary": summary,
            "section": section,
            "sectionLabel": section.capitalize(),
            "source": source, "url": url,
            "published": published,
            "added": NOW.isoformat(),
            "image": "images/" + slug + ".webp",
        })
        print("ADD", slug, os.path.getsize(dst))

    d["stories"].extend(added)
    d["edition"] = 11
    d["updated"] = NOW.isoformat()
    d["updatedLabel"] = NOW.strftime("%d %b %Y \u00b7 %H:%M WAT").lstrip("0")
    json.dump(d, open(path, "w"), indent=1, ensure_ascii=False)
    print("\nTOTAL", len(d["stories"]), "| edition", d["edition"], "|", d["updatedLabel"])


if __name__ == "__main__":
    main()
