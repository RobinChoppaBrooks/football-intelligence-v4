"""families.py - the 12 model families as score functions  score(train, apply) -> higher = more likely Over 2.5.
Fitted families learn only from `train` (always strictly earlier seasons than `apply`). Count rules ignore `train`."""
import numpy as np, pandas as pd
from math import exp
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from scipy.stats import poisson

SEED = 20261120


def c(d, col):
    return d[col].astype(float).fillna(0.0)


# ---------- 1-4, 7, 8: transparent count scores ----------
def f1_collision(tr, d):      # strongest attack v weakest defence route
    return np.maximum(c(d, "h_S5_s2") + c(d, "a_S5_c2"), c(d, "a_S5_s2") + c(d, "h_S5_c2"))

def f2_two_attacks(tr, d):
    return c(d, "h_S5_s2") + c(d, "a_S5_s2") + 0.01 * np.minimum(c(d, "h_S5_s2"), c(d, "a_S5_s2"))

def f3_defensive(tr, d):
    return c(d, "h_S5_c2") + c(d, "a_S5_c2") + 0.01 * np.minimum(c(d, "h_S5_c2"), c(d, "a_S5_c2"))

def f3b_drivers20(tr, d):     # V4.1's displayed drivers20: both Scored 2+ and both Let in 2+
    return c(d, "h_S5_s2") + c(d, "a_S5_s2") + c(d, "h_S5_c2") + c(d, "a_S5_c2")

def f4_one_sided(tr, d):      # one dominant attack against a defence that leaks: goal counts, last 5
    return np.maximum(c(d, "h_S5_gf") + c(d, "a_S5_ga"), c(d, "a_S5_gf") + c(d, "h_S5_ga"))

def f4b_one_sided3(tr, d):
    return np.maximum(c(d, "h_S5_s3") + c(d, "a_S5_c3"), c(d, "a_S5_s3") + c(d, "h_S5_c3"))

def f_o25_counts(tr, d):      # supporting evidence on its own: both sides' Over 2.5 count, last 5
    return c(d, "h_S5_o25") + c(d, "a_S5_o25")

def f_goals10(tr, d):         # total goals in both sides' last 10 league games (counts of goals)
    return c(d, "h_S10_g") + c(d, "a_S10_g")

def f7_venue(tr, d):          # venue-only version of drivers20 (home at home, away away, last 5)
    return c(d, "h_V5_s2") + c(d, "h_V5_c2") + c(d, "a_V5_s2") + c(d, "a_V5_c2")

def f7b_venue_blend(tr, d):
    return f3b_drivers20(tr, d) + 0.5 * f7_venue(tr, d)

def f8_opp_adjusted(tr, d):   # goals above what each past opponent usually conceded / scored
    return c(d, "h_S5_adj_gf") + c(d, "a_S5_adj_gf") + c(d, "h_S5_adj_ga") + c(d, "a_S5_adj_ga")


# ---------- 6: momentum (fitted logistic, base v base+acceleration) ----------
BASE = ["h_S5_s2", "a_S5_s2", "h_S5_c2", "a_S5_c2", "h_S5_o25", "a_S5_o25", "h_S5_cs", "a_S5_cs", "h_S5_fts", "a_S5_fts", "lg_rate"]

def _prep(d):
    d = d.copy()
    d["lg_rate"] = np.where(d.lg_n >= 30, d.lg_o25 / d.lg_n.replace(0, np.nan), d.pl_o / d.pl_n)
    for s in ("h", "a"):
        for m in ("gf", "ga", "g"):
            n3 = d[f"{s}_S3_n"].replace(0, np.nan); n10 = d[f"{s}_X10_n"].replace(0, np.nan)
            d[f"{s}_acc_{m}"] = (d[f"{s}_S3_{m}"] / n3 - d[f"{s}_X10_{m}"] / n10)
    return d

