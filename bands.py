"""
bands.py  -  the Over 2.5 selection model. V4.2 (11 Nov 2026): every input is a count, no averages anywhere (Rob's rule).

    python3 bands.py features.pkl        -> prints validation results and the cut points; writes bands_model.pkl

Inputs (38), all counts from this season's games before kick-off:
  each side, last 5 league games: goals scored, goals conceded, total goals, games with 3+, games with BTTS, scored 2+,
     let in 2+, clean sheets, failed to score, games with 4+, biggest total in one game, games played (12 x 2)
  each side, last 3 league games at this venue: goals scored, goals conceded, total goals, games with 3+, games played (5 x 2)
  the competition: games played so far this season, cup or league, games with 3+ in its last 50 games this season,
     games in that window (under 50 early in the season) (4)
Train: seasons 2023-24 and 2024-25. Validate: 2025-26 (never seen in training). Results are FT only (config.FINISHED).

Cut points (same rule as V4.1, set on the 2025-26 validation season split into ten equal groups by score):
  High   starts at the lowest group where at least 65 in 100 went 3+
  Medium starts at the lowest group where at least 58 in 100 went 3+
  Weak   is the bottom quarter of Medium
V4.2: every cut point is rounded to 3 decimals and stored that way, so the printed score always shows its band:
  High = score 0.xxx and above, Medium and Weak stop one thousandth below the next band, nothing sits on a boundary.
"""
import sys, pickle, numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from evaluate import brier, logloss, auc

MODEL_VERSION = "v4.2"
FEATS = [f"{s}_l5_{m}_cnt" for s in ("h", "a") for m in ("gf", "ga", "tot", "over25", "btts", "gf2", "ga2", "cs", "fts", "tot4")] + \
        [f"{s}_l5_{m}" for s in ("h", "a") for m in ("maxtot", "n")] + \
        [f"{s}_v3_{m}_cnt" for s in ("h", "a") for m in ("gf", "ga", "tot", "over25")] + [f"{s}_v3_n" for s in ("h", "a")] + \
        ["lg_games_cnt", "cup_flag", "lg_l50_o25_cnt", "lg_l50_n"]
assert len(FEATS) == 38

def r3(x): return round(float(x), 3)

def band_of(p, b):
    """High / Medium / Weak / rejected from a score, using the stored 3-decimal cut points. Score is compared at 3 decimals."""
    p = round(float(p), 3)
    if p >= b["green"]: return "High"
    if p >= b["weak"]: return "Medium"
    if p >= b["amber"]: return "Weak"
    return "rejected"

def fit(X):
    X = X[X.target_over25.notna()].copy()
    tr = X[X.season.isin([2023, 2024])]; va = X[X.season == 2025]
    m = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.04, max_iter=300, min_samples_leaf=80, l2_regularization=1.0, random_state=0)
    m.fit(tr[FEATS].astype(float), tr.target_over25.values)
    p = m.predict_proba(va[FEATS].astype(float))[:, 1]; y = va.target_over25.values
    print(f"train {len(tr)} fixtures, validate {len(va)}; validation brier {brier(p, y):.4f} logloss {logloss(p, y):.4f} auc {auc(p, y):.3f}")
    va = va.assign(p=p)
    q = va.assign(bucket=pd.qcut(va.p, 10, labels=False, duplicates="drop")).groupby("bucket").agg(
        n=("target_over25", "size"), went_3plus=("target_over25", "sum"), pmin=("p", "min"), pmax=("p", "max"))
    q["went_3plus"] = q.went_3plus.astype(int)
    print("\nvalidation groups (ten equal groups by score):"); print(q.round(3).to_string())
    hit = q.went_3plus / q.n
    green = r3(q[hit >= 0.65].pmin.min()); amber = r3(q[hit >= 0.58].pmin.min())
    weak = r3(amber + (green - amber) / 4)
    bundle = {"model": ("gbm", m), "feats": FEATS, "green": green, "weak": weak, "amber": amber, "model_version": MODEL_VERSION}
    print(f"\ncut points: High {green:.3f}+, Medium {weak:.3f} to {green - 0.001:.3f}, Weak {amber:.3f} to {weak - 0.001:.3f}, rejected {amber - 0.001:.3f} and below")
    va["band"] = [band_of(x, bundle) for x in va.p]
    for lab in ("High", "Medium", "Weak", "rejected"):
        s = va[va.band == lab]; print(f"  {lab:8s} 3+ in {int(s.target_over25.sum())} of {len(s)}")
    pickle.dump(bundle, open("bands_model.pkl", "wb"))
    return bundle

def predict(bundle, X):
    return bundle["model"][1].predict_proba(X[bundle["feats"]].astype(float))[:, 1]

if __name__ == "__main__":
    X = pd.read_pickle(sys.argv[1]); fit(X)
