"""10_pool_reranker.py - second-stage picker INSIDE V4.1's weekend pool (High + Medium + trump). V4.1 itself is unchanged.

Question (Rob, 20 Nov 2026): V4.1 gives the pool; is there a formula that picks the best 20 / 15 / 10 / 5 from it
better than simply taking V4.1's own top by score?

Method
  pool      : weekend (Fri-Sun) fixtures, Rob's 14 leagues, V4.1 score >= Medium cut 0.58084, or trump
              (one side 16+ goals in last 5 and the opponent fewer than 2 clean sheets)
  baseline  : V4.1 order (highest score first)
  rule pick : fixtures meeting the rule first (in V4.1 order), then the rest of the pool in V4.1 order, top K
  candidates: every count atom and every 2-atom AND from the main search vocabulary (scripts/formula.py),
              plus 'avoid' versions (rule-false first), plus second-stage ML models trained on pool fixtures only
  splits    : DEV 2023-24 + 2024-25 (search), VAL 2025-26 (selection, frozen to results/pool_preregistered.json),
              TEST 2026-27 opened once afterwards. Null search on shuffled pool results measures luck.
Outputs: results/pool_reranker_*.csv, results/pool_preregistered.json
"""
import json, sys, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import lab, formula as FM, families as F

R = f"{lab.ROOT}/results"; KS = (5, 10, 15, 20); SEED = 20261120
X = lab.load()
U = lab.universe(X, lab.DEV + lab.VAL + lab.TEST)
U = U[U.window.str.endswith("WE")].copy()
trump = ((U.h_S5_gf >= 16) & (U.a_S5_cs < 2)) | ((U.a_S5_gf >= 16) & (U.h_S5_cs < 2))
U["trump"] = trump
P = U[(U.v4_score >= 0.58084) | trump].copy()
P = P.sort_values(["window", "v4_score", "fixture_id"], ascending=[True, False, True]).reset_index(drop=True)


def split(seasons):
    return P[P.season.isin(seasons)].reset_index(drop=True)


def pick_wins(d, M, y):
    """M: rules x fixtures boolean (rule-true goes first). d sorted by window then V4 score.
    Returns wins[rule, k] for each K: rule-true fixtures in V4 order, then rule-false in V4 order."""
    w = d.window.values; starts = np.r_[0, np.flatnonzero(w[1:] != w[:-1]) + 1]; ends = np.r_[starts[1:], len(w)]
    out = np.zeros((M.shape[0], len(KS)), np.int64)
    for s, e in zip(starts, ends):
        m = M[:, s:e]; yy = y[s:e]
        ct = np.cumsum(m, 1); cf = np.cumsum(~m, 1); nt = m.sum(1, keepdims=True)
        for j, k in enumerate(KS):
            take_t = m & (ct <= k); room = np.maximum(0, k - np.minimum(nt, k))
            take_f = (~m) & (cf <= room)
            out[:, j] += ((take_t | take_f) * yy).sum(1)
    return out


def baseline(d):
    return pick_wins(d, np.zeros((1, len(d)), bool), d.y.values)[0]


def rule_bank(d):
    V = FM.variables(d)
    atoms = []
    for name, v in V.items():
        vals = np.unique(v[v > -99])
        if len(vals) > 25:
            vals = np.unique(np.quantile(v, np.linspace(0.05, 0.95, 19)).round())
        for k in vals:
            for op in (">=", "<="):
                atoms.append(f"{name} {op} {int(k) if float(k).is_integer() else k}")
    return atoms


def masks(d, formulas):
    V = FM.variables(d); return np.stack([FM.mask(f, V) for f in formulas])


DEV, VAL, TEST = split(lab.DEV), split(lab.VAL), split(lab.TEST)
b_dev, b_val = baseline(DEV), baseline(VAL)
atoms = rule_bank(DEV)
Md = masks(DEV, atoms)
keep = (Md.sum(1) >= 0.05 * len(DEV)) & (Md.sum(1) <= 0.95 * len(DEV))
atoms = [a for a, k in zip(atoms, keep) if k]; Md = Md[keep]
print(f"pool fixtures DEV {len(DEV)} ({DEV.window.nunique()} weekends), VAL {len(VAL)}, TEST {len(TEST)}; atoms {len(atoms)}", flush=True)

# candidates: atoms, avoid-atoms, AND pairs (prefer) - evaluated on DEV
cands = [(a, "prefer") for a in atoms] + [(a, "avoid") for a in atoms]
Mc = np.vstack([Md, ~Md])
iu = np.triu_indices(len(atoms), 1)
pairs = [(f"{atoms[i]} AND {atoms[j]}", "prefer") for i, j in zip(*iu)]
y = DEV.y.values
W1 = pick_wins(DEV, Mc, y)
W2 = np.vstack([pick_wins(DEV, Md[iu[0][c]] & Md[iu[1][c]], y) for c in np.array_split(np.arange(len(iu[0])), 60)])
allc = cands + pairs; Wd = np.vstack([W1, W2]) - b_dev
print(f"rules tested on DEV: {len(allc):,}", flush=True)

# null: shuffle pool outcomes within weekend, same search on pairs+atoms, best improvement by chance
rng = np.random.default_rng(SEED); null = []
for r in range(3):
    ys = DEV.groupby("window").y.transform(lambda s: s.sample(frac=1, random_state=SEED + r).values).values
    bs = pick_wins(DEV, np.zeros((1, len(DEV)), bool), ys)[0]
    a = pick_wins(DEV, Mc, ys) - bs
    p = np.vstack([pick_wins(DEV, Md[iu[0][c]] & Md[iu[1][c]], ys) for c in np.array_split(np.arange(len(iu[0])), 60)]) - bs
    null.append(np.vstack([a, p]).max(0).tolist())
