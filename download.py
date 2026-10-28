"""
download.py  -  Phase 1. Fills football.db. Safe to run any time; every run is incremental and resumable.

  py download.py            everything: fixture lists for all seasons, stats for finished matches, odds for the coming week
  py download.py --no-odds  skip the odds step (historical load only)
  py download.py --results  fixture lists only: last night's results and any new fixtures, about 36 calls, under a minute
  py download.py --results --recent-stats 10   as above plus shots/xG for finished matches in the last 10 days (covered leagues only, ~150 calls)

Stops itself when the day's allowance is nearly used; run again tomorrow and it carries on from the cache.
"""
import sys, json, time
from datetime import datetime, timezone, timedelta
from api import Client
from config import LEAGUES, CUPS, NONLEAGUE, SEASONS, ODDS_DAYS_AHEAD, FINISHED, DEAD

STAT_MAP = {"Total Shots": "shots", "Shots on Goal": "shots_on_target", "Shots off Goal": "shots_off_target",
            "Blocked Shots": "blocked", "Shots insidebox": "shots_inside_box", "Shots outsidebox": "shots_outside_box",
            "Corner Kicks": "corners", "Ball Possession": "possession", "Fouls": "fouls", "Offsides": "offsides",
            "Goalkeeper Saves": "saves", "Total passes": "passes", "Passes %": "pass_accuracy", "expected_goals": "xg"}
STAT_COLS = list(STAT_MAP.values())

def num(v):
    if v is None or v == "": return None
    if isinstance(v, str):
        v = v.strip().rstrip("%")
        try: return float(v)
        except ValueError: return None
    return v

def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def upsert_fixtures(c, rows, league_id, season):
    for f in rows:
        fx, t, sc, lg = f["fixture"], f["teams"], f["score"], f["league"]
        for side in ("home", "away"):
            c.db.execute("INSERT OR IGNORE INTO teams(team_id,name) VALUES(?,?)", (t[side]["id"], t[side]["name"]))
        ht, ft = sc.get("halftime") or {}, sc.get("fulltime") or {}
        c.db.execute("""INSERT INTO fixtures(fixture_id,league_id,season,round,kickoff_utc,home_id,away_id,status,ht_home,ht_away,ft_home,ft_away,updated_at)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                        ON CONFLICT(fixture_id) DO UPDATE SET round=excluded.round, kickoff_utc=excluded.kickoff_utc, status=excluded.status,
                        ht_home=excluded.ht_home, ht_away=excluded.ht_away, ft_home=excluded.ft_home, ft_away=excluded.ft_away, updated_at=excluded.updated_at""",
                     (fx["id"], league_id, season, lg.get("round"), fx["date"], t["home"]["id"], t["away"]["id"], fx["status"]["short"],
                      ht.get("home"), ht.get("away"), ft.get("home"), ft.get("away"), now_iso()))
    c.db.commit()

def step_fixtures(c):
    print("== Fixture lists ==")
    cur = datetime.now(timezone.utc)
    for name, (lid, country) in {**LEAGUES, **CUPS, **NONLEAGUE}.items():
        c.db.execute("INSERT OR IGNORE INTO competitions(league_id,name,country,is_cup) VALUES(?,?,?,?)", (lid, name, country, 1 if name in CUPS else 0))
        for season in SEASONS:
            # past seasons: cached forever. current season: always refetch (statuses and scores change).
            live = season == SEASONS[-1]
            if "--results" in sys.argv and not live: continue
            rows = c.get("fixtures", use_cache=not live, league=lid, season=season)
            if rows: upsert_fixtures(c, rows, lid, season)
            api_name = rows[0]["league"]["name"] if rows else "-"
            print(f"  {name:24s} {season}: {len(rows):4d} fixtures   (API calls it: {api_name})")
    n = c.db.execute("SELECT COUNT(*) FROM fixtures").fetchone()[0]
    print(f"  fixtures table: {n} rows")

