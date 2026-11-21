#!/usr/bin/env python3
"""Append edition 10 stories to data/stories.json and convert photos to webp."""
import json, os, subprocess, sys
from datetime import datetime, timezone, timedelta
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAND = "/workspace/cand"
WAT = timezone(timedelta(hours=1))
NOW = datetime.now(WAT)

# (slug, title, summary, section, source, url, published, photo)
STORIES = [
 ("bahrain-iranian-attack-industrial-facility-fire",
  "Bahrain says Iranian attack hit industrial facility and caused a fire",
  "Bahrain's Interior Ministry said an Iranian attack struck a civilian industrial facility on Saturday, causing a fire and material damage but no injuries. Iran's Revolutionary Guards said they targeted US military positions in the kingdom, home to the US Navy's Fifth Fleet. Civil Defence teams worked to contain the blaze.",
  "world", "Reuters",
  "https://www.reuters.com/world/middle-east/bahrain-warns-residents-potential-threat-iran-conflict-persists-2026-11-21",
  "2026-11-21T14:15:00+00:00", "bahrain1.jpg"),

 ("bolsonaro-intensive-care-bowel-obstruction",
  "Brazil's Bolsonaro in intensive care with acute bowel obstruction",
  "Former Brazilian president Jair Bolsonaro was admitted to the intensive care unit at DF Star hospital in Brasilia with an acute obstructive abdomen after being hospitalised with severe abdominal pain. The hospital said the 71-year-old was clinically stable, conscious and breathing on his own, with a gastric tube inserted and no expected discharge date. He has had repeated abdominal problems since being stabbed on the campaign trail in 2018.",
  "world", "Al Jazeera",
  "https://www.aljazeera.com/news/2026/11/21/brazils-jair-bolsonaro-in-intensive-care-with-bowel-obstruction",
  "2026-11-21T15:00:00+00:00", "bolsonaro1.jpg"),

 ("lisbon-thousands-march-living-costs-housing",
  "Thousands march in Lisbon as living costs and rents fuel anger",
  "Thousands of people marched through central Lisbon in heavy rain to protest against soaring living costs, a deepening housing crisis and low wages. Organiser CGTP, Portugal's largest trade union federation, demanded higher wages and pensions, lower prices for essentials and measures to curb housing costs. House prices have more than doubled since 2017 and rents for new leases have nearly doubled.",
  "world", "Reuters",
  "https://www.reuters.com/world/europe/thousands-march-lisbon-living-costs-fuel-anger-2026-11-21",
  "2026-11-21T09:38:00+00:00", "lisbon1.jpg"),

 ("uganda-cancels-sgr-contract-yapi-merkezi",
  "Uganda cancels Standard Gauge Railway contract with Turkish firm Yapi Merkezi",
  "Uganda's Chief of Defence Forces, Gen Muhoozi Kainerugaba, announced the Standard Gauge Railway contract with Turkish construction firm Yapi Merkezi has been cancelled indefinitely, saying a more suitable partner would be found. The deal covered a 270-kilometre line from Malaba on the Kenyan border to Kampala. The project had already been delayed by difficulties securing financing.",
  "africa", "Kenyans.co.ke",
  "https://www.kenyans.co.ke/news/129568-uganda-cancels-multi-billion-sgr-deal-turkish-firm-muhoozi-claims",
  "2026-11-21T10:21:00+00:00", "uganda2.jpg"),

 ("somalia-eu-brussels-security-talks-aussom",
  "Somalia and EU hold Brussels security talks ahead of AUSSOM mandate decision",
  "Somalia and the European Union convened security transition talks in Brussels with AUSSOM troop-contributing countries Djibouti, Ethiopia, Kenya and Uganda, alongside the US, UK, Turkiye, Egypt and Gulf states. Participants stressed close coordination as the African Union mission's UN authorisation runs to 31 December 2026. The Security Council is expected to consider renewal next month.",
  "africa", "Hiiraan Online",
  "https://www.hiiraan.com/news4/2026/Nov/206822/somalia_eu_host_security_talks_in_brussels_ahead_of_aussom_mandate_decision__.aspx",
  "2026-11-21T12:00:00+00:00", "somalia1.jpg"),

 ("kenya-braces-intensifying-november-rains-floods",
  "Kenya braces for intensifying November rains as forecasters warn of floods",
  "Kenya's meteorological services forecast above-average rainfall in more than 40 counties including Nairobi, Mombasa, Kisumu and Garissa through November. The outlook warns that excessive rain could expose vulnerable communities to flooding, infrastructure damage and disruption to livelihoods. Rainfall remains critical to agriculture, livestock and water security.",
  "africa", "The Star Kenya",
  "https://www.the-star.co.ke/news/2026-11-21-kenya-braces-for-intensifying-november-rains",
  "2026-11-21T09:00:00+03:00", "kenya1.jpg"),

 ("tinubu-ibadan-apc-rally-low-key-bayelsa",
  "Tinubu holds low-key Ibadan rally after Bayelsa boat tragedy",
  "President Bola Tinubu and First Lady Oluremi Tinubu arrived in Ibadan for the South-West leg of the APC presidential campaign at Mapo Hall, the seventh stop of the 2027 re-election tour. Tinubu directed the rally be observed without much fanfare in honour of those lost in the Bayelsa boat disaster. He later flew to Lagos, where he was received by Governor Babajide Sanwo-Olu.",
  "nigeria", "Punch",
  "https://punchng.com/video-tinubu-first-lady-land-in-ibadan-for-apc-rally",
  "2026-11-21T14:00:00+01:00", "tinubu1.jpg"),

 ("nafdac-destroys-100bn-fake-products-ogun",
  "NAFDAC destroys ₦100bn of fake, expired and banned products in Ogun",
  "The National Agency for Food and Drug Administration and Control destroyed falsified, expired, banned and substandard products valued at about ₦100 billion at Ogwama Dumpsite in Ogere Remo, Ogun State. The haul included unregistered medicines, banned Analgin injections, expired codeine syrups, counterfeit cosmetics and unwholesome food. Director-General Mojisola Adeyeye said the aim was to stop dangerous products re-entering the market.",
  "nigeria", "P.M. News",
  "https://pmnewsnigeria.com/2026/11/21/nafdac-destroys-%E2%82%A6100bn-worth-of-fake-expired-and-banned-products-in-ogun",
  "2026-11-21T16:00:00+01:00", "nafdac1.jpg"),

 ("wall-street-ai-rout-sp500-dow-correction",
  "S&P 500 and Dow close in correction as AI rout deepens",
  "The S&P 500 fell 3.7% and the Dow dropped about 950 points, both entering correction territory, while the Nasdaq tumbled 5.3% to erase its 2026 gains. Nvidia slid roughly 12% and finished the week down 23%, its worst week since the financial crisis, and Anthropic gave back most of its IPO-day pop. For the week the S&P lost 8.6% and the Nasdaq 10%.",
  "business", "CNBC",
  "https://www.cnbc.com/2026/11/19/stock-market-today-live-updates.html",
  "2026-11-20T20:00:00+00:00", "nyse2.jpg"),

 ("oregon-sues-openai-2bn-teen-safety",
  "Oregon sues OpenAI for $2.035bn over ChatGPT and child safety",
  "Oregon Attorney General Dan Rayfield filed a $2.035 billion lawsuit against OpenAI in Multnomah County Circuit Court, accusing the company of endangering children and misleading parents about ChatGPT's safety. The complaint pleads violations of the state's Unlawful Trade Practices Act, negligence, unjust enrichment and public nuisance. OpenAI said it has built age-specific protections and will keep strengthening safeguards.",
  "tech", "Oregon Department of Justice",
  "https://www.doj.state.or.us/media-home/news-media-releases/ag-rayfield-files-2b-lawsuit-against-open-ai-launches-keeping-kids-safe-initiative",
  "2026-11-17T18:00:00+00:00", "openai1.jpg"),

 ("leeds-thrash-chelsea-stamford-bridge",
  "Leeds thrash Chelsea 4-1 at Stamford Bridge for first win there since 1999",
  "Leeds United beat Chelsea 4-1 at Stamford Bridge, their first victory at the ground since 1999, and moved three consecutive Premier League games unbeaten against the Blues. The result deepened pressure on Chelsea after an earlier home defeat to Tottenham. Leeds were worth the margin and could have won by more.",
  "sports", "TNT Sports",
  "https://www.facebook.com/tntsportsfootball/posts/leeds-win-at-stamford-bridge-for-the-first-time-since-1999-the-whites-thrash-che/1722419385914492",
  "2026-11-21T17:00:00+00:00", "leeds2.jpg"),

 ("newcastle-arsenal-2-2-madueke-rescue",
  "Madueke rescues Arsenal in 2-2 draw at Newcastle",
  "Noni Madueke snatched a 2-2 draw for Arsenal after Newcastle produced a stunning second-half turnaround at St James' Park. Eberechi Eze had put the champions ahead before Harvey Barnes and a second Magpies goal flipped the game. Arsenal's five-match league winning run ended but their lead at the top stretched to six points over Brighton.",
  "sports", "ESPN",
  "https://www.espn.com/soccer/report/_/gameId/401879232",
  "2026-11-21T19:30:00+00:00", "newcastle1.jpg"),

 ("hooker-beats-ortega-ufc-qatar",
  "Hooker snaps losing skid with unanimous decision over Ortega at UFC Qatar",
  "Dan Hooker beat Brian Ortega by unanimous decision (30-27, 30-27, 30-27) at UFC Fight Night in Doha, ending a three-fight losing streak. The lightweight bout was the co-main event on a card headlined by Jiri Prochazka against undefeated Navajo Stirling at ABHA Arena. Ortega has now lost four of his last five.",
  "sports", "UFC News",
  "https://x.com/UFCNews/status/2124228099219046697",
  "2026-11-21T18:00:00+00:00", "ufc3.jpg"),

 ("cma-awards-seven-year-ratings-high-swift",
  "CMA Awards hit seven-year ratings high as Taylor Swift returns",
  "The 60th CMA Awards drew 7.62 million live and same-day viewers, up 26% on last year and the show's largest audience since 2019. Taylor Swift's first CMA performance in 13 years, a medley of 'I Knew It, I Knew You' and 'Our Song', helped lift the 18-49 rating to 1.01, a three-year best. Lainey Wilson hosted for a third year and Ella Langley won Single of the Year.",
  "entertainment", "Billboard",
  "https://www.billboard.com/music/awards/2026-cma-awards-ratings-up-seven-year-high-1236387203",
  "2026-11-20T22:00:00+00:00", "cma2.jpg"),

 ("who-keeps-bundibugyo-ebola-pheic",
  "WHO keeps Bundibugyo Ebola a global health emergency as DRC cases pass 11,600",
  "WHO's Director-General determined on 18 November that the Bundibugyo Ebola outbreak in DR Congo, Kenya and Nigeria continues to constitute a public health emergency of international concern. The agency reassessed risk on 17 November, grouping states by population mobility and response capacity. WHO advises against travel and trade restrictions on affected countries.",
  "health", "WHO",
  "https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON630",
  "2026-11-20T00:00:00+00:00", "who1.png"),

 ("scientists-disagree-what-science-is-study",
  "Scientists disagree more than the public on what science actually is, study finds",
  "A study published in Royal Society Open Science found scientists' views on what counts as science are more divided than those of the general public. Researchers at the Santa Fe Institute surveyed definitions and found sharp disagreement across disciplines. The authors warn that as AI systems take on scientific work, a narrow definition could crowd out other valuable methods.",
  "science", "ScienceDaily",
  "https://www.sciencedaily.com/releases/2026/11/261119194541.htm",
  "2026-11-21T00:00:00+00:00", "sfi1.jpg"),
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
    d["edition"] = 10
    d["updated"] = NOW.isoformat()
    d["updatedLabel"] = NOW.strftime("%d %b %Y · %H:%M WAT").lstrip("0")
    json.dump(d, open(path, "w"), indent=1, ensure_ascii=False)
    print("\nTOTAL", len(d["stories"]), "| edition", d["edition"], "|", d["updatedLabel"])

if __name__ == "__main__":
    main()
