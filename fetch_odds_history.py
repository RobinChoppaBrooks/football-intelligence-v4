"""
fetch_odds_history.py  -  research only (19 Nov 2026). Downloads football-data.co.uk results-and-odds CSVs for Rob's leagues,
seasons 2023-24 to 2026-27, into data/research_odds/. Used to score strategies against real historical Over 2.5 prices.
Never a selection input. Run from GitHub Actions ("fetch-odds" hand run) because the Claude sandbox cannot reach the site.
"""
import os, sys, time, urllib.request
CODES = {"E0": "Premier League", "E1": "Championship", "E2": "League One", "E3": "League Two", "EC": "National League",
         "D1": "Bundesliga", "N1": "Eredivisie", "F1": "Ligue 1", "T1": "Super Lig", "SC0": "Scottish Premiership",
         "SP1": "La Liga", "P1": "Primeira Liga"}
SEASONS = ["2324", "2425", "2526", "2627"]
OUT = "data/research_odds"
os.makedirs(OUT, exist_ok=True)
ok = 0
for s in SEASONS:
    for code in CODES:
        url = f"https://www.football-data.co.uk/mmz4281/{s}/{code}.csv"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 football-v4-research"})
            data = urllib.request.urlopen(req, timeout=60).read()
            open(f"{OUT}/{s}_{code}.csv", "wb").write(data); ok += 1
            print(f"{s} {code}: {len(data)} bytes")
        except Exception as e:
            print(f"{s} {code}: failed {e}")
        time.sleep(1)
print(f"{ok} files")
