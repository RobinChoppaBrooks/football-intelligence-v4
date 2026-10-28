"""evaluate.py  -  scorecard functions shared by every model. Chronological splits, Brier, log loss, calibration, top-N."""
import numpy as np, pandas as pd

def splits(X):
    """train: 2023-24 + 2024-25. valid: 2025-26 Aug-Jan. test: 2025-26 Feb-May (locked). live: 2026-27."""
    k = X.kickoff_utc
    s = pd.Series("train", index=X.index)
    s[(X.season == 2025) & (k < "2026-02-01")] = "valid"
    s[(X.season == 2025) & (k >= "2026-02-01")] = "test"
    s[X.season == 2026] = "live"
    return s

def brier(p, y): return float(np.mean((p - y) ** 2))
def logloss(p, y):
    p = np.clip(p, 1e-6, 1 - 1e-6); return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
def auc(p, y):
    from sklearn.metrics import roc_auc_score
    return float(roc_auc_score(y, p)) if len(np.unique(y)) > 1 else float("nan")

def calibration(p, y, edges=(0, .4, .45, .5, .55, .6, .65, .7, .75, .8, 1.01)):
    b = pd.cut(p, edges, right=False)
    d = pd.DataFrame({"bucket": b, "p": p, "y": y}).groupby("bucket", observed=True).agg(n=("y", "size"), predicted=("p", "mean"), actual=("y", "mean"))
    d["gap_pp"] = (d.actual - d.predicted) * 100
    return d.round(3)

def top_n(df, pcol, ycol="target_over25", ns=(1, 3, 5, 10)):
    """Top-N per calendar day and probability thresholds."""
    d = df.copy(); d["day"] = d.kickoff_utc.dt.date
    rows = []
    for n in ns:
        s = d.sort_values(pcol, ascending=False).groupby("day").head(n)
        rows.append(("top %d/day" % n, len(s), int(s[ycol].sum()), s[ycol].mean(), s[pcol].mean()))
    for t in (.6, .65, .7, .75):
        s = d[d[pcol] >= t]
        rows.append((">= %d%%" % (t * 100), len(s), int(s[ycol].sum()), s[ycol].mean() if len(s) else np.nan, s[pcol].mean() if len(s) else np.nan))
    out = pd.DataFrame(rows, columns=["selection", "n", "hits", "hit_rate", "mean_pred"])
    out["gap_pp"] = (out.hit_rate - out.mean_pred) * 100
    return out.round(3)

def scorecard(df, pcol, ycol="target_over25", by=None):
    y = df[ycol].values; p = df[pcol].values
    base = np.full_like(p, y.mean())
    rows = [("all", len(df), y.mean(), brier(p, y), brier(base, y), logloss(p, y), logloss(base, y), auc(p, y))]
    if by:
        for k, g in df.groupby(by):
            yy, pp = g[ycol].values, g[pcol].values
            if len(g) < 30: continue
            rows.append((str(k), len(g), yy.mean(), brier(pp, yy), brier(np.full_like(pp, yy.mean()), yy), logloss(pp, yy), logloss(np.full_like(pp, yy.mean()), yy), auc(pp, yy)))
    out = pd.DataFrame(rows, columns=["group", "n", "base_rate", "brier", "brier_null", "logloss", "logloss_null", "auc"])
    out["brier_skill"] = 1 - out.brier / out.brier_null
    return out.round(4)
