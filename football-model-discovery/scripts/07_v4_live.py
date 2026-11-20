"""07_v4_live.py - compare against the V4.1 predictions actually published (data/predictions/predictions_log.csv, results from
data/results/results_log.csv). Read-only. Checks the historical V4 reconstruction against the logged model_score, then
compares, on the identical published fixtures, V4.1's own selections with the best challenger taking the same number
per run. Live log fixtures fall inside the test season, which no challenger was tuned on."""
import numpy as np, pandas as pd
import lab, families as F

REPO = lab.ROOT.rsplit("/", 1)[0]
P = pd.read_csv(f"{REPO}/data/predictions/predictions_log.csv")
Rz = pd.read_csv(f"{REPO}/data/results/results_log.csv")
P = P[P.league_id.isin(lab.LEAGUE_NAMES)].drop_duplicates(["run_id", "fixture_id"])
X = lab.load()
ALL = lab.universe(X, lab.DEV + lab.VAL + lab.TEST)
tr = ALL[ALL.season.isin(lab.DEV + lab.VAL)]
Te = X[X.season == 2026].copy()
Te["f11_rf"] = F.f11_rf(tr, Te)
M = P.merge(Te[["fixture_id", "y", "status", "v4_score", "f11_rf", "eligible"]], on="fixture_id", how="inner")
diff = (M.model_score - M.v4_score).abs()
print(f"published rows in Rob's 14 leagues with a result in the database: {len(M)} (runs {M.run_id.nunique()})")
print(f"reconstruction check: |logged model_score - recomputed V4.1 score| <= 0.001 for {(diff <= 0.001).sum()} of {len(M)}; max gap {diff.max():.3f}")
M = M[M.status == "FT"]
# a fixture published in two runs (e.g. weekend 29 and 30 Oct) is counted once: the latest run before kick-off
M = M.sort_values("generated_at").drop_duplicates("fixture_id", keep="last")
print(f"unique finished fixtures after de-duplicating repeat runs: {len(M)}")
M["v4_selected"] = M.classification.isin(["High", "Medium"]) | (M.get("trump", 0) == 1)
out = []
for run, g in M.groupby("run_id"):
    k = int(g.v4_selected.sum())
    ch = g.sort_values(["f11_rf", "fixture_id"], ascending=[False, True]).head(k)
    out.append({"run_id": run, "fixtures": len(g), "v4_selected": k, "v4_won": int(g.y[g.v4_selected].sum()), "rf_same_count_won": int(ch.y.sum()),
                "overlap": int(len(set(ch.fixture_id) & set(g.fixture_id[g.v4_selected])))})
O = pd.DataFrame(out); O.to_csv(f"{lab.ROOT}/results/v4_live_comparison.csv", index=False)
print(O.to_string()); print(O[["fixtures", "v4_selected", "v4_won", "rf_same_count_won", "overlap"]].sum())
hi = M[M.classification == "High"]; md = M[M.classification == "Medium"]; rj = M[M.classification == "rejected"]
print(f"published High {int(hi.y.sum())} of {len(hi)}, Medium {int(md.y.sum())} of {len(md)}, rejected {int(rj.y.sum())} of {len(rj)}")
