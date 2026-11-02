"""
download_events.py  -  goal events for the research watchlists (2 Nov 2026). Research only: nothing here touches the
model, the classifications or the prediction log. Run by ci/run.sh after download.py --results; incremental.

Fetches API-Football events for each team's last N completed league matches (default 10) in Rob's 14 priority leagues,
season 2026, and stores them in fixture_events (schema already in store.py). Uses api.Client, so every call is cached in
api_cache and logged in api_log, and a re-run only fetches what is missing.

Calls: the fixtures endpoint accepts up to 20 ids per request and returns events for each, so ~1,400 fixtures cost ~71
calls. If a batch comes back without an events block the script falls back to fixtures/events, one call per fixture.

    py download_events.py                 last 10 league games per team, 14 leagues
    py download_events.py --last 10 --leagues 39,40,41   (override)
    py download_events.py --dry-run       count only, no API calls

Runs in GitHub Actions (APISPORTS_KEY) or on the PC next to football.db and apisports_key.txt.
"""
import sys, sqlite3, json, argparse
from datetime import datetime, timezone

PRIORITY_14 = [39, 40, 41, 42, 43, 50, 51, 78, 88, 61, 203, 179, 140, 94]   # Rob's 14 leagues (config/competitions.json)
FINISHED = ("FT", "AET", "PEN")
SEASON = 2026

def fixture_set(db, leagues, last_n):
    q = f"""SELECT fixture_id, league_id, kickoff_utc, home_id, away_id FROM fixtures
            WHERE season=? AND league_id IN ({','.join('?'*len(leagues))}) AND status IN ({','.join('?'*len(FINISHED))})
            ORDER BY kickoff_utc"""
    rows = db.execute(q, (SEASON, *leagues, *FINISHED)).fetchall()
    by_team = {}
    for fid, lg, ko, h, a in rows:
        by_team.setdefault(h, []).append(fid); by_team.setdefault(a, []).append(fid)
    wanted = set()
    for t, fids in by_team.items(): wanted.update(fids[-last_n:])
    return sorted(wanted)

def store_events(db, fid, events):
    db.execute("DELETE FROM fixture_events WHERE fixture_id=?", (fid,))
    for i, e in enumerate(events):
        t = e.get("time") or {}; team = e.get("team") or {}
        db.execute("INSERT OR REPLACE INTO fixture_events(fixture_id,seq,minute,extra,team_id,type,detail) VALUES(?,?,?,?,?,?,?)",
                   (fid, i, t.get("elapsed"), t.get("extra"), team.get("id"), e.get("type"), e.get("detail")))
    db.execute("UPDATE fixtures SET events_fetched=? WHERE fixture_id=?", (1 if events else -1, fid))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--last", type=int, default=10); ap.add_argument("--leagues", default=",".join(map(str, PRIORITY_14)))
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--batch", type=int, default=20)
    ap.add_argument("--db", default="football.db")
    a = ap.parse_args()
    leagues = [int(x) for x in a.leagues.split(",")]
    db = sqlite3.connect(a.db)
    from store import ensure_schema; ensure_schema(db)
    wanted = fixture_set(db, leagues, a.last)
    have = {r[0] for r in db.execute("SELECT fixture_id FROM fixtures WHERE events_fetched<>0")}
    todo = [f for f in wanted if f not in have]
    print(f"{len(wanted)} fixtures in the last-{a.last} set across {len(leagues)} leagues; {len(todo)} still to fetch; "
          f"about {-(-len(todo)//a.batch)} calls in batches of {a.batch}")
    if a.dry_run or not todo: return
    db.close()
    from api import Client
    c = Client(a.db)
    fetched = fallback = 0
    for i in range(0, len(todo), a.batch):
        ids = todo[i:i + a.batch]
        try:
            rows = c.get("fixtures", ids="-".join(map(str, ids)))
        except RuntimeError as e:
            print(f"  {e}"); break
        got = {}
        for r in rows or []:
            fid = (r.get("fixture") or {}).get("id")
            if fid is not None and "events" in r: got[fid] = r["events"] or []
        for fid in ids:
            if fid in got:
                store_events(c.db, fid, got[fid]); fetched += 1
            else:   # batch response without an events block: one call for this fixture
                try:
                    ev = c.get("fixtures/events", fixture=fid)
                except RuntimeError as e:
                    print(f"  {e}"); c.db.commit(); return
                store_events(c.db, fid, ev or []); fetched += 1; fallback += 1
        c.db.commit()
        print(f"  {fetched}/{len(todo)} stored (fallback calls {fallback}, remaining today {c.remaining})")
    n_ev = c.db.execute("SELECT COUNT(*) FROM fixture_events").fetchone()[0]
    n_fx = c.db.execute("SELECT COUNT(*) FROM fixtures WHERE events_fetched=1").fetchone()[0]
    n_none = c.db.execute("SELECT COUNT(*) FROM fixtures WHERE events_fetched=-1").fetchone()[0]
    print(f"done: {fetched} fixtures this run, {c.calls_this_run} API calls; fixture_events now holds {n_ev} rows for {n_fx} fixtures; {n_none} fixtures with no events at the API")

if __name__ == "__main__":
    main()