def step_stats(c, recent_days=None):
    print("== Fixture statistics (finished matches, leagues with declared coverage) ==")
    recent = "" if recent_days is None else f" AND f.kickoff_utc >= '{(datetime.now(timezone.utc) - timedelta(days=recent_days)).isoformat(timespec='seconds')}'"
    # Rounds the API never has statistics for (learned from the 25 Sep load): FA Cup preliminary and qualifying
    # rounds, and the Scottish Cup / Scottish League Cup outside the last eight. Skipping them saves ~2,500 calls.
    todo = c.db.execute(f"""SELECT f.fixture_id FROM fixtures f JOIN coverage v ON v.league_id=f.league_id AND v.season=f.season
                            WHERE f.status IN ({','.join('?'*len(FINISHED))}) AND f.stats_fetched=0 AND v.cov_stats_fixtures=1
                              AND NOT (f.league_id=45 AND (f.round LIKE '%Preliminary%' OR f.round LIKE '%Qualifying%'))
                              AND NOT (f.league_id IN (181,185) AND f.round NOT IN ('Quarter-finals','Semi-finals','Final')){recent}
                            ORDER BY f.season DESC, f.kickoff_utc""", FINISHED).fetchall()
    print(f"  {len(todo)} matches to fetch")
    done = 0
    for (fid,) in todo:
        try:
            rows = c.get("fixtures/statistics", fixture=fid)
        except RuntimeError as e:
            print(f"  {e}"); break
        if not rows:
            c.db.execute("UPDATE fixtures SET stats_fetched=-1 WHERE fixture_id=?", (fid,))   # -1 = API has nothing; don't retry
        else:
            for team in rows:
                vals = {k: None for k in STAT_COLS}
                for s in team.get("statistics", []):
                    col = STAT_MAP.get(s["type"])
                    if col: vals[col] = num(s["value"])
                c.db.execute(f"INSERT OR REPLACE INTO fixture_stats(fixture_id,team_id,{','.join(STAT_COLS)},fetched_at) VALUES(?,?,{','.join('?'*len(STAT_COLS))},?)",
                             (fid, team["team"]["id"], *[vals[k] for k in STAT_COLS], now_iso()))
            c.db.execute("UPDATE fixtures SET stats_fetched=1 WHERE fixture_id=?", (fid,))
        done += 1
        if done % 100 == 0:
            c.db.commit(); print(f"  {done}/{len(todo)}  (remaining today: {c.remaining})")
    c.db.commit()
    print(f"  fetched {done}")

def step_odds(c):
    print(f"== Pre-match odds, fixtures in the next {ODDS_DAYS_AHEAD} days ==")
    lo, hi = now_iso(), (datetime.now(timezone.utc) + timedelta(days=ODDS_DAYS_AHEAD)).isoformat(timespec="seconds")
    todo = c.db.execute("""SELECT f.fixture_id FROM fixtures f JOIN coverage v ON v.league_id=f.league_id AND v.season=f.season
                           WHERE f.status='NS' AND f.kickoff_utc BETWEEN ? AND ? AND v.cov_odds=1 ORDER BY f.kickoff_utc""", (lo, hi)).fetchall()
    print(f"  {len(todo)} fixtures")
    for (fid,) in todo:
        try:
            rows = c.get("odds", use_cache=False, fixture=fid)     # prices move; always refetch, keep latest per bookmaker
        except RuntimeError as e:
            print(f"  {e}"); break
        for o in rows:
            for bk in o.get("bookmakers", []):
                rec = {"over25": None, "under25": None, "btts_yes": None, "btts_no": None}
                for bet in bk.get("bets", []):
                    nm = bet.get("name", "")
                    if nm == "Goals Over/Under":
                        for v in bet["values"]:
                            if v["value"] == "Over 2.5": rec["over25"] = num(v["odd"])
                            if v["value"] == "Under 2.5": rec["under25"] = num(v["odd"])
                    elif nm == "Both Teams Score":
                        for v in bet["values"]:
                            if v["value"] == "Yes": rec["btts_yes"] = num(v["odd"])
                            if v["value"] == "No": rec["btts_no"] = num(v["odd"])
                if any(rec.values()):
                    c.db.execute("INSERT OR REPLACE INTO fixture_odds VALUES(?,?,?,?,?,?,?,?,?)",
                                 (fid, bk["id"], bk["name"], rec["over25"], rec["under25"], rec["btts_yes"], rec["btts_no"], o.get("update"), now_iso()))
        if rows: c.db.execute("UPDATE fixtures SET odds_fetched=1 WHERE fixture_id=?", (fid,))
    c.db.commit()

