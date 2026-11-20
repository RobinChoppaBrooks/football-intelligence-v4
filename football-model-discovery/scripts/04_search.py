"""04_search.py - automated formula discovery on DEV (2023-24 + 2024-25) only.

Search space (all pre-match counts, last 5 league games this season unless named):
  atoms   : side-level (home, away, sum, min, max) count thresholds (>= / <=) on 13 count variables, venue last-3 counts,
            last-10 counts, plus symmetric attack-v-defence route atoms
  pairs   : every AND of two atoms                       (structured grid)
  triples : 60,000 random ANDs of three atoms            (randomised search, fixed seed)
  linear  : integer-weight scores (-1..2) over 8 count aggregates, cut at the top 10 / 20 / 33% (simple scoring formulas)
  trees   : depth 2-4 decision trees, every leaf a rule  (interpretable tree rules)
Null search: the identical pair search with outcomes shuffled within league-season, to measure how good the best
formula looks by pure chance. Nothing here reads VAL or TEST.
Outputs: results/search_dev_candidates.parquet (shortlist), results/search_log.json
"""
import json, itertools, time, numpy as np, pandas as pd
from sklearn.tree import DecisionTreeClassifier, _tree
import lab

SEED = 20261120
rng = np.random.default_rng(SEED)
X = lab.load()
D = lab.universe(X, lab.DEV).reset_index(drop=True)
y = D.y.values.astype(np.float32); N = len(D); base = y.mean()

VARS = ["s1", "s2", "s3", "c1", "c2", "c3", "cs", "fts", "o25", "o35", "btts", "both2", "one3"]


def frame(d):
    """the named count variables every formula may use."""
    V = {}
    for v in VARS:
        h, a = d[f"h_S5_{v}"].values, d[f"a_S5_{v}"].values
        V[f"h.{v}"] = h; V[f"a.{v}"] = a; V[f"sum.{v}"] = h + a; V[f"min.{v}"] = np.minimum(h, a); V[f"max.{v}"] = np.maximum(h, a)
    for v in ("o25", "s2", "c2"):
        V[f"hv3.{v}"] = d[f"h_V3_{v}"].values; V[f"av3.{v}"] = d[f"a_V3_{v}"].values
        V[f"v3sum.{v}"] = d[f"h_V3_{v}"].values + d[f"a_V3_{v}"].values
    V["l10sum.o25"] = d.h_S10_o25.values + d.a_S10_o25.values
    V["goals5.sum"] = d.h_S5_g.values + d.a_S5_g.values
    V["route.s2c2"] = np.maximum(d.h_S5_s2 + d.a_S5_c2, d.a_S5_s2 + d.h_S5_c2).values
    V["route.s3c3"] = np.maximum(d.h_S5_s3 + d.a_S5_c3, d.a_S5_s3 + d.h_S5_c3).values
    V["route.min"] = np.maximum(np.minimum(d.h_S5_s2, d.a_S5_c2), np.minimum(d.a_S5_s2, d.h_S5_c2)).values
    V["drivers20"] = (d.h_S5_s2 + d.a_S5_s2 + d.h_S5_c2 + d.a_S5_c2).values
    lr = np.where(d.lg_n >= 30, d.lg_o25 / d.lg_n.replace(0, np.nan), d.pl_o / d.pl_n)
    V["lg.o25x10"] = np.round(np.nan_to_num(lr, nan=0.53) * 10)      # league Over 2.5 rate in tenths (5 = half)
    return {k: np.nan_to_num(np.asarray(v, float), nan=-99) for k, v in V.items()}


def atoms_for(V):
    out = []
    for name, v in V.items():
        vals = np.unique(v[v > -99])
        if len(vals) > 25:
            vals = np.unique(np.quantile(v, np.linspace(0.05, 0.95, 19)).round())
        for k in vals:
            for op in (">=", "<="):
                m = (v >= k) if op == ">=" else ((v <= k) & (v > -99))
                out.append((f"{name} {op} {int(k) if float(k).is_integer() else k}", m))
    return out


