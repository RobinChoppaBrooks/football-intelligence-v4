"""
bands.py  -  learns the traffic-light rule from the prompt's own evidence (last 5 league games this season, venue 3,
attack-vs-defence counts, league scoring rate) and validates it walk-forward. Goals only, so it applies to every tier.

    python3 bands.py features.pkl        -> prints validation calibration and the green/amber cut points; writes bands_model.pkl

Train: seasons 2023-24 and 2024-25. Validate: 2025-26 (never seen in training). Every feature is from before kickoff.
"""
import sys, pickle, numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from evaluate import brier, logloss, auc, calibration

FEATS = ["h_l5L_gf", "h_l5L_ga", "a_l5L_gf", "a_l5L_ga", "h_l5L_over25", "a_l5L_over25", "h_l5L_btts", "a_l5L_btts",
         "h_l5L_gf2", "h_l5L_ga2", "a_l5L_gf2", "a_l5L_ga2", "h_l5L_cs", "a_l5L_cs", "h_l5L_fts", "a_l5L_fts",
         "h_l5L_tot", "a_l5L_tot", "h_l5L_tot4", "a_l5L_tot4", "h_l5L_maxtot", "a_l5L_maxtot", "h_l5L_n", "a_l5L_n",
         "h_v3L_gf", "h_v3L_ga", "a_v3L_gf", "a_v3L_ga", "h_v3L_tot", "a_v3L_tot", "h_v3L_over25", "a_v3L_over25", "h_v3L_n", "a_v3L_n",
         "lg_o25", "lg_tot", "lg_n", "is_cup"]

def fit(X):
    X = X[X.target_over25.notna()].copy()
    tr = X[X.season.isin([2023, 2024])]; va = X[X.season == 2025]
    y_tr, y_va = tr.target_over25.values, va.target_over25.values
    models = {
        "league_rate_only": None,
        "logistic": LogisticRegression(max_iter=2000, C=0.3),
        "gbm": HistGradientBoostingClassifier(max_depth=3, learning_rate=0.04, max_iter=300, min_samples_leaf=80, l2_regularization=1.0, random_state=0),
    }
    out = {}
    for name, m in models.items():
        if m is None:
            p = va.lg_o25.fillna(tr.target_over25.mean()).values
        else:
            A = tr[FEATS].astype(float); B = va[FEATS].astype(float)
            if name == "logistic":
                med = A.median(); A = A.fillna(med); B = B.fillna(med)
                mu, sd = A.mean(), A.std().replace(0, 1); A = (A - mu) / sd; B = (B - mu) / sd
                m.fit(A, y_tr); p = m.predict_proba(B)[:, 1]
                models[name] = ("logistic", m, med, mu, sd)
            else:
                m.fit(A, y_tr); p = m.predict_proba(B)[:, 1]
                models[name] = ("gbm", m)
        out[name] = (p, brier(p, y_va), logloss(p, y_va), auc(p, y_va))
        print(f"{name:18s} brier {out[name][1]:.4f}  logloss {out[name][2]:.4f}  auc {out[name][3]:.3f}")
    best = min(("logistic", "gbm"), key=lambda k: out[k][2])
    p = out[best][0]; va = va.assign(p=p)
    print(f"\nbest on validation: {best}\n"); print(calibration(p, y_va).to_string())
    # cut points: green = top band where actual >= 0.65 holds, amber = actual >= 0.58, red below. Found on validation deciles.
    q = va.assign(bucket=pd.qcut(va.p, 10, labels=False, duplicates="drop")).groupby("bucket").agg(n=("target_over25", "size"), pmin=("p", "min"), pmax=("p", "max"), actual=("target_over25", "mean"))
    print("\nvalidation deciles:"); print(q.round(3).to_string())
    green = q[q.actual >= 0.65].pmin.min(); amber = q[q.actual >= 0.58].pmin.min()
    print(f"\ncut points: green p >= {green:.3f}, amber p >= {amber:.3f}")
    for lab, lo, hi in (("green", green, 2), ("amber", amber, green), ("red", 0, amber)):
        s = va[(va.p >= lo) & (va.p < hi)]
        print(f"  {lab:6s} n={len(s):5d} actual over {s.target_over25.mean():.3f}")
    print("\nby tier (validation):")
    for t, g in va.groupby("tier"):
        gg = g[g.p >= green]; print(f"  tier {t}: green n={len(gg)} actual {gg.target_over25.mean() if len(gg) else float('nan'):.3f}; all n={len(g)} base {g.target_over25.mean():.3f}")
    print("\nby competition, green only (validation):")
    for cpt, g in va[va.p >= green].groupby("comp"):
        if len(g) >= 15: print(f"  {cpt:26s} n={len(g):4d} actual {g.target_over25.mean():.3f}")
    pickle.dump({"model": models[best], "feats": FEATS, "green": float(green), "amber": float(amber)}, open("bands_model.pkl", "wb"))
    return models[best], green, amber

def predict(bundle, X):
    kind = bundle["model"][0]; B = X[bundle["feats"]].astype(float)
    if kind == "logistic":
        _, m, med, mu, sd = bundle["model"]; B = ((B.fillna(med)) - mu) / sd; return m.predict_proba(B)[:, 1]
    return bundle["model"][1].predict_proba(B)[:, 1]

if __name__ == "__main__":
    X = pd.read_pickle(sys.argv[1]); fit(X)
