"""
value_tracker.py  -  scores the pre-registered V1 value rule (19 Nov 2026). Research only, never a selection input.

    python value_tracker.py [football.db]

V1: model High or Medium (incl. report Weak, trump card) AND best pre-match price x model score >= 1.00, level £1 singles at the
best price. Uses the last price fetched before kick-off per fixture from data/prices/prices_log.csv; a fixture counts once
(its first run). Only FT results count (not AET/PEN; abandoned, awarded, void excluded). Writes data/prices/v1_tracker.md.
Judged only after 300 qualifying bets; no thresholds are changed on what it shows.
"""
import os, sys, sqlite3
import pandas as pd

IN, OUT, JUDGE = "data/prices/prices_log.csv", "data/prices/v1_tracker.md", 300

def main(db="football.db"):
    if not os.path.exists(IN): print("no prices logged yet"); return
    p = pd.read_csv(IN)
    c = sqlite3.connect(db)
    fx = pd.read_sql("select fixture_id, kickoff_utc, status, ft_home, ft_away from fixtures", c).set_index("fixture_id")
    p = p.join(fx, on="fixture_id")
    p = p[pd.to_datetime(p.fetched_at, utc=True) < pd.to_datetime(p.kickoff_utc, utc=True)]
    first_run = p.groupby("fixture_id").run_id.first()
    p = p[p.run_id == p.fixture_id.map(first_run)]
    last = p.sort_values("fetched_at").groupby("fixture_id").tail(1).copy()       # one row per fixture: latest pre-kick-off fetch
    last["v1"] = (last.best_over25 * last.model_score >= 1.0)
    done = last[last.status == "FT"].copy()
    done["hit"] = (done.ft_home + done.ft_away) >= 3
    lines = ["# V1 value rule tracker (research only)", "",
             "Rule, pre-registered 19 Nov 2026: High or Medium AND best price x model score >= 1.00, £1 singles at the best price.",
             f"Judge only after {JUDGE} qualifying bets. Counts and units, no percentages.", "",
             "| Group | Bets | Hits | P/L at best price (units) | P/L at Bet365 (units) |", "|---|---|---|---|---|"]
    def row(lab, d):
        b = d[d.b365_over25.notna()]
        return f"| {lab} | {len(d)} | {int(d.hit.sum())} | {round(float((d.best_over25 * d.hit - 1).sum()), 2)} | {round(float((b.b365_over25 * b.hit - 1).sum()), 2)} (on {len(b)}) |"
    lines += [row("V1 qualifying", done[done.v1]), row("All selected with a price", done), row("Selected, not V1", done[~done.v1])]
    lines += ["", f"Fixtures priced: {len(last)}; settled: {len(done)}; V1 qualifying awaiting results: {int((last.v1 & (last.status != 'FT')).sum())}.",
              f"Progress to judgement: {int(done.v1.sum())} of {JUDGE} V1 bets settled."]
    os.makedirs(os.path.dirname(OUT), exist_ok=True); open(OUT, "w").write("\n".join(lines) + "\n"); print("\n".join(lines))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "football.db")
