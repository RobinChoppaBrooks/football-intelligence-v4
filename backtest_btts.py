"""Chronological backtest of the production BTTS verdict against alternatives and baselines.

python3 backtest_btts.py [features_all.pkl]   (build it first: python3 -c "import features; features.build('football.db').to_pickle('features_all.pkl')")
Writes reports/btts_audit/backtest/backtest_rules.csv, backtest_groups.csv, backtest_model_calibration_oos.csv, backtest_params.json.
Run from the repository root. Read-only on everything else.

Train/validation/test are the model's own: GBM fitted on 2023-24 and 2024-25, cut points chosen on 2025-26, so the only
clean out-of-sample period is season 2026-27 (August to 28 October 2026). The rule-based candidates are not fitted at all,
but the evidence-score cut is chosen on 2023 to 2025 and then applied unchanged to 2026-27.
"""
import sys, os, pickle, json, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
repo, feats, outdir = ".", sys.argv[1] if len(sys.argv) > 1 else "features_all.pkl", "reports/btts_audit/backtest"; os.makedirs(outdir, exist_ok=True)
sys.path.insert(0, repo)
from btts import predict as btts_predict
from btts_rules import counts_from_features, prod_pattern, candidates, evidence_score

X = pd.read_pickle(feats)
X = X[X.target_btts.notna()].copy()
bb = pickle.load(open(f"{repo}/btts_model.pkl", "rb"))
X["p_btts"] = btts_predict(bb, X)
C = counts_from_features(X)
X["ev"] = evidence_score(C)
y = X.target_btts.astype(int)
X["period"] = np.where(X.season <= 2024, "train 2023-25", np.where(X.season == 2025, "validation 2025-26", "out of sample 2026-27"))
full = (C.h_n >= 5) & (C.a_n >= 5)
lg = X.is_cup == 0

def tab(mask, R, label):
    rows = []
    yy = y[mask]
    for col in R.columns:
        pr = R.loc[mask, col]
        ny, nn = int(pr.sum()), int((~pr).sum())
        rows.append(dict(period=label, rule=col, n=int(mask.sum()), base_rate=round(float(yy.mean()), 3),
                         yes_n=ny, yes_hit=int(yy[pr].sum()), yes_precision=round(float(yy[pr].mean()), 3) if ny else None,
                         no_n=nn, no_hit=int((1 - yy[~pr]).sum()), no_precision=round(float((1 - yy[~pr]).mean()), 3) if nn else None,
                         accuracy=round(float(((pr.astype(int) == yy)).mean()), 3)))
    return pd.DataFrame(rows)

# choose the evidence-score cut on train+validation only: smallest cut whose YES precision >= 0.60 with at least 10% coverage
dev = (X.period != "out of sample 2026-27") & full & lg
best = None
for cut in range(15, 29):
    pr = X.ev[dev] >= cut
    if pr.mean() < 0.10: break
    prec = y[dev][pr].mean()
    if prec >= 0.60 and best is None: best = cut
ev_cut = best or 23
print("evidence-score YES cut chosen on 2023-2025 (first cut with YES precision >= 0.60):", ev_cut)

R, _ = candidates(C, X.p_btts, bb["high"], bb["medium"], ev_cut_yes=ev_cut)
R["BASE_league_rate_over_50"] = X.lg_btts.fillna(0.5) >= 0.5
R["AUDIT_v1_yes_or_lean_yes"] = (X.p_btts >= bb["high"]) | ((X.p_btts >= bb["medium"]) & ((X.ev >= ev_cut) | (C[["h_btts", "a_btts"]].min(axis=1) >= 4)))
R["AUDIT_v1_yes_only"] = X.p_btts >= bb["high"]
R["COMBO_model_high_and_evidence_25"] = (X.p_btts >= bb["high"]) & (X.ev >= 25)

out = []
for per in ("train 2023-25", "validation 2025-26", "out of sample 2026-27"):
    m = (X.period == per) & full & lg
    out.append(tab(m, R, per + " (league, 5 games each side)"))
m = (X.period == "out of sample 2026-27") & lg & (C.h_n >= 3) & (C.a_n >= 3)
out.append(tab(m, R, "out of sample 2026-27 (league, 3+ games each side)"))
m = (X.period == "out of sample 2026-27") & (X.is_cup == 1) & (C.h_n >= 3) & (C.a_n >= 3)
out.append(tab(m, R, "out of sample 2026-27 (cup ties, 3+ league games each side)"))
T = pd.concat(out); T.to_csv(f"{outdir}/backtest_rules.csv", index=False)
print(T.to_string(index=False))

# the contradiction groups: production NO split by what the model and the evidence say
X["prod_yes"] = R.PROD_pattern_rule; X["lab"] = np.where(X.p_btts >= bb["high"], "High", np.where(X.p_btts >= bb["medium"], "Medium", "Low"))
X["min_btts"] = C[["h_btts", "a_btts"]].min(axis=1); X["min_s1"] = C[["h_s1", "a_s1"]].min(axis=1); X["min_c1"] = C[["h_c1", "a_c1"]].min(axis=1)
G = []
for per in ("validation 2025-26", "out of sample 2026-27"):
    m = (X.period == per) & full & lg
    d = X[m]
    for verdict in (False, True):
        for lab in ("High", "Medium", "Low"):
            g = d[(d.prod_yes == verdict) & (d.lab == lab)]
            G.append(dict(period=per, prod_verdict="YES" if verdict else "NO", model_likelihood=lab, n=len(g), btts_hit=int(g.target_btts.sum()), actual_rate=round(float(g.target_btts.mean()), 3) if len(g) else None))
    for mb in range(6):
        g = d[(~d.prod_yes) & (d.min_btts == mb)]
        G.append(dict(period=per, prod_verdict="NO", model_likelihood=f"any, both sides BTTS >= {mb}/5 (min = {mb})", n=len(g), btts_hit=int(g.target_btts.sum()), actual_rate=round(float(g.target_btts.mean()), 3) if len(g) else None))
    for ev in range(14, 31):
        g = d[d.ev == ev]
        G.append(dict(period=per, prod_verdict="any", model_likelihood=f"evidence score = {ev}", n=len(g), btts_hit=int(g.target_btts.sum()), actual_rate=round(float(g.target_btts.mean()), 3) if len(g) else None))
G = pd.DataFrame(G); G.to_csv(f"{outdir}/backtest_groups.csv", index=False)
print(); print(G.to_string(index=False))

# calibration of the model probability out of sample (deciles)
m = (X.period == "out of sample 2026-27") & full & lg
d = X[m].assign(b=lambda t: pd.qcut(t.p_btts, 10, labels=False, duplicates="drop"))
cal = d.groupby("b").agg(n=("target_btts", "size"), p_min=("p_btts", "min"), p_mean=("p_btts", "mean"), actual=("target_btts", "mean")).round(3)
cal.to_csv(f"{outdir}/backtest_model_calibration_oos.csv"); print(); print(cal.to_string())
json.dump(dict(ev_cut=ev_cut, cut_high=bb["high"], cut_medium=bb["medium"]), open(f"{outdir}/backtest_params.json", "w"), indent=1)
