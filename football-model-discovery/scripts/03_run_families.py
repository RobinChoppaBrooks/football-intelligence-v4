"""03_run_families.py - score every family walk-forward on 2024-25 (train 2023-24) and 2025-26 (train 2023-24 + 2024-25).
The test season is NOT scored here. Output: results/family_scores_wf.parquet, results/families_validation.csv"""
import time, numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
import lab, families as F

X = lab.load()
rows, scores = [], []
PROB = ("f6", "f9", "f10", "f11", "v4")
for season, train_seasons in ((2024, [2023]), (2025, [2023, 2024])):
    tr = lab.universe(X, train_seasons); ap = lab.universe(X, [season]).copy()
    S = ap[["fixture_id", "season", "league_id", "window", "y", "v4_score"]].copy()
    for f in F.COUNT_RULES + F.FITTED:
        t = time.time(); S[f.__name__] = np.asarray(f(tr, ap), float)
        print(f"{season} {f.__name__:20s} {time.time()-t:5.1f}s", flush=True)
    S["v4"] = S.v4_score
    scores.append(S)
S = pd.concat(scores, ignore_index=True)
S.to_parquet(f"{lab.ROOT}/results/family_scores_wf.parquet")

names = [f.__name__ for f in F.COUNT_RULES + F.FITTED] + ["v4"]
for season, g in S.groupby("season"):
    for nm in names:
        r = {"season": lab.SEASON_NAMES[season], "model": nm, "family": F.family(nm), "eligible": len(g), "base_won": int(g.y.sum())}
        r["auc"] = round(roc_auc_score(g.y, g[nm]), 4)
        if nm.startswith(PROB):
            r["brier"] = round(lab.brier(g[nm].values, g.y.values), 4); r["logloss"] = round(lab.logloss(g[nm].values, g.y.values), 4)
        for k in (5, 10, 15, 20):
            m = lab.topk_per_window(g, nm, k); r[f"top{k}_sel"] = int(m.sum()); r[f"top{k}_won"] = int(g.y[m].sum())
        for q in (10, 20, 33):
            thr = g[nm].quantile(1 - q / 100); m = g[nm] >= thr
            r[f"top{q}pct_sel"] = int(m.sum()); r[f"top{q}pct_won"] = int(g.y[m].sum())
        if nm == "v4" and season == 2024:
            r["note"] = "V4.1 trained on this season (in-sample)"
        rows.append(r)
R = pd.DataFrame(rows)
R.to_csv(f"{lab.ROOT}/results/families_validation.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
print(R[["season", "model", "auc", "brier", "logloss", "top5_won", "top10_won", "top20_won", "top20_sel", "top10pct_won", "top10pct_sel"]].to_string())