null = np.array(null)

# shortlist: top 40 per K on DEV improvement
short = set()
for j in range(len(KS)):
    for i in np.argsort(-Wd[:, j])[:40]:
        short.add(i)
short = sorted(short)
rows = []
for i in short:
    f, mode = allc[i]
    mv = masks(VAL, [f])
    if mode == "avoid": mv = ~mv
    wv = pick_wins(VAL, mv, VAL.y.values)[0] - b_val
    rows.append({"formula": f, "mode": mode, **{f"dev_top{k}_vs_v4": int(Wd[i, j]) for j, k in enumerate(KS)}, **{f"val_top{k}_vs_v4": int(wv[j]) for j, k in enumerate(KS)}})
S = pd.DataFrame(rows)

# second-stage ML trained on pool fixtures only (DEV -> VAL)
def ml_scores(tr, ap, kind):
    Fz = F.ml_feats(F._prep(tr)) + ["v4_score"]
    A = F._prep(tr)[Fz].astype(float); B = F._prep(ap)[Fz].astype(float); med = A.median()
    if kind == "logit":
        sc = StandardScaler().fit(A.fillna(med)); m = LogisticRegression(C=0.02, max_iter=5000).fit(sc.transform(A.fillna(med)), tr.y)
        return m.predict_proba(sc.transform(B.fillna(med)))[:, 1]
    m = HistGradientBoostingClassifier(max_depth=2, learning_rate=0.03, max_iter=200, min_samples_leaf=80, random_state=SEED).fit(A, tr.y)
    return m.predict_proba(B)[:, 1]

def rank_wins(d, s):
    d = d.assign(_s=s); out = []
    for k in KS:
        m = lab.topk_per_window(d, "_s", k); out.append(int(d.y[m].sum()))
    return np.array(out)

ml = {}
for kind in ("logit", "hgb"):
    sv = ml_scores(DEV, VAL, kind); ml[kind] = (rank_wins(VAL, sv) - b_val)
print("second-stage ML on VAL (wins v V4.1 order, top 5/10/15/20):", {k: v.tolist() for k, v in ml.items()})

# freeze: per K, the rule with best VAL improvement among those also positive on DEV
fin = {}
for j, k in enumerate(KS):
    c = S[(S[f"dev_top{k}_vs_v4"] > 0) & (S[f"val_top{k}_vs_v4"] > 0)].sort_values([f"val_top{k}_vs_v4", f"dev_top{k}_vs_v4"], ascending=False)
    fin[f"top{k}"] = None if c.empty else {"formula": c.iloc[0].formula, "mode": c.iloc[0]["mode"]}
best_ml = max(ml, key=lambda k: ml[k].sum())
pre = {"frozen_at": pd.Timestamp.now(tz="Europe/London").isoformat(), "per_size_rule": fin, "second_stage_ml": best_ml,
       "rule_pick": "rule-true fixtures first in V4.1 order, then the rest of the pool in V4.1 order"}
json.dump(pre, open(f"{R}/pool_preregistered.json", "w"), indent=1)
S.to_csv(f"{R}/pool_reranker_shortlist.csv", index=False)

# ---- TEST, opened once
bt = baseline(TEST); res = []
for j, k in enumerate(KS):
    f = fin[f"top{k}"]
    if f:
        m = masks(TEST, [f["formula"]]); m = ~m if f["mode"] == "avoid" else m
        res.append({"size": k, "picker": f"{f['mode']}: {f['formula']}", "TEST_won": int(pick_wins(TEST, m, TEST.y.values)[0][j]), "V4_order_won": int(bt[j])})
trv = pd.concat([DEV, VAL]); st = ml_scores(trv, TEST, best_ml); mw = rank_wins(TEST, st)
for j, k in enumerate(KS):
    res.append({"size": k, "picker": f"second-stage {best_ml}", "TEST_won": int(mw[j]), "V4_order_won": int(bt[j])})
T = pd.DataFrame(res); T["vs_V4"] = T.TEST_won - T.V4_order_won
T.to_csv(f"{R}/pool_reranker_test.csv", index=False)

picks = {}
for nm, d, b in (("DEV", DEV, b_dev), ("VAL", VAL, b_val), ("TEST", TEST, bt)):
    picks[nm] = {f"top{k}": int(sum(min(k, n) for n in d.groupby("window").size())) for k in KS}
log = {"pool_fixtures": {"DEV": len(DEV), "VAL": len(VAL), "TEST": len(TEST)}, "weekends": {"DEV": DEV.window.nunique(), "VAL": VAL.window.nunique(), "TEST": TEST.window.nunique()},
       "picks_per_size": picks, "v4_order_won": {"DEV": b_dev.tolist(), "VAL": b_val.tolist(), "TEST": bt.tolist()},
       "rules_tested_dev": len(allc), "null_best_dev_gain_by_size": dict(zip([f"top{k}" for k in KS], null.max(0).tolist())),
       "real_best_dev_gain_by_size": dict(zip([f"top{k}" for k in KS], Wd.max(0).tolist())),
       "shortlist_beating_v4_on_val": {f"top{k}": int((S[f"val_top{k}_vs_v4"] > 0).sum()) for k in KS}, "shortlist_size": len(S),
       "ml_val_vs_v4": {k: v.tolist() for k, v in ml.items()}}
json.dump(log, open(f"{R}/pool_reranker_log.json", "w"), indent=1)
print(json.dumps(log, indent=1)); print(json.dumps(pre, indent=1)); print(T.to_string())