def _logit(tr, d, feats, C=0.5):
    tr, d = _prep(tr), _prep(d)
    A = tr[feats].astype(float); B = d[feats].astype(float); med = A.median()
    sc = StandardScaler().fit(A.fillna(med))
    m = LogisticRegression(C=C, max_iter=3000).fit(sc.transform(A.fillna(med)), tr.y)
    return m.predict_proba(sc.transform(B.fillna(med)))[:, 1]

def f6_base_logit(tr, d):
    return _logit(tr, d, BASE)

def f6_momentum_logit(tr, d):
    return _logit(tr, d, BASE + [f"{s}_acc_{m}" for s in "ha" for m in ("gf", "ga", "g")])


# ---------- 9: historical match DNA (nearest neighbours from earlier fixtures only) ----------
DNA = ["h_S5_s2", "a_S5_s2", "h_S5_c2", "a_S5_c2", "h_S5_o25", "a_S5_o25", "h_S5_cs", "a_S5_cs", "h_V3_o25", "a_V3_o25", "lg_rate"]

def make_knn(k):
    def f(tr, d):
        tr, d = _prep(tr), _prep(d)
        A = tr[DNA].astype(float); med = A.median(); A = A.fillna(med); B = d[DNA].astype(float).fillna(med)
        sc = StandardScaler().fit(A); nn = NearestNeighbors(n_neighbors=k).fit(sc.transform(A))
        idx = nn.kneighbors(sc.transform(B), return_distance=False)
        return tr.y.values[idx].mean(axis=1)
    f.__name__ = f"f9_knn{k}"; return f


# ---------- 10: Poisson / Dixon-Coles ----------
def _ptot3(lh, la, rho=0.0):
    """P(total >= 3) from independent Poisson goals, optional Dixon-Coles low-score correction."""
    lh = np.asarray(lh, float); la = np.asarray(la, float)
    ph = [poisson.pmf(i, lh) for i in range(3)]; pa = [poisson.pmf(j, la) for j in range(3)]
    tau = {(0, 0): 1 - lh * la * rho, (0, 1): 1 + lh * rho, (1, 0): 1 + la * rho, (1, 1): 1 - rho}
    p_le2 = 0
    for i in range(3):
        for j in range(3 - i):
            p_le2 = p_le2 + ph[i] * pa[j] * tau.get((i, j), 1.0)
    return 1 - p_le2

def _lambdas(d, window="X10", m=4.0):
    """shrunk multiplicative attack x defence rates from each side's last-10 league games."""
    lg_n = d.lg_n.replace(0, np.nan)
    hmu = np.where(d.lg_n >= 30, d.lg_hgoals / lg_n, d.pl_hg / d.pl_n)
    amu = np.where(d.lg_n >= 30, d.lg_agoals / lg_n, d.pl_ag / d.pl_n)
    hmu = pd.Series(hmu, index=d.index).fillna(1.45); amu = pd.Series(amu, index=d.index).fillna(1.15)
    mu = (hmu + amu) / 2
    def rate(s, col):
        return (d[f"{s}_{window}_{col}"].fillna(0) + m * mu) / (d[f"{s}_{window}_n"].fillna(0) + m)
    ha, hd, aa, ad = rate("h", "gf"), rate("h", "ga"), rate("a", "gf"), rate("a", "ga")
    lh = hmu * (ha / mu) * (ad / mu); la = amu * (aa / mu) * (hd / mu)
    return lh.values, la.values

def f10_poisson(tr, d):
    lh, la = _lambdas(d); return _ptot3(lh, la)

def f10_poisson_s5(tr, d):
    lh, la = _lambdas(d, "S5", m=3.0); return _ptot3(lh, la)

def f10_dixon_coles(tr, d):
    """same rates; rho and an overall goal-level scale fitted on train by grid search on log loss (2 params)."""
    lh, la = _lambdas(tr); best = None
    for s in np.round(np.arange(0.80, 1.201, 0.025), 3):
        for rho in np.round(np.arange(-0.40, 0.401, 0.05), 3):
            p = np.clip(_ptot3(lh * s, la * s, rho), 1e-6, 1 - 1e-6)
            ll = -np.mean(tr.y * np.log(p) + (1 - tr.y) * np.log(1 - p))
            if best is None or ll < best[0]:
                best = (ll, s, rho)
    _, s, rho = best; f10_dixon_coles.params = {"scale": round(float(s), 3), "rho": round(float(rho), 3)}
    lh, la = _lambdas(d); return _ptot3(lh * s, la * s, rho)


