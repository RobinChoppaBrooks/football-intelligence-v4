"""05_validate.py - score the DEV shortlist on VAL (2025-26), compare each with V4.1 at identical volume, and freeze the
finalists BEFORE the test season is opened. Writes results/validation_formulas.csv and results/preregistered.json.

Pre-declared selection rule (written before VAL was looked at, applied mechanically):
  * a formula must pick at least 100 VAL fixtures (about 1.2 per window) and its DEV and VAL rates must both beat
    V4.1 at matched volume on VAL (equal fixtures per window, ranked by the V4.1 score);
  * finalists = up to 10, ranked by VAL Wilson lower bound, skipping any formula whose VAL selection overlaps an
    already chosen one by 60% or more (so the top 10 are not ten copies of one idea);
  * ranking models: the family scores with the most VAL top-20-per-window wins go forward, plus V4.1 as the benchmark.
"""
import json, numpy as np, pandas as pd
import lab, formula as FM

X = lab.load()
D = lab.universe(X, lab.DEV).reset_index(drop=True); Va = lab.universe(X, lab.VAL).reset_index(drop=True)
C = pd.read_parquet(f"{lab.ROOT}/results/search_dev_candidates.parquet")
VD, VV = FM.variables(D), FM.variables(Va)

# self-check: the parser reproduces the search's DEV counts
bad = 0
for _, r in C.iterrows():
    m = FM.mask(r.formula, VD)
    bad += (int(m.sum()) != r.dev_selected) or (int(D.y[m].sum()) != r.dev_won)
print(f"parser check on DEV: {len(C)} formulas, {bad} mismatches")
if bad:
    mm = [r.formula for _, r in C.iterrows() if int(FM.mask(r.formula, VD).sum()) != r.dev_selected][:5]; print(mm)

rows, masks = [], {}
for _, r in C.iterrows():
    m = pd.Series(FM.mask(r.formula, VV), index=Va.index)
    s = lab.summarise(m, Va.y)
    mv = lab.matched_volume(Va, m, "v4_score"); v4w = int(Va.y[mv].sum())
    rows.append({**r.to_dict(), "val_selected": s["selected"], "val_won": s["won"], "val_lost": s["lost"], "val_one_in": s["one_in"],
                 "val_lb95": s["lo95"], "val_hi95": s["hi95"], "val_v4_matched_won": v4w, "val_minus_v4": s["won"] - v4w})
    masks[r.formula] = m.values
R = pd.DataFrame(rows)
R["val_rate"] = R.val_won / R.val_selected.replace(0, np.nan)
R["shrink_dev_to_val"] = R.val_rate - R.dev_rate
R.to_csv(f"{lab.ROOT}/results/validation_formulas.csv", index=False)

base_v = Va.y.mean()
print(f"VAL universe {len(Va)} fixtures, {int(Va.y.sum())} won (1 in {len(Va)/Va.y.sum():.2f})")
print(f"mean DEV rate of shortlist {R.dev_rate.mean():.3f} -> VAL {R.val_rate.mean():.3f} (shrinkage {R.shrink_dev_to_val.mean():+.3f})")
print(f"formulas beating V4.1 at matched volume on VAL: {(R.val_minus_v4 > 0).sum()} of {len(R)}; tied {(R.val_minus_v4 == 0).sum()}; worse {(R.val_minus_v4 < 0).sum()}")

ok = R[(R.val_selected >= 100) & (R.val_minus_v4 > 0)].sort_values("val_lb95", ascending=False)
chosen = []
for _, r in ok.iterrows():
    m = masks[r.formula]
    if any((m & masks[c]).sum() / max(1, min(m.sum(), masks[c].sum())) >= 0.6 for c in chosen):
        continue
    chosen.append(r.formula)
    if len(chosen) == 10:
        break
fin = R.set_index("formula").loc[chosen].reset_index()
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 90)
print(fin[["method", "formula", "dev_selected", "dev_won", "val_selected", "val_won", "val_one_in", "val_v4_matched_won", "val_minus_v4"]].to_string())

FV = pd.read_csv(f"{lab.ROOT}/results/families_validation.csv")
fv = FV[FV.season == "2025-26"].sort_values("top20_won", ascending=False)
rankers = list(fv.model.head(6))
if "v4" not in rankers: rankers.append("v4")
pre = {"frozen_at": pd.Timestamp.now(tz="Europe/London").isoformat(), "test_season": "2026-27 (to 17 Nov 2026)",
       "finalist_formulas": chosen, "ranking_models": rankers, "consensus": "f12 = mean percentile rank of the top 5 non-V4 ranking models",
       "acca_qualify_rule": "a fixture may fill an accumulator only if its score is at or above that model's VAL 67th percentile (top third), fixed on VAL",
       "primary_metric": "TEST top-20-per-window wins against V4.1 on identical fixtures; secondary top 5/10/15 and formula hits v V4.1 at matched volume",
       "note": "Nothing below this line may be changed after the test season is opened."}
json.dump(pre, open(f"{lab.ROOT}/results/preregistered.json", "w"), indent=1)
print(json.dumps(pre, indent=1))
