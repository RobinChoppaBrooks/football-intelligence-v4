"""
log_prices.py  -  pre-match Over 2.5 prices for the selected fixtures of one run (19 Nov 2026, Rob approved).

    python log_prices.py RUN_ID

Research and tracking only. Prices are never used to select or rank fixtures and never appear in the reports Rob picks from.
For every High / Medium (incl. report Weak) / trump card fixture of the run that has not kicked off: one API odds call,
every bookmaker's Over 2.5 / Under 2.5 price stored in football.db (fixture_odds, latest per bookmaker) and appended to
data/prices/prices_log.csv (one row per fixture per bookmaker per fetch; earlier rows are never edited).
The V1 value rule (pre-registered 19 Nov 2026, docs/research/value_test_2026-11-19) is flagged per fixture:
v1 = best price x model score >= 1.00. value_tracker.py scores it once results are in.
"""
import os, sys, csv
from datetime import datetime, timezone
import pandas as pd

LOG = "data/predictions/predictions_log.csv"
OUT = "data/prices/prices_log.csv"
COLS = ["run_id", "fetched_at", "fixture_id", "kickoff_uk", "competition", "home", "away", "classification", "trump",
        "model_score", "bookmaker", "over25", "under25", "best_over25", "best_bookmaker", "b365_over25", "v1"]

def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None

def parse(rows):
    """API odds response -> {bookmaker: (over25, under25)}"""
    out = {}
    for o in rows:
        for bk in o.get("bookmakers", []):
            ov = un = None
            for bet in bk.get("bets", []):
                if bet.get("name") == "Goals Over/Under":
                    for v in bet.get("values", []):
                        if v.get("value") == "Over 2.5": ov = num(v.get("odd"))
                        if v.get("value") == "Under 2.5": un = num(v.get("odd"))
            if ov: out[(bk.get("id"), bk.get("name"))] = (ov, un, o.get("update"))
    return out

def selected(run_id):
    p = pd.read_csv(LOG, dtype={"run_id": str})
    p = p[p.run_id == run_id]
    tr = p.trump.astype(str).str.lower().isin(["1", "true"])
    return p[(p.classification.isin(["High", "Medium", "Weak"])) | tr].assign(trump=tr.astype(int))

def main(run_id, client=None):
    sel = selected(run_id)
    if sel.empty: print(f"no selected fixtures for run {run_id}"); return 0
    if client is None:
        from api import Client
        client = Client()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    new = not os.path.exists(OUT)
    done = 0
    with open(OUT, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if new: w.writeheader()
        for r in sel.itertuples():
            st = client.db.execute("SELECT status FROM fixtures WHERE fixture_id=?", (int(r.fixture_id),)).fetchone()
            if st and st[0] != "NS": continue
            try:
                prices = parse(client.get("odds", use_cache=False, fixture=int(r.fixture_id)))
            except RuntimeError as e:
                print(f"  {e}"); break
            if not prices: continue
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            best_k = max(prices, key=lambda k: prices[k][0]); best = prices[best_k][0]
            b365 = next((v[0] for k, v in prices.items() if k[1] == "Bet365"), None)
            v1 = int(best * float(r.model_score) >= 1.0)
            for (bid, bname), (ov, un, upd) in prices.items():
                client.db.execute("INSERT OR REPLACE INTO fixture_odds VALUES(?,?,?,?,?,?,?,?,?)", (int(r.fixture_id), bid, bname, ov, un, None, None, upd, now))
                w.writerow(dict(run_id=run_id, fetched_at=now, fixture_id=int(r.fixture_id), kickoff_uk=r.kickoff_uk, competition=r.competition,
                                home=r.home, away=r.away, classification=r.classification, trump=r.trump, model_score=r.model_score,
                                bookmaker=bname, over25=ov, under25=un, best_over25=best, best_bookmaker=best_k[1], b365_over25=b365, v1=v1))
            client.db.execute("UPDATE fixtures SET odds_fetched=1 WHERE fixture_id=?", (int(r.fixture_id),))
            done += 1
        client.db.commit()
    print(f"prices logged for {done} of {len(sel)} selected fixtures (run {run_id}); API calls {getattr(client, 'calls_this_run', '?')}")
    return done

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    main(sys.argv[1])