# ---------- 11: machine learning on the full library ----------
def ml_feats(d):
    keep = [col for col in d.columns if col[:2] in ("h_", "a_") and any(col.startswith(f"{s}_{w}_") for s in "ha" for w in ("S3", "S5", "S10", "X10", "X15", "V3", "V5"))]
    keep = [k for k in keep if not k.endswith("_sbh")]
    return keep + ["lg_rate"]

def _ml(model, tr, d):
    tr, d = _prep(tr), _prep(d); F = ml_feats(tr)
    A = tr[F].astype(float); med = A.median()
    if isinstance(model, LogisticRegression):
        sc = StandardScaler().fit(A.fillna(med)); model.fit(sc.transform(A.fillna(med)), tr.y)
        return model.predict_proba(sc.transform(d[F].astype(float).fillna(med)))[:, 1]
    if isinstance(model, RandomForestClassifier):
        model.fit(A.fillna(med), tr.y); return model.predict_proba(d[F].astype(float).fillna(med))[:, 1]
    model.fit(A, tr.y); return model.predict_proba(d[F].astype(float))[:, 1]

def f11_logit_l2(tr, d): return _ml(LogisticRegression(C=0.05, max_iter=5000), tr, d)
def f11_logit_l1(tr, d): return _ml(LogisticRegression(C=0.02, penalty="l1", solver="liblinear", max_iter=5000), tr, d)
def f11_rf(tr, d): return _ml(RandomForestClassifier(n_estimators=400, min_samples_leaf=60, max_features=0.3, n_jobs=2, random_state=SEED), tr, d)
def f11_hgb(tr, d): return _ml(HistGradientBoostingClassifier(max_depth=3, learning_rate=0.04, max_iter=300, min_samples_leaf=80, l2_regularization=1.0, random_state=SEED), tr, d)
def f11_hgb_shallow(tr, d): return _ml(HistGradientBoostingClassifier(max_depth=2, learning_rate=0.03, max_iter=250, min_samples_leaf=150, l2_regularization=2.0, random_state=SEED), tr, d)


COUNT_RULES = [f1_collision, f2_two_attacks, f3_defensive, f3b_drivers20, f4_one_sided, f4b_one_sided3, f_o25_counts, f_goals10, f7_venue, f7b_venue_blend, f8_opp_adjusted]
FITTED = [f6_base_logit, f6_momentum_logit, make_knn(50), make_knn(150), make_knn(400), f10_poisson, f10_poisson_s5, f10_dixon_coles,
          f11_logit_l2, f11_logit_l1, f11_rf, f11_hgb, f11_hgb_shallow]
FAMILY_OF = {"f1": "1 Attack v Defence collision", "f2": "2 Two powerful attacks", "f3": "3 Defensive vulnerability", "f4": "4 One-sided goal potential",
             "f_": "5 Combined counts (single scores)", "f6": "6 Momentum", "f7": "7 Home/away specialists", "f8": "8 Opponent-adjusted",
             "f9": "9 Historical match DNA (kNN)", "f10": "10 Poisson / Dixon-Coles", "f11": "11 Machine learning", "f12": "12 Consensus", "v4": "V4.1 (locked)"}

OVERRIDE = {"f6_base_logit": "6 Momentum (baseline, no momentum terms)", "f3b_drivers20": "5 Combined counts (drivers20)", "f_o25_counts": "5 Combined counts (Over 2.5 counts)", "f_goals10": "5 Combined counts (goals, last 10)"}

def family(name):
    if name in OVERRIDE:
        return OVERRIDE[name]
    for k in sorted(FAMILY_OF, key=len, reverse=True):
        if name.startswith(k):
            return FAMILY_OF[k]
    return "?"