V = frame(D)
A = atoms_for(V)
A = [(n, m) for n, m in A if 0.02 * N <= m.sum() <= 0.98 * N]
names = [n for n, _ in A]; M = np.stack([m for _, m in A]).astype(np.float32)   # atoms x fixtures
print(f"DEV fixtures {N}, base {int(y.sum())} won (1 in {N/y.sum():.2f}); atoms {len(names)}", flush=True)
log = {"dev_fixtures": N, "dev_won": int(y.sum()), "atoms": len(names), "seed": SEED}


def wilson_lb(k, n, z=1.96):
    n = np.maximum(n, 1); p = k / n; d = 1 + z * z / n
    return ((p + z * z / (2 * n)) - z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d


def pair_search(yv, keep_top=4000):
    """all AND pairs; returns the best by Wilson lower bound within each volume band."""
    S = M @ M.T                      # selected counts
    K = (M * yv) @ M.T               # wins
    iu = np.triu_indices(len(names), 1)
    n = S[iu]; k = K[iu]
    lb = wilson_lb(k, n)
    return iu, n, k, lb


BANDS = [(0.02, 0.05), (0.05, 0.10), (0.10, 0.20), (0.20, 0.35), (0.35, 0.60)]

t = time.time()
iu, n, k, lb = pair_search(y)
log["pairs_tested"] = int(len(n)); print(f"pairs {len(n):,} in {time.time()-t:.1f}s", flush=True)
cands = []
for i, nm in enumerate(names):        # single atoms
    s = M[i].sum(); w = (M[i] * y).sum()
    cands.append(("atom", nm, int(s), int(w), float(wilson_lb(w, s))))
order = np.argsort(-lb)
for lo, hi in BANDS:
    sel = order[(n[order] >= lo * N) & (n[order] < hi * N)][:60]
    for j in sel:
        cands.append(("pair", f"{names[iu[0][j]]} AND {names[iu[1][j]]}", int(n[j]), int(k[j]), float(lb[j])))

# ---- null search: same pair search on shuffled outcomes (within league-season), 3 shuffles
null = []
for r in range(3):
    ys = D.groupby(["league_id", "season"]).y.transform(lambda s: s.sample(frac=1, random_state=SEED + r).values).values.astype(np.float32)
    _, nn_, kk_, lb_ = pair_search(ys)
    for lo, hi in BANDS:
        m = (nn_ >= lo * N) & (nn_ < hi * N)
        j = np.argmax(np.where(m, lb_, -1))
        null.append({"shuffle": r, "band": f"{int(lo*100)}-{int(hi*100)}%", "best_won": int(kk_[j]), "best_sel": int(nn_[j]), "best_rate": float(kk_[j] / nn_[j])})
real_best = []
for lo, hi in BANDS:
    m = (n >= lo * N) & (n < hi * N); j = np.argmax(np.where(m, lb, -1))
    real_best.append({"band": f"{int(lo*100)}-{int(hi*100)}%", "best_formula": f"{names[iu[0][j]]} AND {names[iu[1][j]]}", "best_won": int(k[j]), "best_sel": int(n[j]), "best_rate": float(k[j] / n[j])})
log["null_search"] = null; log["real_best_by_band"] = real_best
print(pd.DataFrame(null).groupby("band").best_rate.max().round(3).to_dict(), flush=True)
print(pd.DataFrame(real_best)[["band", "best_won", "best_sel", "best_rate"]].to_string(), flush=True)

# ---- random triples
t = time.time(); T = 60000
tri = rng.integers(0, len(names), size=(T, 3))
tri = tri[(tri[:, 0] != tri[:, 1]) & (tri[:, 0] != tri[:, 2]) & (tri[:, 1] != tri[:, 2])]
Mb = M.astype(bool)
best_tri = []
for ch in np.array_split(tri, 30):
    sel = Mb[ch[:, 0]] & Mb[ch[:, 1]] & Mb[ch[:, 2]]
    nn_ = sel.sum(1); kk_ = (sel * y.astype(bool)).sum(1); lbb = wilson_lb(kk_, nn_)
    for i in range(len(ch)):
        if nn_[i] >= 0.02 * N:
            best_tri.append((lbb[i], int(nn_[i]), int(kk_[i]), ch[i]))
log["triples_tested"] = int(len(tri)); print(f"triples {len(tri):,} in {time.time()-t:.1f}s", flush=True)
best_tri.sort(key=lambda r: -r[0])
for lo, hi in BANDS:
    got = [b for b in best_tri if lo * N <= b[1] < hi * N][:40]
    for lbb, nn_, kk_, ch in got:
        cands.append(("triple", " AND ".join(names[c] for c in ch), nn_, kk_, float(lbb)))

# ---- linear integer-weight scores
AGG = ["sum.s2", "sum.c2", "sum.o25", "sum.cs", "sum.fts", "route.s2c2", "v3sum.o25", "lg.o25x10"]
Z = np.stack([V[a] for a in AGG]).astype(np.float32); Z[Z == -99] = 0
W = np.array(list(itertools.product([-1, 0, 1, 2], repeat=len(AGG))), np.float32)
W = W[(W != 0).sum(1) >= 1]
t = time.time(); lin = []
for ch in np.array_split(np.arange(len(W)), 40):
    Sc = W[ch] @ Z                                   # formulas x fixtures
    for q in (0.10, 0.20, 0.33):
        thr = np.quantile(Sc, 1 - q, axis=1, method="higher")[:, None]
        sel = Sc >= thr; nn_ = sel.sum(1); kk_ = (sel * y).sum(1); lbb = wilson_lb(kk_, nn_)
        for i, wi in enumerate(ch):
            lin.append((float(lbb[i]), int(nn_[i]), int(kk_[i]), int(wi), q, float(thr[i, 0])))
log["linear_formulas_tested"] = int(len(W)); log["linear_evaluations"] = len(lin)
print(f"linear {len(W):,} formulas x 3 cuts in {time.time()-t:.1f}s", flush=True)
lin.sort(key=lambda r: -r[0])
for q in (0.10, 0.20, 0.33):
    for lbb, nn_, kk_, wi, qq, thr in [r for r in lin if r[4] == q][:40]:
        terms = " + ".join(f"{int(w)}*{a}" for w, a in zip(W[wi], AGG) if w != 0).replace("+ -1*", "- ").replace("1*", "")
        cands.append(("linear", f"[{terms}] >= {thr:g}", nn_, kk_, lbb))

# ---- decision-tree rules
tree_vars = list(V.keys()); TV = np.stack([V[k] for k in tree_vars]).T
ntrees = 0
for depth in (2, 3, 4):
    for leaf in (150, 300, 600):
        clf = DecisionTreeClassifier(max_depth=depth, min_samples_leaf=leaf, random_state=SEED).fit(TV, y); ntrees += 1
        tr = clf.tree_
        def walk(node, conds):
            if tr.feature[node] == _tree.TREE_UNDEFINED:
                yield conds, node; return
            f = tree_vars[tr.feature[node]]; th = tr.threshold[node]
            yield from walk(tr.children_left[node], conds + [f"{f} <= {np.floor(th):g}"])
            yield from walk(tr.children_right[node], conds + [f"{f} >= {np.floor(th)+1:g}"])
        for conds, node in walk(0, []):
            nn_ = int(tr.n_node_samples[node]); kk_ = int(round(tr.value[node][0][1] * nn_)) if tr.value[node].sum() <= 1.0001 else int(tr.value[node][0][1])
            cands.append(("tree", " AND ".join(conds), nn_, kk_, float(wilson_lb(kk_, nn_))))
log["trees_fitted"] = ntrees

C = pd.DataFrame(cands, columns=["method", "formula", "dev_selected", "dev_won", "dev_lb95"]).drop_duplicates("formula")
C["dev_rate"] = C.dev_won / C.dev_selected
C["dev_share"] = C.dev_selected / N
log["total_formulas_evaluated"] = int(len(names) + log["pairs_tested"] + log["triples_tested"] + log["linear_evaluations"] + C[C.method == "tree"].shape[0])
log["shortlist"] = int(len(C))
C.to_parquet(f"{lab.ROOT}/results/search_dev_candidates.parquet")
json.dump(log, open(f"{lab.ROOT}/results/search_log.json", "w"), indent=1)
print(json.dumps({k: v for k, v in log.items() if k not in ("null_search", "real_best_by_band")}, indent=1))
print(C.sort_values("dev_lb95", ascending=False).groupby(pd.cut(C.dev_share, [0, .05, .1, .2, .35, .6, 1])).head(3).to_string())
