#!/usr/bin/env python3
"""Append edition 6 stories to data/stories.json. Never deletes older stories."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "stories.json")

ADDED = "2026-11-15T12:20:00+01:00"

NEW = [
    {
        "slug": "irgc-claims-two-tankers-mines-hormuz",
        "section": "world",
        "sectionLabel": "World",
        "title": "IRGC says two oil tankers exploded on mines in the Strait of Hormuz",
        "summary": "Iran's Revolutionary Guard Navy said two oil tankers exploded and caught fire after striking naval mines in the Strait of Hormuz, claiming both vessels had switched off their navigation and AIS transponders to pass through an unauthorised route. The IRGC said two other tankers turned back after warnings from its maritime traffic control centre. US Central Command has not confirmed the Iranian account, and the reports could not be independently verified.",
        "source": "Al Jazeera",
        "url": "https://www.aljazeera.com/news/2026/11/15/iran-us-tensions-tankers-on-fire-hormuz",
        "published": "2026-11-15T06:30:00+00:00",
        "added": ADDED,
        "image": "images/irgc-claims-two-tankers-mines-hormuz.webp",
    },
    {
        "slug": "putin-xi-trump-trilateral-shenzhen-nov-19",
        "section": "world",
        "sectionLabel": "World",
        "title": "Kremlin confirms Putin, Xi and Trump will meet in Shenzhen on 19 November",
        "summary": "Kremlin spokesman Dmitry Peskov said an agreement has been reached for Vladimir Putin, Xi Jinping and Donald Trump to hold a trilateral meeting in Shenzhen on 19 November, on the sidelines of the APEC summit. The White House confirmed Trump's attendance at the 18-19 November summit. It would be the first trilateral summit bringing together the leaders of the United States, Russia and China.",
        "source": "Anadolu Agency",
        "url": "https://www.aa.com.tr/en/eurasia/kremlin-says-putin-xi-trump-to-hold-trilateral-meeting-in-shenzhen-on-nov-19/4125290",
        "published": "2026-11-14T18:40:00+00:00",
        "added": ADDED,
        "image": "images/putin-xi-trump-trilateral-shenzhen-nov-19.webp",
    },
    {
        "slug": "cape-verde-polls-open-neves-second-term",
        "section": "africa",
        "sectionLabel": "Africa",
        "title": "Cape Verde votes as President Neves seeks a second term",
        "summary": "Cape Verdeans went to the polls on Sunday in a presidential election that pits incumbent Jose Maria Neves against five challengers, including former justice minister Joana Rosa, who is seeking to become the country's first female president. Neves, in office since 2021 and prime minister from 2001 to 2016, is favoured to win another five-year term. The vote is widely seen as a test of democratic stability in a region hit by coups elsewhere.",
        "source": "Al Jazeera",
        "url": "https://www.aljazeera.com/news/2026/11/15/polls-open-in-cape-verde-in-race-with-first-female-presidential-candidate",
        "published": "2026-11-15T08:00:00+00:00",
        "added": ADDED,
        "image": "images/cape-verde-polls-open-neves-second-term.webp",
    },
    {
        "slug": "adf-attacks-kill-44-civilians-ituri",
        "section": "africa",
        "sectionLabel": "Africa",
        "title": "Islamic State-linked attacks kill at least 44 civilians in eastern DR Congo",
        "summary": "Gunmen from the Islamic State-linked Allied Democratic Forces killed at least 44 civilians in a series of raids across north-eastern DR Congo this week, according to humanitarian and security sources. A local official said victims were hacked with machetes and shot. The attacks in Ituri province came days after the same group killed 66 people in neighbouring North Kivu.",
        "source": "Africanews",
        "url": "https://www.africanews.com/2026/11/14/dr-congo-at-least-44-dead-in-attack-by-islamic-state-linked-gunmen",
        "published": "2026-11-14T09:15:00+00:00",
        "added": ADDED,
        "image": "images/adf-attacks-kill-44-civilians-ituri.webp",
    },
    {
        "slug": "algeria-sentences-kamel-daoud-five-years",
        "section": "africa",
        "sectionLabel": "Africa",
        "title": "Algeria sentences writer Kamel Daoud to five years over novel",
        "summary": "A court in the western Algerian city of Oran sentenced Prix Goncourt winner Kamel Daoud and his wife, psychiatrist Aicha Dahdouh, to five years in prison in absentia for breaching professional confidentiality and invading privacy. The case followed a complaint from a woman who said the novel Houris used details she disclosed in therapy. Both live in France and were also fined 300,000 dinars each; Daoud called the verdict a trial without defence or justice.",
        "source": "RFI",
        "url": "https://www.rfi.fr/en/international/20261113-algerian-writer-kamel-daoud-sentenced-to-five-years-over-prize-winning-novel",
        "published": "2026-11-13T16:20:00+00:00",
        "added": ADDED,
        "image": "images/algeria-sentences-kamel-daoud-five-years.webp",
    },
    {
        "slug": "tinubu-revive-dormant-nnpc-refineries",
        "section": "nigeria",
        "sectionLabel": "Nigeria",
        "title": "Tinubu pledges to revive Nigeria's dormant refineries",
        "summary": "President Bola Tinubu has pledged to rehabilitate Nigeria's dormant national refineries, saying the facilities will not be allowed to become stranded investments as domestic refining capacity expands. Officials said Nigeria needs up to $40 billion in fresh oil and gas investment by 2030, and that talks with NNPC on a pilot national strategic stock programme are at an advanced stage. Import licences will stay open on published, merit-based criteria.",
        "source": "The Guardian Nigeria",
        "url": "https://guardian.ng/business-services/tinubu-reiterates-plan-to-revive-refineries-as-local-capacity-expands",
        "published": "2026-11-14T11:00:00+00:00",
        "added": ADDED,
        "image": "images/tinubu-revive-dormant-nnpc-refineries.webp",
    },
    {
        "slug": "nvidia-investors-urge-board-jensen-huang-return",
        "section": "business",
        "sectionLabel": "Business",
        "title": "Nvidia investors urge board to weigh a return of Jensen Huang",
        "summary": "Altimeter Capital's Brad Gerstner and Atreides Management's Gavin Baker wrote to Nvidia's board urging a slow, measured and deliberate process on the company's future leadership, including the potential return of Jensen Huang. The letter did not call for his immediate reinstatement. Elon Musk said on X that he signed a petition backing Huang, which organisers say has more than 100,000 signatures including over 5,000 current Nvidia employees.",
        "source": "CNBC",
        "url": "https://www.cnbc.com/2026/11/14/nvidia-investors-jensen-huang-return-board-letter.html",
        "published": "2026-11-14T19:30:00+00:00",
        "added": ADDED,
        "image": "images/nvidia-investors-urge-board-jensen-huang-return.webp",
    },
    {
        "slug": "microsoft-apologises-global-outage-no-cyberattack",
        "section": "tech",
        "sectionLabel": "Tech",
        "title": "Microsoft apologises for global outage and rules out a cyberattack",
        "summary": "Microsoft apologised after a global service disruption took down Teams, Outlook and Copilot for more than 24 hours across at least 70 countries, affecting government agencies, schools, airlines and hospitals. The company said the fault was introduced during an earlier network capacity upgrade and triggered by a subsequent network change, and that it found no indication of malicious activity or an AI cause. Service has since been restored, though Microsoft warned of intermittent issues.",
        "source": "CGTN",
        "url": "https://news.cgtn.com/news/2026-11-14/Microsoft-apologizes-for-global-outage-rules-out-cyberattack-1S3I9qOB6F2/p.html",
        "published": "2026-11-14T11:29:00+00:00",
        "added": ADDED,
        "image": "images/microsoft-apologises-global-outage-no-cyberattack.webp",
    },
    {
        "slug": "patriots-lions-nfl-munich-allianz-arena",
        "section": "sports",
        "sectionLabel": "Sports",
        "title": "Patriots and Lions meet in Munich as NFL returns to Germany",
        "summary": "The New England Patriots (5-4) face the Detroit Lions (6-2) at FC Bayern Munich's Allianz Arena on Sunday in the NFL's Week 10 international game, the sixth regular-season game staged in Germany and the third in Munich. Detroit arrive on a four-game winning run knowing a victory would put them top of the NFC North. New England are coming off a 45-27 home defeat to Green Bay and have injury concerns, with A.J. Brown and Rhamondre Stevenson among those listed questionable.",
        "source": "DAZN",
        "url": "https://www.dazn.com/en-US/news/football/patriots-vs-lions-munich-preview-key-matchups-how-to-watch-nfl-game-pass/8l6zkg3pfiju1l8my44vi5hvl",
        "published": "2026-11-14T14:00:00+00:00",
        "added": ADDED,
        "image": "images/patriots-lions-nfl-munich-allianz-arena.webp",
    },
    {
        "slug": "sayers-backs-khawaja-sandpapergate-claims",
        "section": "sports",
        "sectionLabel": "Sports",
        "title": "Chadd Sayers backs Khawaja's sandpapergate account as Cummins denies it",
        "summary": "Former Australia seamer Chadd Sayers said Usman Khawaja's account of the 2018 Cape Town ball-tampering scandal is accurate, backing the opener's claim in his book Sabr that the whole Test team knew sandpaper was being used. Pat Cummins has called the claim 100 per cent wrong, and Cricket Australia defended its original investigation. David Warner publicly supported Khawaja, while Mitchell Johnson questioned the timing of the revelations.",
        "source": "BBC Sport",
        "url": "https://www.bbc.com/sport/cricket/articles/c6x2v277z89eo",
        "published": "2026-11-14T09:00:00+00:00",
        "added": ADDED,
        "image": "images/sayers-backs-khawaja-sandpapergate-claims.webp",
    },
    {
        "slug": "governors-awards-17th-ceremony-honorary-oscars",
        "section": "entertainment",
        "sectionLabel": "Entertainment",
        "title": "Academy holds 17th Governors Awards, honouring Close, Norman and Scott",
        "summary": "The Academy of Motion Picture Arts and Sciences holds its 17th Governors Awards on Sunday at the Ray Dolby Ballroom at Ovation Hollywood, the first major event of the awards season. Academy Honorary Awards go to actor Glenn Close, animator Floyd Norman and director Ridley Scott, with the Irving G. Thalberg Memorial Award to producers Christine Vachon and Pamela Koffler. The honours are conferred by the Academy's Board of Governors rather than voted by members.",
        "source": "Academy Press Office",
        "url": "http://press.oscars.org/news/academy-honor-glenn-close-floyd-norman-ridley-scott-and-christine-vachon-pamela-koffler-2026",
        "published": "2026-11-15T02:00:00+00:00",
        "added": ADDED,
        "image": "images/governors-awards-17th-ceremony-honorary-oscars.webp",
    },
    {
        "slug": "nigeria-ebola-contacts-42-day-countdown",
        "section": "health",
        "sectionLabel": "Health",
        "title": "Nigeria must clear 42 days of Ebola monitoring before being declared free",
        "summary": "The WHO's executive director for health emergencies, Chikwe Ihekweazu, said Nigeria must monitor all 53 identified contacts of its imported Ebola case for 21 days and then a further 21 before it can be declared free of the disease. The NCDC had targeted 13 November to complete monitoring of 62 contacts linked to the case, a woman who travelled from Uganda and was later evacuated to Switzerland. Ihekweazu said the evacuation reflected the requesting country's wishes, not any gap in Nigerian capacity.",
        "source": "Arise News",
        "url": "https://www.arise.tv/ihekweazu-nigeria-must-complete-42-day-monitoring-before-declaring-ebola-free",
        "published": "2026-11-14T15:00:00+00:00",
        "added": ADDED,
        "image": "images/nigeria-ebola-contacts-42-day-countdown.webp",
    },
    {
        "slug": "stanford-brain-activity-predicts-alzheimers",
        "section": "science",
        "sectionLabel": "Science",
        "title": "Brain activity patterns may flag Alzheimer's years before memory slips",
        "summary": "Stanford Medicine-led researchers compared resting-state functional MRI in 180 cognitively normal super agers and 110 people with Alzheimer's disease, finding distinct patterns of underactivity and overactivity across brain regions that separated the two groups. The patterns, known as functional connectivity, predicted future cognitive decline more effectively than age, genetics or amyloid and tau biomarkers. The team says the approach could reveal Alzheimer's risk earlier than existing tests.",
        "source": "Stanford Medicine",
        "url": "https://med.stanford.edu/news/all-news/2026/11/alzheimers-brain-activity.html",
        "published": "2026-11-04T17:00:00+00:00",
        "added": ADDED,
        "image": "images/stanford-brain-activity-predicts-alzheimers.webp",
    },
]


def main():
    with open(DATA) as f:
        doc = json.load(f)

    existing = {s["slug"] for s in doc["stories"]}
    added = []
    for s in NEW:
        if s["slug"] in existing:
            print("SKIP duplicate:", s["slug"])
            continue
        doc["stories"].append(s)
        added.append(s["slug"])

    doc["edition"] = 6
    doc["updated"] = ADDED
    doc["updatedLabel"] = "15 Nov 2026 \u00b7 12:20 WAT"

    with open(DATA, "w") as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)

    print("added", len(added), "stories; total now", len(doc["stories"]))
    for s in added:
        print("  +", s)


if __name__ == "__main__":
    main()
