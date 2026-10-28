"""
review.py  -  scores predictions_log.csv against results and reports Over 2.5 and BTTS performance separately.

    python3 review.py football.db [--since YYYY-MM-DD]

Fills score / over25_result / btts_result for played fixtures, then prints hit rates by confidence, BTTS likelihood,
competition, goal pattern and catch presence. Zero API calls.
"""
import sys, os, sqlite3, argparse, pandas as pd

ap = argparse.ArgumentParser(); ap.add_argument("db"); ap.add_argument("--since", default=None)
a = ap.parse_args()
logp = os.path.join(os.path.dirname(os.path.abspath(a.db)), "predictions_log.csv")
log = pd.read_csv(logp)
c = sqlite3.connect(a.db)
fx = pd.read_sql("select fixture_id, status, ft_home, ft_away from fixtures", c).set_index("fixture_id")
played = fx[fx.status.isin(["FT", "AET", "PEN"])]
m = log.fixture_id.isin(played.index)
log.loc[m, "score"] = log.loc[m, "fixture_id"].map(lambda i: f"{int(played.ft_home[i])}-{int(played.ft_away[i])}")
log.loc[m, "over25_result"] = log.loc[m, "fixture_id"].map(lambda i: "Y" if played.ft_home[i] + played.ft_away[i] >= 3 else "N")
log.loc[m, "btts_result"] = log.loc[m, "fixture_id"].map(lambda i: "Y" if played.ft_home[i] > 0 and played.ft_away[i] > 0 else "N")
log.to_csv(logp, index=False)

d = log[log.over25_result.isin(["Y", "N"])].copy()
if a.since: d = d[d.run_date >= a.since]
if d.empty: print("no played fixtures in the log yet"); sys.exit()
d["o"] = (d.over25_result == "Y").astype(int); d["b"] = (d.btts_result == "Y").astype(int)
d["has_catch"] = d.catch.fillna("").str.len() > 0
def table(col, target, label):
    t = d.groupby(col)[target].agg(hit="sum", n="size"); t["rate"] = (t.hit / t.n).round(2)
    print(f"\n{label} by {col}:"); print(t.to_string())
print(f"{len(d)} played fixtures, runs {d.run_date.min()} to {d.run_date.max()}")
print(f"\nOVER 2.5: shown {d[d.over25=='YES'].o.mean():.2f} (n={int((d.over25=='YES').sum())}), rejected {d[d.over25=='NO'].o.mean():.2f} (n={int((d.over25=='NO').sum())})")
table("confidence", "o", "Over 2.5")
table("pattern", "o", "Over 2.5")
table("has_catch", "o", "Over 2.5 (shown only)") if False else None
s = d[d.over25 == "YES"]
print("\nOver 2.5, shown fixtures, by catch present:"); print(s.groupby("has_catch").o.agg(hit="sum", n="size").assign(rate=lambda t: (t.hit / t.n).round(2)).to_string())
print("\nOver 2.5, shown fixtures, by competition:")
print(s.groupby("comp").o.agg(hit="sum", n="size").assign(rate=lambda t: (t.hit / t.n).round(2)).sort_values("n", ascending=False).to_string())
print(f"\nBTTS: YES {d[d.btts=='YES'].b.mean():.2f} (n={int((d.btts=='YES').sum())}), NO {d[d.btts=='NO'].b.mean():.2f} (n={int((d.btts=='NO').sum())})")
table("btts_likelihood", "b", "BTTS")
table("pattern", "b", "BTTS")
