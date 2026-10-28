"""
btts.py  -  Both Teams To Score model, same recipe as bands.py (GBM on last-5 league / venue-3 counts, league rate).
Train 2023-24 + 2024-25, validate 2025-26. Likelihood bands set from validation deciles:
HIGH = top band where actual BTTS >= 0.60, MEDIUM = actual >= 0.52, LOW below. Verdict YES = HIGH or MEDIUM.

    python3 btts.py features.pkl   -> writes btts_model.pkl
"""
import sys, pickle, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from evaluate import brier, logloss, auc, calibration
from bands import FEATS

def fit(X):
    X = X[X.target_btts.notna()].copy()
    tr = X[X.season.isin([2023, 2024])]; va = X[X.season == 2025]
    m = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.04, max_iter=300, min_samples_leaf=80, l2_regularization=1.0, random_state=0)
    m.fit(tr[FEATS].astype(float), tr.target_btts.values)
    p = m.predict_proba(va[FEATS].astype(float))[:, 1]; y = va.target_btts.values
    base = va.lg_btts.fillna(tr.target_btts.mean()).values
    print(f"league_rate_only brier {brier(base, y):.4f} logloss {logloss(base, y):.4f} auc {auc(base, y):.3f}")
    print(f"gbm              brier {brier(p, y):.4f} logloss {logloss(p, y):.4f} auc {auc(p, y):.3f}\n")
    print(calibration(p, y).to_string())
    va = va.assign(p=p)
    q = va.assign(b=pd.qcut(va.p, 10, labels=False, duplicates="drop")).groupby("b").agg(n=("target_btts", "size"), pmin=("p", "min"), actual=("target_btts", "mean"))
    print("\nvalidation deciles:"); print(q.round(3).to_string())
    high = q[q.actual >= 0.60].pmin.min(); med = q[q.actual >= 0.52].pmin.min()
    print(f"\ncut points: HIGH p >= {high:.3f}, MEDIUM p >= {med:.3f}")
    for lab, lo, hi in (("HIGH", high, 2), ("MEDIUM", med, high), ("LOW", 0, med)):
        s = va[(va.p >= lo) & (va.p < hi)]; print(f"  {lab:6s} n={len(s):5d} actual btts {s.target_btts.mean():.3f}")
    pickle.dump({"model": ("gbm", m), "feats": FEATS, "high": float(high), "medium": float(med)}, open("btts_model.pkl", "wb"))

def predict(bundle, X): return bundle["model"][1].predict_proba(X[bundle["feats"]].astype(float))[:, 1]
def label(bundle, p): return "HIGH" if p >= bundle["high"] else "MEDIUM" if p >= bundle["medium"] else "LOW"

if __name__ == "__main__":
    fit(pd.read_pickle(sys.argv[1]))
