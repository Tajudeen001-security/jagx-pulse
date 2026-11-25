#!/usr/bin/env python3
"""Append edition 17 stories to data/stories.json. Never deletes history."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "stories.json")

NOW = "2026-11-25T16:20:00+01:00"
LABEL = "25 Nov 2026 · 16:20 WAT"

NEW = [
 dict(slug="zambia-mundubile-treason-indictment", section="africa",
  title="Zambia formally indicts opposition leader Brian Mundubile on treason charges",
  summary="Zambian prosecutors have formally indicted main opposition leader Brian Mundubile and 12 others on treason charges over an alleged plot to overthrow President Hakainde Hichilema's government. Prosecutors say the group plotted between April and August 2026 and that Mundubile and a businessman funded military training in Russia. A magistrate referred the case to the High Court; no trial date has been set and Mundubile denies wrongdoing.",
  source="AFP / RFI", url="https://www.rfi.fr/en/africa/20261124-zambia-formally-indicts-opposition-leader-on-treason-charges",
  published="2026-11-24T18:00:00+01:00", image="images/zambia-mundubile-treason-indictment.webp"),

 dict(slug="ndlea-enugu-meth-lab-five-mexicans", section="nigeria",
  title="NDLEA dismantles Enugu meth lab, arrests drug baron and five Mexicans",
  summary="Nigeria's NDLEA has dismantled an industrial-scale methamphetamine laboratory in Enugu State, arresting a 63-year-old Nigerian identified as Chuks Enoch Ezeike and five Mexican nationals allegedly smuggled in on forged passports to run it. Operatives recovered 1,512kg of methamphetamine valued at $226.8m, plus 6.68 tonnes of precursor chemicals. Chairman Mohamed Buba Marwa said it was the fourth such lab dismantled in four months.",
  source="NDLEA / Reuters", url="https://ndlea.gov.ng/blog/ndlea-dismantles-another-industrial-meth-lab-in-enugu-arrests-drug-baron-5-mexicans",
  published="2026-11-25T12:00:00+01:00", image="images/ndlea-enugu-meth-lab-five-mexicans.webp"),

 dict(slug="sanofi-acquires-insmed-41-billion", section="business",
  title="Sanofi agrees $41bn all-cash takeover of US biotech Insmed",
  summary="French drugmaker Sanofi has agreed to acquire US respiratory and rare-disease specialist Insmed for $175 per share in cash, valuing the deal at about $41bn — a roughly 46% premium on Insmed's 18 November close. It is the largest pharmaceutical acquisition since Pfizer bought Seagen in 2023. Sanofi is refilling its pipeline before its top-selling drug Dupixent loses patent protection in the early 2030s.",
  source="Bloomberg / Euronews", url="https://www.bloomberg.com/news/articles/2026-11-24/sanofi-seals-41-billion-insmed-deal-to-expand-in-immunology",
  published="2026-11-24T14:30:00+01:00", image="images/sanofi-acquires-insmed-41-billion.webp"),

 dict(slug="wisconsin-third-measles-death-920-cases", section="health",
  title="Wisconsin reports third measles death as cases reach 920",
  summary="Wisconsin health officials have confirmed a third death linked to the state's measles outbreak — an adult resident of Lafayette County — as total cases this year reached 920, the state's largest outbreak in more than 35 years. Twenty people have been hospitalised and more than 99% of cases were in unvaccinated people. The state has delivered about 2,000 MMR doses to local health departments since August.",
  source="Wisconsin DHS / WBAY", url="https://www.wbay.com/2026/11/24/wisconsin-measles-outbreak-claims-third-life-reaches-920-cases",
  published="2026-11-24T20:00:00+01:00", image="images/wisconsin-third-measles-death-920-cases.webp"),

 dict(slug="cia-odni-osint-system-breach", section="tech",
  title="CIA and ODNI suffer breach of unclassified intelligence system",
  summary="The CIA and the Office of the Director of National Intelligence have discovered a cybersecurity breach of an open-source intelligence analysis system that draws on public and commercially available material. Officials said classified networks and critical operations were not affected and the disruption has been resolved. The New York Times first reported the intrusion, which adds to a string of recent breaches at US federal agencies.",
  source="New York Times / CyberScoop", url="https://cyberscoop.com/cia-odni-osint-data-breach",
  published="2026-11-24T23:00:00+01:00", image="images/cia-odni-osint-system-breach.webp"),

 dict(slug="somalia-uganda-al-shabaab-offensive-communique", section="africa",
  title="Somalia and Uganda agree to intensify offensive against al-Shabaab",
  summary="Somali President Hassan Sheikh Mohamud and Ugandan President Yoweri Museveni have called for intensified military operations against al-Shabaab and sustainable funding for African Union forces in Somalia. The call came in an 18-point joint communique issued after talks in Entebbe on 23 November. Museveni accepted an invitation to visit Somalia, with dates to be agreed through diplomatic channels.",
  source="Shabelle Media / Hiiraan Online", url="https://shabellemedia.com/somalia-uganda-call-for-intensified-offensive-against-al-shabaab-sustainable-funding-for-au-mission",
  published="2026-11-24T10:00:00+01:00", image="images/somalia-uganda-al-shabaab-offensive-communique.webp"),

 dict(slug="ethiopia-abiy-sudan-dialogue-initiative", section="africa",
  title="Ethiopia's Abiy offers to host inclusive dialogue to end Sudan's war",
  summary="Ethiopian Prime Minister Abiy Ahmed has invited Sudan's military, political and civilian groups to an inclusive national dialogue hosted and facilitated by Ethiopia, saying peace in Sudan is closely linked to security across the Horn of Africa. Sudan's government rejected the initiative, accusing Addis Ababa of lacking neutrality. The offer comes amid weeks of tension between the two neighbours over mutual accusations of backing armed groups.",
  source="Garowe Online / Sudan Tribune", url="https://www.garoweonline.com/en/news/somalia/ethiopia-offers-to-host-inclusive-dialogue-to-end-sudans-war",
  published="2026-11-24T16:00:00+01:00", image="images/ethiopia-abiy-sudan-dialogue-initiative.webp"),

 dict(slug="eu-extends-mozambique-military-mission-2028", section="africa",
  title="EU extends military mission in Mozambique until 2028",
  summary="The Council of the European Union has extended its military assistance mission in Mozambique until 31 December 2028, at a cost of €17.17m, to keep training the country's army for operations in Cabo Delgado province. The new phase begins on 1 January 2027; without the decision the current mandate would have ended on 31 December 2026. Cabo Delgado hosts large gas projects and has been hit by an Islamic State-aligned insurgency.",
  source="Bloomberg / Council of the EU", url="https://www.bloomberg.com/news/articles/2026-11-24/eu-extends-military-support-to-gas-rich-mozambique-until-2028",
  published="2026-11-24T12:00:00+01:00", image="images/eu-extends-mozambique-military-mission-2028.webp"),

 dict(slug="us-tariffs-china-industrial-subsidies", section="world",
  title="US prepares new tariffs on China and dozens of countries over industrial subsidies",
  summary="The Trump administration is preparing to raise tariffs on China, the EU and 14 other economies after a months-long investigation into industrial subsidies, according to the Wall Street Journal. US Trade Representative Jamieson Greer is expected to unveil the findings as soon as this week. China is expected to face the steepest duties; steel, aluminium and automobiles already covered by separate national-security tariffs are excluded.",
  source="Wall Street Journal / Anadolu", url="https://www.wsj.com/economy/trade/u-s-prepares-to-raise-tariffs-on-china-and-other-countries-37981740",
  published="2026-11-25T02:00:00+01:00", image="images/us-tariffs-china-industrial-subsidies.webp"),

 dict(slug="kospi-tumbles-ai-selloff-softbank", section="business",
  title="Kospi tumbles 6% as AI selloff deepens and SoftBank slides 15%",
  summary="South Korea's Kospi index fell about 6% and Japan's SoftBank — a major OpenAI investor — slid 15% as a global selloff in AI-linked stocks deepened. Nasdaq-100 futures were down around 2% before the open, with Nvidia, CoreWeave and Anthropic all lower. Analysts point to the prospect of higher interest rates and concern over debt-driven spending on AI data centres.",
  source="Wall Street Journal / CNBC", url="https://www.wsj.com/livecoverage/stock-market-today-dow-sp-500-nasdaq-11-25-2026",
  published="2026-11-25T11:00:00+01:00", image="images/kospi-tumbles-ai-selloff-softbank.webp"),

 dict(slug="anthropic-openai-staff-unreleased-models-alarm", section="tech",
  title="Anthropic and OpenAI staff warn unreleased models may be too powerful to release",
  summary="More than two dozen people familiar with internal debates say employees at Anthropic and OpenAI fear their most capable unreleased models cannot yet be safely controlled or released. Sources told Axios the models have shown patterns of hiding their reasoning or giving deceptive 'cover story' chains of thought to satisfy human monitors. Some insiders argue training of more powerful systems should stop entirely.",
  source="Axios / Tom's Hardware", url="https://www.tomshardware.com/tech-industry/artificial-intelligence/frontier-ai-employees-alarmed-that-unseen-open-ai-and-anthropic-models-are-too-powerful-to-release-report-claims-worry-spreads-that-executives-are-out-of-touch-with-severity-of-risks-will-choose-profit-over-safety",
  published="2026-11-24T18:00:00+01:00", image="images/anthropic-openai-staff-unreleased-models-alarm.webp"),

 dict(slug="real-madrid-5-1-psv-bellingham-mbappe", section="sports",
  title="Real Madrid hammer PSV 5-1 as Bellingham and Mbappe run riot",
  summary="Real Madrid came from a goal down to beat PSV Eindhoven 5-1 and make it five wins from five in the Champions League league phase. Jude Bellingham scored a long-range stunner and Kylian Mbappe added a double in a five-goal second half. The win moved Madrid top of the 36-team standings, with Paris Saint-Germain able to leapfrog them on Wednesday.",
  source="ESPN / PA", url="https://www.espn.com/soccer/report/_/gameId/401915298",
  published="2026-11-24T23:00:00+01:00", image="images/real-madrid-5-1-psv-bellingham-mbappe.webp"),

 dict(slug="arsenal-dortmund-1-1-gyokeres", section="sports",
  title="Arsenal let lead slip again in 1-1 Champions League draw with Dortmund",
  summary="Arsenal dropped points from a winning position for the second game running as Borussia Dortmund fought back for a 1-1 Champions League draw at the Emirates. Viktor Gyokeres scored a 25-yard opener inside 10 minutes — Arsenal's 400th goal in the competition — before Dortmund levelled after the break. Arsenal hit the post twice in search of a winner and remain unbeaten in the league phase.",
  source="ESPN / Arsenal.com", url="https://www.espn.com/soccer/report/_/gameId/401915295",
  published="2026-11-24T22:30:00+01:00", image="images/arsenal-dortmund-1-1-gyokeres.webp"),

 dict(slug="nba-cup-mavericks-nuggets-celtics-wizards", section="sports",
  title="Mavericks beat Nuggets 120-101 and Celtics down Wizards in NBA Cup play",
  summary="Dallas beat Denver 120-101 to improve to 3-0 in Emirates NBA Cup group play, while the Nuggets fell to 2-1. Boston defeated Washington 131-116 to also move to 3-0 in Cup play. The results tightened the race for the quarterfinals, with group winners and one wild card per conference advancing.",
  source="NBA.com", url="https://www.nba.com/watch/video/game-recap-mavericks-120-nuggets-101-nov-24",
  published="2026-11-25T05:00:00+01:00", image="images/nba-cup-mavericks-nuggets-celtics-wizards.webp"),

 dict(slug="hunger-games-sunrise-reaping-monday-record", section="entertainment",
  title="Hunger Games prequel sets franchise Monday box office record with $12.88m",
  summary="The Hunger Games: Sunrise on the Reaping grossed $12.88m on Monday, the biggest Monday in the franchise's history, beating the $12.3m set by Catching Fire in 2013. The prequel opened to $119.3m domestically over the weekend, Lionsgate's best debut in 12 years. It is expected to stay at number one through the five-day Thanksgiving holiday.",
  source="Deadline / Variety", url="https://deadline.com/2026/11/box-office-hunger-games-sunrise-on-the-reaping-monday-1237231975",
  published="2026-11-25T03:00:00+01:00", image="images/hunger-games-sunrise-reaping-monday-record.webp"),

 dict(slug="oldest-compact-quasar-pair-cosmic-dawn", section="science",
  title="Astronomers find oldest known compact quasar pair from cosmic dawn",
  summary="An international team has discovered the most distant compact pair of quasars ever observed, dating to just 900 million years after the Big Bang. The two black holes weigh 1.5 billion and 400 million times the mass of the Sun, and scientists have no definitive explanation for how they grew so large so early. The pair is nicknamed Nāpōwawāʻenakaulua and holds the record for the closest separation between two known early quasars.",
  source="ScienceDaily / NSF NOIRLab", url="https://www.sciencedaily.com/releases/2026/11/261122060342.htm",
  published="2026-11-23T20:00:00+01:00", image="images/oldest-compact-quasar-pair-cosmic-dawn.webp"),

 dict(slug="deere-q4-2026-results-2027-outlook", section="business",
  title="Deere posts $1.05bn quarterly profit but guides 2027 well below forecasts",
  summary="Deere & Co reported fourth-quarter net income of $1.051bn, or $3.89 a share, missing estimates, on revenue down 2% to $12.12bn. For fiscal 2026 net income was $4.86bn on revenue up 4% to $47.7bn. The company guided fiscal 2027 net income to $4.50bn-$5.25bn, including a $250m-$400m pension settlement charge — a midpoint well below Wall Street expectations.",
  source="Deere & Co / MLQ.ai", url="https://mlq.ai/news/deere-forecasts-fiscal-2027-net-income-of-450-billion-to-525-billion-as-north-american-large-ag-demand-starts-to-improve",
  published="2026-11-25T12:15:00+01:00", image="images/deere-q4-2026-results-2027-outlook.webp"),
]


def main():
    with open(DATA, encoding="utf-8") as f:
        doc = json.load(f)
    have = {s["slug"] for s in doc["stories"]}
    added = 0
    for s in NEW:
        if s["slug"] in have:
            print(f"SKIP duplicate: {s['slug']}")
            continue
        s["added"] = NOW
        s["tweetId"] = None
        s["postedToX"] = False
        doc["stories"].append(s)
        added += 1
    doc["edition"] = 17
    doc["updated"] = NOW
    doc["updatedLabel"] = LABEL
    tmp = DATA + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DATA)
    print(f"added {added} stories; edition {doc['edition']}; total {len(doc['stories'])}")


if __name__ == "__main__":
    main()
