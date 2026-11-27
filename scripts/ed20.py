#!/usr/bin/env python3
"""Edition 20 builder: append verified stories, bump edition, sync sw.js."""
import json, os, shutil, subprocess, sys

REPO = "/workspace/repo"
CAND = "/workspace/cand20"
NOW = "2026-11-27T20:10:00+01:00"
LABEL = "27 Nov 2026 · 20:10 WAT"
EDITION = 20

# slug, section, title, summary, source, url, published, photo-file
STORIES = [
 ("us-air-force-cloud-one-breach", "world",
  "Hackers breached the US Air Force's flagship Cloud One platform, Reuters reports",
  "Hackers broke into the US Air Force's Cloud One cloud computing platform, which hosts sensitive tactical, personnel and logistics data, according to a Reuters report citing three sources. Two of the sources said the intrusion was uncovered within the past month during a platform upgrade. It is not yet known who was behind the breach, how far they got, or whether data was taken; plans to migrate more back-office applications to Cloud One have been paused.",
  "Reuters", "https://www.reuters.com/", "2026-11-27T11:20:00+00:00", "cloudone.jpg"),

 ("zelenskyy-warns-major-russian-attack", "world",
  "Zelenskyy warns Russia is preparing another large-scale strike as Trump urges Putin to pull back",
  "Ukrainian President Volodymyr Zelenskyy said in his 26 November evening address that Ukrainian intelligence indicates Russia is completing preparations for another massive strike, and urged citizens to heed missile alerts over the coming days. Possible targets include energy and logistics facilities and infrastructure serving cities. US President Donald Trump said he had urged Vladimir Putin to pull back military aggression in Europe.",
  "Al Jazeera", "https://www.aljazeera.com/news/2026/11/27/zelenskyy-warns-of-major-russian-attack-as-trump-urges-putin-to-pull-back", "2026-11-27T09:00:00+00:00", "zelenskyy.jpg"),

 ("kenya-mackenzie-manslaughter-conviction", "africa",
  "Kenyan cult leader Paul Mackenzie convicted of manslaughter over 123 more deaths",
  "A court in Mombasa found starvation cult leader Paul Nthenge Mackenzie and 29 others guilty of manslaughter over the deaths of 123 followers who were ordered to fast to death in Shakahola forest between 2021 and 2023. Sixty defendants were acquitted. Mackenzie is already serving a 200-year sentence for the murder of 191 people, all but one of them children, handed down earlier this month.",
  "BBC", "https://www.bbc.com/news/articles/cmy49de4xx1zo", "2026-11-27T13:30:00+00:00", "mackenzie.jpg"),

 ("sudan-rsf-attacks-east-darfur-west-kordofan", "africa",
  "At least 14 killed in RSF attacks on Sudan's East Darfur and West Kordofan, rights group says",
  "The Sudan Human Rights Observatory said at least 14 people were killed in attacks by the paramilitary Rapid Support Forces in Sudan's East Darfur and West Kordofan states, with 12 deaths in East Darfur and two in West Kordofan. The group said villages in Yassin locality were subjected to systematic attacks for three consecutive days, and reported separate retaliatory campaigns against West Kordofan residents lasting nearly five days. The RSF did not immediately comment.",
  "Middle East Monitor", "https://www.middleeastmonitor.com/20261127-at-least-14-killed-in-rsf-attacks-on-east-darfur-west-kordofan-sudan-rights-group/", "2026-11-27T13:28:00+00:00", "sudanrsf.jpg"),

 ("kenya-high-court-ebola-quarantine-unconstitutional", "africa",
  "Kenya's High Court rules US-backed Ebola quarantine site breached the constitution",
  "Kenya's High Court ruled that the government violated the constitution by allowing a US-backed Ebola quarantine and treatment facility to be built at Laikipia Air Base near Nanyuki without disclosing the agreement or seeking public input. Justice Patricia Nyaundi ordered further works halted until the government publishes the deal, safety assessments, approvals and patient protocols, and gave authorities 45 days to comply. The 50-bed facility had already housed seven American aid workers.",
  "Al Jazeera", "https://www.aljazeera.com/news/2026/11/26/kenya-govt-violated-constitution-with-ebola-quarantine-site-court-says", "2026-11-26T16:00:00+00:00", "kenyacourt.jpg"),

 ("nigeria-plateau-tafigana-attack-17-killed", "nigeria",
  "Armed men kill 17 villagers in Plateau State as police appeal against reprisals",
  "Armed men killed at least 17 villagers and wounded four in a raid on Tafigana in Bassa Local Government Area of Plateau State, police spokesperson Alfred Alabo said. The attackers opened fire on Wednesday and fled as officers approached. Government spokesperson Joyce Lohya Ramnap appealed to citizens to avoid reprisals, inflammatory statements and the spread of unverified information.",
  "Reuters", "https://www.internazionale.it/ultime-notizie-reuters/2026/11/27/armed-men-kill-17-villagers-in-nigeria-s-plateau-state-police-say", "2026-11-27T12:00:00+00:00", "plateau.jpg"),

 ("nigeria-peter-obi-edo-rally-shooting", "nigeria",
  "Gunmen open fire at Peter Obi's Edo rally, wounding one supporter",
  "Three gunmen in a black Toyota Hilux opened fire along Airport Road in Benin City as supporters gathered to welcome opposition presidential candidate Peter Obi, wounding one man, Aimionkhale Micheal, in the thighs. Edo State police said officers stationed at the airport exit gate prevented the assailants from advancing, and the state CID is investigating. Amnesty International condemned the attack as part of a pattern of violence against opposition supporters.",
  "Punch", "https://punchng.com/one-injured-as-gunmen-attack-obi-supporters-in-benin/", "2026-11-25T18:00:00+00:00", "obi.jpg"),

 ("nigeria-emefiele-naira-redesign-court-witness", "nigeria",
  "Emefiele executed a colour swap instead of the approved naira redesign, investigator tells court",
  "A police investigator told an Abuja High Court that former Central Bank of Nigeria governor Godwin Emefiele approved a colour change of the naira notes rather than the redesign President Muhammadu Buhari had approved. The witness said the initial designs included QR codes, watermarks and different numbering, but the versions produced did not carry QR codes and had no subsequent presidential approval. Emefiele faces four counts including alleged disobedience to lawful directives; he denies the allegations.",
  "Premium Times", "https://www.premiumtimesng.com/news/headlines/928237-emefiele-executed-colour-swap-instead-of-approved-naira-redesign-investigator-tells-court.html", "2026-11-27T08:00:00+00:00", "cbn.jpg"),

 ("nvidia-sp-creditwatch-negative-governance", "business",
  "S&P places Nvidia's AA credit rating on CreditWatch negative over governance risk",
  "S&P Global Ratings said it may cut Nvidia's AA credit rating by one notch after a 90-day review, citing rising management and governance risk following the departure and return of chief executive Jensen Huang. The agency pointed to weak executive oversight, a lack of succession planning and heavy reliance on Huang, and said it was unaware of remedial action by the board. The warning came after Moody's lowered its Nvidia outlook to stable on 18 November.",
  "CNBC", "https://www.cnbc.com/2026/11/26/nvidia-market-governance-risk.html", "2026-11-26T02:57:00+00:00", "nvidia.jpg"),

 ("nigeria-naira-strengthens-ngx-snaps-losing-run", "business",
  "Naira strengthens to N1,387.89 as Nigerian equities snap seven-day losing run",
  "The naira strengthened to N1,387.89 per dollar at the official window while holding at N1,460 in the bureau de change segment, widening the gap between the two rates to 5.20%. The All Share Index rose 0.04% to 244,089.47 points, ending seven consecutive losses, though decliners outnumbered advancers 28 to 21. Stop rates rose at the Treasury Bills auction, with the 364-day rate up 71 basis points to 16.60%.",
  "Proshare", "https://x.com/proshare/status/2126173852875039055", "2026-11-27T09:00:00+00:00", "naira.jpg"),

 ("x-parental-controls-launch", "tech",
  "X launches its first parental controls, 20 years after the platform went live",
  "X began rolling out parental controls for families with teenagers aged 13 to 17, letting parents and guardians see weekly screen time, set daily limits, approve new followers, restrict feed recommendations to accounts a teen already follows, filter words and turn off sensitive media. Accounts belonging to 13-to-17-year-olds are set to protected mode by default. Parents cannot read private messages, see search or viewing history, or post as their teen, and every change is visible to the teenager.",
  "TechCrunch", "https://techcrunch.com/2026/11/26/x-finally-gets-parental-controls-after-20-years", "2026-11-26T19:31:00+00:00", "xparental.jpg"),

 ("bournemouth-celta-vigo-europa-league", "sports",
  "Ten-man Bournemouth come from behind to beat Celta Vigo 2-1 and top the Europa League",
  "Bournemouth extended their winning run to 10 games by coming from a goal down to win 2-1 at Celta Vigo in the Europa League despite playing most of the match with 10 men after Bafode Diakite was sent off in the 23rd minute. Iago Aspas had put Celta ahead on 19 minutes; Alvaro Rodriguez headed the equaliser early in the second half and substitute Rayan fired the winner on 78 minutes. The result takes Bournemouth to the top of the league phase.",
  "ESPN", "https://www.espn.com/soccer/report/_/gameId/401915519", "2026-11-26T22:00:00+00:00", "bournemouth.jpg"),

 ("crystal-palace-real-sociedad-frank-first-win", "sports",
  "Thomas Frank earns first Crystal Palace win as they rally to beat 10-man Real Sociedad 2-1",
  "Crystal Palace came from behind to beat 10-man Real Sociedad 2-1 in the Europa League, handing Thomas Frank his first victory since taking charge. Real Sociedad led through a Job Ochieng pass finished by Sarr, but Palace levelled from the penalty spot after Martin was shown a second yellow for pulling down Jean-Philippe Mateta, and substitute McNeil poked home the winner at the far post. Dean Henderson denied Orri Oskarsson late to preserve the win.",
  "ESPN", "https://www.espn.com/soccer/report/_/gameId/401915504", "2026-11-26T22:00:00+00:00", "palace.jpg"),

 ("alabama-kansas-state-players-era-16", "sports",
  "No. 15 Alabama use balanced scoring to beat Kansas State 104-91 at Players Era 16",
  "Qayden Samuels scored 14 points and led seven Alabama players in double figures as the No. 15 Crimson Tide beat Kansas State 104-91 in a consolation-round game of the Players Era 16 tournament in Las Vegas. Alabama led 51-35 at halftime and by as many as 19. Brock Vice and Brandon Rechsteiner each scored 27 for Kansas State, who fall to 3-4.",
  "AP", "https://apnews.com/article/alabama-kansas-state-score-e1a0355f5416206a77548f6941a92dfe", "2026-11-27T05:16:00+00:00", "alabama.jpg"),

 ("u2-netflix-nfl-thanksgiving-eve-halftime", "entertainment",
  "U2 headline Netflix's first NFL Thanksgiving Eve halftime show at SoFi Stadium",
  "U2 performed the halftime show at the NFL's first Thanksgiving Eve game, a Netflix stream of the Green Bay Packers against the Los Angeles Rams at SoFi Stadium, marking the band's 50th anniversary. Bono sang \"Torn\" from their new album with the late Dolly Parton's voice and image projected on white screens; it was the last song Parton recorded before her death in August. The performance drew comparisons to a Super Bowl-calibre show.",
  "Variety", "https://variety.com/2026/tv/news/netflix-nfl-thanksgiving-eve-u2-1236956485/", "2026-11-26T06:00:00+00:00", "u2.jpg"),

 ("who-measles-deaths-historic-low", "health",
  "Measles deaths fall to a historic low but immunization gaps threaten progress, WHO says",
  "The World Health Organization said worldwide measles deaths are at a historic low, with an estimated 72,000 deaths in 2025, a 91% reduction since 2000, and vaccination estimated to have saved more than 60 million lives over 25 years. The agency warned that coverage remains insufficient and uneven, putting elimination goals at risk. Director-General Tedros Adhanom Ghebreyesus said countries that had eliminated measles are now losing that status.",
  "WHO", "https://www.who.int/news/item/27-11-2026-historic-low-in-measles-deaths--but-immunization-gaps-threaten-progress", "2026-11-27T10:00:00+00:00", "measles.jpg"),

 ("uganda-mrna-ebola-vaccine-trial", "health",
  "Uganda launches mRNA Ebola vaccine trial as DRC outbreak passes 12,000 cases",
  "Uganda launched a trial of an experimental vaccine against the Bundibugyo strain of Ebola, while the global vaccine alliance Gavi said it had bought 1.5 million doses of another candidate. There are currently no approved vaccines or treatments for the Bundibugyo strain behind the outbreak in the Democratic Republic of Congo, which has caused more than 5,900 deaths from over 12,000 cases since May. Two further experimental vaccines were due to begin testing in eastern DRC.",
  "AFP", "https://www.afp.com/en/mrna-ebola-vaccine-trial-launched-uganda", "2026-11-27T12:00:00+00:00", "ebola.jpg"),

 ("homo-erectus-rainforest-china-teeth", "science",
  "Fossil teeth show Homo erectus lived in southern China's rainforests far longer than thought",
  "Proteins preserved in eight Homo erectus teeth from the Baxian and Naxian caves in southern China's Guangxi province show the species lived in tropical rainforest between 324,000 and 184,000 years ago, the youngest securely dated evidence for Homo erectus in mainland China. Chemical traces in the teeth place them in rainforest, a habitat previously thought off limits to any human species before our own. The work, published in Nature, suggests the species persisted on mainland Eurasia longer than previously known.",
  "The Leakey Foundation", "https://leakeyfoundation.org/the-secret-lives-of-our-early-ancestors-revealed-in-fossil-teeth-from-china", "2026-11-26T15:00:00+00:00", "erectus.jpg"),

 ("narwhal-tusk-opposing-spirals-xray", "science",
  "X-ray imaging reveals two opposing microscopic spirals inside the narwhal's tusk",
  "An international team using tensor tomography X-ray imaging found that the narwhal's spiral tusk contains two intertwined microscopic spirals that twist in opposite directions, with the outer path following a left-handed spiral and the inner structure twisting right. The researchers said the opposing arrangement of mineralised collagen fibres keeps the tusk straight while boosting flexibility and resistance to torsion, bending and cracking in Arctic sea ice. The study was published in Nature Communications.",
  "ScienceDaily", "https://www.sciencedaily.com/releases/2026/11/261126063316.htm", "2026-11-27T05:00:00+00:00", "narwhal.jpg"),

 ("pvc-upcycled-synthetic-lubricant-oil", "science",
  "Chemists turn PVC, one of the hardest plastics to recycle, into synthetic lubricant oil",
  "Researchers at Virginia Tech led by chemist and chemical engineer Guoliang Liu converted polyvinyl chloride into polyalphaolefin, a key ingredient in synthetic lubricants such as engine oil, in a process taking about three hours. The method dissolves PVC of the kind used in household plumbing, window frames and credit cards in a solvent, then adds aluminium trichloride and alpha-olefins. Published in Nature, the work offers a potential route for the roughly 40 million tonnes of PVC produced each year.",
  "ScienceDaily", "https://www.sciencedaily.com/releases/2026/11/261126033501.htm", "2026-11-27T05:00:00+00:00", "pvc.jpg"),
]