def step_extras(c, days):
    """Odds (every market, every bookmaker the API returns) and injuries for NS fixtures in the next `days` days,
    competitions named in extras_comps.txt (config.py names, one per line). One odds call plus one injuries call per fixture."""
    from config import LEAGUES, CUPS, NONLEAGUE
    allc = {**LEAGUES, **CUPS, **NONLEAGUE}
    names = [l.strip() for l in open("extras_comps.txt", encoding="utf-8") if l.strip() and not l.startswith("#")]
    lids = [allc[n][0] for n in names if n in allc]
    lo, hi = now_iso(), (datetime.now(timezone.utc) + timedelta(days=days)).isoformat(timespec="seconds")
    todo = c.db.execute(f"SELECT fixture_id FROM fixtures WHERE status='NS' AND kickoff_utc BETWEEN ? AND ? AND league_id IN ({','.join('?'*len(lids))}) ORDER BY kickoff_utc", (lo, hi, *lids)).fetchall()
    print(f"== Extras: odds + injuries for {len(todo)} fixtures in the next {days} days ({len(lids)} competitions) ==")
    for (fid,) in todo:
        try:
            rows = c.get("odds", use_cache=False, fixture=fid)
            for o in rows:
                for bk in o.get("bookmakers", []):
                    for bet in bk.get("bets", []):
                        for v in bet.get("values", []):
                            c.db.execute("INSERT OR REPLACE INTO market_odds VALUES(?,?,?,?,?,?)", (fid, bk["name"], bet.get("name", ""), str(v.get("value")), num(v.get("odd")), now_iso()))
            inj = c.get("injuries", use_cache=False, fixture=fid)
            for i in inj:
                c.db.execute("INSERT OR REPLACE INTO injuries VALUES(?,?,?,?,?,?,?)",
                             (fid, i["team"]["id"], i["player"]["id"], i["player"]["name"], i["player"].get("type"), i["player"].get("reason"), now_iso()))
        except RuntimeError as e:
            print(f"  {e}"); break
        c.db.commit()
    print(f"  done")

def summary(c):
    print("== Store ==")
    for r in c.db.execute("""SELECT cp.name, f.season, COUNT(*), SUM(f.status IN ('FT','AET','PEN')), SUM(f.stats_fetched=1), SUM(f.odds_fetched=1)
                             FROM fixtures f JOIN competitions cp ON cp.league_id=f.league_id GROUP BY cp.name, f.season ORDER BY cp.name, f.season"""):
        print(f"  {r[0]:24s} {r[1]}  fixtures {r[2]:4d}  finished {r[3]:4d}  stats {r[4]:4d}  odds {r[5]:3d}")
    xg = c.db.execute("SELECT COUNT(*) FROM fixture_stats WHERE xg IS NOT NULL").fetchone()[0]
    print(f"  fixture_stats rows with xG: {xg}")

def main():
    c = Client()
    if c.db.execute("SELECT COUNT(*) FROM coverage").fetchone()[0] == 0:
        sys.exit("coverage table is empty: run  py probe.py  first.")
    t0 = time.time()
    try:
        if "--extras-only" not in sys.argv: step_fixtures(c)
        if "--extras" in sys.argv:
            step_extras(c, int(sys.argv[sys.argv.index("--extras") + 1]))
        if "--results" in sys.argv:
            if "--recent-stats" in sys.argv:
                step_stats(c, recent_days=int(sys.argv[sys.argv.index("--recent-stats") + 1]))
            else:
                print("results-only run: skipping statistics and odds")
        else:
            step_stats(c)
            if "--no-odds" not in sys.argv: step_odds(c)
    finally:
        summary(c)
        print(f"API calls this run: {c.calls_this_run}   remaining today: {c.remaining}   {time.time()-t0:.0f}s")
        c.close()

if __name__ == "__main__":
    main()
