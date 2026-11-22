#!/usr/bin/env python3
"""Append edition 12 stories to data/stories.json and convert photos to webp."""
import json, os, sys
from datetime import datetime, timezone, timedelta
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAND = "/workspace/cand12"
WAT = timezone(timedelta(hours=1))
NOW = datetime.now(WAT)

# (slug, title, summary, section, source, url, published, photo)
STORIES = [
 ("bayelsa-boat-capsize-24-dead-mourners",
  "Boat carrying mourners capsizes in Bayelsa, killing at least 24",
  "A boat carrying mourners from Ayama to Ukubie for a burial ceremony capsized on Friday in Southern Ijaw, Bayelsa State, and emergency officials said at least 24 bodies had been recovered by Saturday. Police spokesman Musa Mohammed said preliminary findings pointed to a mechanical fault, while residents told Reuters the vessel was carrying at least 300 people. Twenty-four passengers were rescued, the driver fled and the boat's manager was taken into custody as divers and marine police continued searching.",
  "nigeria", "Premium Times / Reuters",
  "https://amp.dw.com/en/nigeria-at-least-24-dead-after-boat-capsizes/a-80011248",
  "2026-11-21T18:00:00+00:00", "boat2.jpg"),

 ("bandits-kill-niger-state-village-head",
  "Bandits behead Niger State village head and kill residents in dawn raid",
  "Suspected bandits attacked Lumma Ba'are community in Borgu Local Government Area of Niger State at about 5am on Saturday, beheading the village head and killing several residents including young children. Residents told SaharaReporters the attackers burnt houses, shops and motorcycles, planted explosives along access roads and abducted several people; police confirmed five deaths and said five injured victims were taken to hospital in New Bussa. Joint security teams were deployed and the search for the perpetrators was ongoing.",
  "nigeria", "Punch / SaharaReporters",
  "https://punchng.com/bandits-behead-niger-village-head-kill-five-others",
  "2026-11-21T14:00:00+00:00", "bandit1.jpg"),

 ("alabama-47-0-chattanooga-final-home-game",
  "Alabama rout Chattanooga 47-0 in final home tuneup before Iron Bowl",
  "Austin Mack threw for 254 yards and four touchdowns as No. 7 Alabama shut out Chattanooga 47-0 at Bryant-Denny Stadium on Saturday. The Crimson Tide defence held the Mocs to minus-12 yards early and forced a safety, while Daniel Hill ran for 75 yards in a ground game that finished with 263 net rushing yards. It was Alabama's last home game of the regular season, with the Iron Bowl at Auburn next.",
  "sports", "ESPN / Alabama Athletics",
  "https://www.espn.com/college-football/recap/_/gameId/401856746",
  "2026-11-21T22:00:00+00:00", "bama2.jpg"),

 ("aston-villa-0-0-sunderland-villa-park",
  "Aston Villa held 0-0 by Sunderland despite 72% possession",
  "Aston Villa dominated the ball but could not break down Sunderland in a 0-0 draw at Villa Park on Saturday, mustering just 0.98 expected goals from 17 attempts. Sunderland goalkeeper Robin Roefs made the key saves, including a late stop from Ross Barkley, and Chemsdine Talbi curled narrowly wide at the other end. The point ended Sunderland's run of three straight away defeats but left them in the bottom three, while Villa's unbeaten Premier League run reached seven games.",
  "sports", "ESPN / Sky Sports",
  "https://www.espn.com/soccer/report/_/gameId/401878756",
  "2026-11-21T17:17:00+00:00", "villa2.jpg"),

 ("trump-permanent-iran-deal-fox-interview",
  "Trump says he will seek a 'permanent' nuclear deal with Iran",
  "President Donald Trump said in a Fox News phone interview on Saturday that he intends to secure a permanent agreement with Iran that would stop Tehran from ever obtaining a nuclear weapon, regardless of who occupies the White House later. He said Iran had repeatedly broken past agreements, describing the current leadership as more reasonable but very difficult to negotiate with. Trump also claimed his administration had already dealt with successive groups of Iranian leadership, calling the situation the ultimate regime change.",
  "world", "Anadolu Agency / The Jerusalem Post",
  "https://www.aa.com.tr/en/middle-east/trump-vows-to-make-permanent-deal-with-iran-prevent-future-nuclear-ambitions/4133079",
  "2026-11-21T20:00:00+00:00", "trump1.jpg"),

 ("sparta-ii-russian-cargo-ship-drone-fire-baltic",
  "Russian cargo ship catches fire in Baltic after drone strike, Finland says Ukraine likely behind it",
  "The Russian-flagged cargo vessel Sparta II caught fire after being hit by drones in the Gulf of Finland on Saturday and later drifted into Finnish waters, prompting Helsinki to impose temporary air and maritime restrictions. Finland's Defence Forces said the 121-metre ship, owned by Oboronlogistika and bound for Kaliningrad, was damaged in international waters west of Gogland island, and Finland's prime minister said Kyiv had the right to strike back at its aggressor. Its 16-member crew evacuated to lifeboats and was taken aboard a nearby Russian ship.",
  "world", "CNBC / CNN",
  "https://www.cnbc.com/2026/11/21/russian-cargo-ship-hit-by-drones-in-baltic-finland-tightens-security.html",
  "2026-11-21T21:00:00+00:00", "sparta1.jpg"),

 ("dr-congo-sudan-drone-strikes-2230-civilians-killed",
  "UN says 2,230 civilians killed in Sudan in ten months, most by drones",
  "The UN Human Rights Office said at least 2,230 civilians were killed in Sudan between January and October 2026, including more than 1,630 in drone strikes, and warned the real toll is likely higher. Its report on the first half of the year documented at least 39 drone strikes on markets, 20 on civilian vehicles, 17 on fuel facilities and 16 on health facilities, with Kordofan accounting for more than two-thirds of recorded casualties. Rights chief Volker Turk said the documented violations could amount to war crimes.",
  "africa", "OHCHR / Anadolu Agency",
  "https://www.ohchr.org/en/press-releases/2026/11/sudan-un-report-details-deadly-civilian-impact-surge-drone-strikes",
  "2026-11-17T12:00:00+00:00", "sudan2.jpg"),

 ("senegal-faye-budget-decree-imf-bailout",
  "Senegal's Faye imposes budget by decree to unlock $2.2bn IMF bailout",
  "President Bassirou Diomaye Faye signed Senegal's revised 2026 budget into force by decree on Thursday after parliament rejected it, a move the government says is needed to meet conditions attached to a proposed $2.2 billion IMF programme. The decision deepened a standoff with the National Assembly controlled by the Pastef party of his former prime minister Ousmane Sonko, and critics questioned its legality. Senegal's public-sector debt was estimated at 132% of GDP at the end of 2024, and the IMF has said agreed fiscal reforms must be completed before it releases funds.",
  "africa", "Africanews / AFP",
  "https://www.africanews.com/2026/11/19/senegal-president-bypasses-parliament-to-advance-22-billion-imf-bailout",
  "2026-11-19T15:00:00+00:00", "senegal1.jpg"),

 ("ethiopia-eritrea-troops-badme-clashes",
  "Ethiopia and Eritrea mass troops at Badme as clashes raise war fears",
  "Ethiopia and Eritrea have massed troops and heavy weapons along their shared border, and conflict monitor ACLED reported direct clashes between the two armies near the disputed town of Badme on 13 November after Ethiopian drone strikes and Eritrean artillery fire. Eritrean forces retook Badme around 15 November and were reinforcing positions, while Ethiopian troops concentrated around Gemhalo about 32km south. Eritrea's government accused Ethiopia's Prosperity Party of an expansionist agenda, and G7 foreign ministers urged both sides to exercise maximum restraint.",
  "africa", "APAnews / allAfrica",
  "https://apanews.net/ethiopia-eritrea-amass-heavily-armed-troops-along-shared-border-report",
  "2026-11-19T09:00:00+00:00", "badme3.jpg"),

 ("naira-touches-1400-cbn-dollar-sales",
  "Naira touches N1,400/$ despite CBN selling $1.30bn in a week",
  "The naira depreciated 2.50% against the dollar on Friday to touch N1,400/$, closing at N1,394 from N1,360 on Monday, even after the Central Bank of Nigeria sold $1.30 billion to meet interbank demand that rose nearly twelvefold during the week. The parallel market moved further, weakening about N100 to N1,460 over the same period according to BusinessDay. The MPC meets on 23 and 24 November with the policy rate at 23% after a 350 basis point cut in September.",
  "business", "Nairametrics / BusinessDay",
  "https://nairametrics.com/2026/11/21/naira-depreciates-to-n1-400-cbn-sells-1-30-billion",
  "2026-11-21T11:35:00+00:00", "naira1.jpg"),

 ("cairn-ai-agents-zero-day-monai-label",
  "China-linked hackers used AI agents that found a zero-day on their own, Amazon says",
  "Amazon's threat intelligence team said a China-linked actor ran autonomous Cairn AI agents against university servers in East Asia and the agents discovered an unpatched path traversal flaw in MONAI Label, an open-source medical imaging tool. Within about 11 minutes the agents went from mapping the application's API to writing files on the server, then planted a Python reverse shell to reach root, with no human choosing each step. The campaign was uncovered because the operator left the Cairn instance publicly accessible without authentication, exposing prompts in Simplified Chinese and logs on China Standard Time.",
  "tech", "SecurityWeek / AWS Security Blog",
  "https://www.securityweek.com/amazon-china-linked-hackers-ai-agents-exploited-medical-software-zero-day",
  "2026-11-20T16:00:00+00:00", "cairn1.jpg"),

 ("us-loses-measles-elimination-status-paho",
  "US loses measles elimination status after 26 years, PAHO confirms",
  "The Pan American Health Organization announced on 17 November that endemic measles transmission has been reestablished in the United States, Mexico and Bolivia, and all three have lost elimination status. Under PAHO criteria a country loses the designation when the same virus genotype and lineage circulate uninterrupted for 12 months or more; the US had held it since 2000. Virginia reported its first measles death of the year this week, and states have reported a total of 12 deaths in 2026 against a CDC count of six.",
  "health", "PAHO / Contagion Live",
  "https://www.contagionlive.com/view/measles-update-november-20-2026",
  "2026-11-20T19:00:00+00:00", "measles1.jpg"),

 ("i-play-rocky-box-office-a-cinemascore",
  "'I Play Rocky' opens wide to $9.3m estimate and a rare A+ CinemaScore",
  "Amazon MGM expanded Peter Farrelly's Rocky origin story to 2,477 North American theatres and it earned $3.8 million on Friday including previews, heading for an estimated $9.3 million weekend and a $10.4 million cumulative total. The film, starring Anthony Ippolito as a young Sylvester Stallone, landed an A+ CinemaScore, only the second release this year to do so, with 89% from critics and 98% from audiences on Rotten Tomatoes. It finished second behind The Hunger Games: Sunrise on the Reaping, which opened to more than $120 million.",
  "entertainment", "Variety / The Hollywood Reporter",
  "https://variety.com/2026/film/box-office/box-office-hunger-games-sunrise-of-the-reaping-opening-day-1236954987",
  "2026-11-21T15:42:00+00:00", "rocky1.jpg"),

 ("spacex-dragon-crs-35-splashdown-science",
  "SpaceX Dragon returns to Earth with bioprinted blood vessels and tumour organoids",
  "The unpiloted SpaceX Dragon splashed down in the Pacific near Los Angeles on Saturday, completing NASA's 35th commercial resupply mission to the International Space Station. The capsule undocked on Friday carrying a 3D-bioprinted blood vessel construct used to study vascular ageing and cardiovascular disease, frozen tumour organoids treated aboard the station, and microbial samples to study how antibiotic-resistant bacteria adapt in space. A lighting system tested for more than three years to support astronaut sleep and wellbeing also came back.",
  "science", "NASA",
  "https://www.nasa.gov/blogs/spacestation/2026/11/21/dragon-returns-to-earth-packed-with-science-and-cargo",
  "2026-11-21T22:03:00+00:00", "dragon1.jpg"),
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
    d["edition"] = 12
    d["updated"] = NOW.isoformat()
    d["updatedLabel"] = NOW.strftime("%d %b %Y \u00b7 %H:%M WAT").lstrip("0")
    json.dump(d, open(path, "w"), indent=1, ensure_ascii=False)
    print("\nTOTAL", len(d["stories"]), "| edition", d["edition"], "|", d["updatedLabel"])


if __name__ == "__main__":
    main()