def main():
    path = os.path.join(REPO, "data", "stories.json")
    d = json.load(open(path))
    have = set(s["slug"] for s in d["stories"])
    added = []
    for slug, section, title, summary, source, url, published, photo in STORIES:
        if slug in have:
            print("SKIP (exists):", slug); continue
        src = os.path.join(CAND, photo)
        if not os.path.exists(src):
            print("MISSING PHOTO:", photo); sys.exit(1)
        dst = os.path.join(REPO, "images", slug + ".webp")
        subprocess.run(["python3", "-c",
            f"from PIL import Image; im=Image.open({src!r}).convert('RGB'); "
            f"im.thumbnail((1600,1600)); im.save({dst!r},'WEBP',quality=82,method=6)"], check=True)
        d["stories"].append({
            "slug": slug, "section": section, "title": title, "summary": summary,
            "source": source, "url": url, "published": published, "added": NOW,
            "image": "images/" + slug + ".webp",
        })
        added.append(slug)
    d["edition"] = EDITION
    d["updated"] = NOW
    d["updatedLabel"] = LABEL
    json.dump(d, open(path, "w"), indent=1, ensure_ascii=False)
    print("added", len(added), "stories; total", len(d["stories"]))

    # bump sw.js
    swp = os.path.join(REPO, "sw.js")
    sw = open(swp).read()
    import re
    sw2 = re.sub(r"jagx-pulse-v5-e\d+", f"jagx-pulse-v5-e{EDITION}", sw)
    open(swp, "w").write(sw2)
    print("sw.js:", re.search(r"jagx-pulse-v5-e\d+", sw2).group(0))

if __name__ == "__main__":
    main()
