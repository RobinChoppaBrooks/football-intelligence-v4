"""06_test.py - opens the untouched test season ONCE for the pre-registered finalists, then accumulator simulation,
season / league breakdowns and threshold-robustness checks. Reads results/preregistered.json; changes nothing in it.
Fitted rankers are refitted on 2023-24..2025-26 (every season before the test) and applied to 2026-27."""
import json, re, numpy as np, pandas as pd
import lab, formula as FM, families as F

R = f"{lab.ROOT}/results"
pre = json.load(open(f"{R}/preregistered.json"))
X = lab.load()
ALL = lab.universe(X, lab.DEV + lab.VAL + lab.TEST).reset_index(drop=True)
Te = ALL[ALL.season.isin(lab.TEST)].copy(); Va = ALL[ALL.season.isin(lab.VAL)].copy()
fn = {f.__name__: f for f in F.COUNT_RULES + F.FITTED}

# ---------- ranking models on TEST (and VAL from the walk-forward file, for the accumulator tables) ----------
tr = ALL[ALL.season.isin(lab.DEV + lab.VAL)]
for m in pre["ranking_models"]:
    Te[m] = Te.v4_score if m == "v4" else np.asarray(fn[m](tr, Te), float)
WF = pd.read_parquet(f"{R}/family_scores_wf.parquet")
Va = Va.merge(WF[WF.season == 2025][["fixture_id"] + [m for m in pre["ranking_models"] if m != "v4"]], on="fixture_id")
Va["v4"] = Va.v4_score
members = [m for m in pre["ranking_models"] if m != "v4"][:5]
for d in (Va, Te):
    d["f12_consensus"] = np.mean([d[m].rank(pct=True) for m in members], axis=0)
RANKERS = pre["ranking_models"] + ["f12_consensus"]

rows = []
for nm in RANKERS:
    for lab_, d in (("VAL 2025-26", Va), ("TEST 2026-27", Te)):
        r = {"model": nm, "family": F.family(nm), "period": lab_, "eligible": len(d), "base_won": int(d.y.sum())}
        for k in (5, 10, 15, 20):
            m = lab.topk_per_window(d, nm, k); r[f"top{k}_sel"] = int(m.sum()); r[f"top{k}_won"] = int(d.y[m].sum())
            mv = lab.topk_per_window(d, "v4", k); r[f"top{k}_minus_v4"] = r[f"top{k}_won"] - int(d.y[mv].sum())
        if nm != "f12_consensus" and d[nm].between(0, 1).all():
            r["brier"] = round(lab.brier(d[nm].values, d.y.values), 4); r["logloss"] = round(lab.logloss(d[nm].values, d.y.values), 4)
        rows.append(r)
RT = pd.DataFrame(rows); RT.to_csv(f"{R}/test_rankers.csv", index=False)

# paired window bootstrap of (model - V4.1) top-20 wins on TEST
rng = np.random.default_rng(20261120); boot = []
wins = sorted(Te.window.unique())
per = {}
for nm in RANKERS:
    m = lab.topk_per_window(Te, nm, 20); per[nm] = Te.y[m].groupby(Te.window[m]).sum().reindex(wins, fill_value=0).values
for nm in RANKERS:
    if nm == "v4": continue
    diff = per[nm] - per["v4"]; bs = [diff[rng.integers(0, len(wins), len(wins))].sum() for _ in range(5000)]
    boot.append({"model": nm, "test_top20_minus_v4": int(diff.sum()), "lo95": int(np.percentile(bs, 2.5)), "hi95": int(np.percentile(bs, 97.5)),
                 "share_of_resamples_better": round(float(np.mean(np.array(bs) > 0)), 3), "windows": len(wins)})
BT = pd.DataFrame(boot); BT.to_csv(f"{R}/test_rankers_bootstrap.csv", index=False)

# ---------- finalist formulas: every season, every league, TEST v V4.1 at matched volume ----------
VA = FM.variables(ALL)
frows, lrows = [], []
for i, f in enumerate(pre["finalist_formulas"], 1):
    m = pd.Series(FM.mask(f, VA), index=ALL.index)
    for s in lab.DEV + lab.VAL + lab.TEST:
        g = ALL.season == s; d = ALL[g]; mm = m[g]
        sm = lab.summarise(mm, d.y); mv = lab.matched_volume(d, mm, "v4_score")
        frows.append({"id": f"F{i:02d}", "formula": f, "season": lab.SEASON_NAMES[s], "split": "DEV" if s in lab.DEV else ("VAL" if s in lab.VAL else "TEST"),
                      "eligible": len(d), **sm, "v4_matched_won": int(d.y[mv].sum()), "minus_v4": sm["won"] - int(d.y[mv].sum()),
                      "rejected": len(d) - sm["selected"], "rejected_won": int(d.y[~mm].sum())})
    for lg, g in ALL.groupby("league_id"):
        mm = m[g.index]
        for split, ss in (("DEV+VAL", lab.DEV + lab.VAL), ("TEST", lab.TEST)):
            q = g.season.isin(ss)
            lrows.append({"id": f"F{i:02d}", "league": lab.LEAGUE_NAMES[lg], "split": split, "selected": int(mm[q].sum()), "won": int(g.y[q & mm].sum())})
FT = pd.DataFrame(frows); FT.to_csv(f"{R}/test_formulas_by_season.csv", index=False)
FL = pd.DataFrame(lrows); FL.to_csv(f"{R}/formulas_by_league.csv", index=False)

# robustness: move each threshold of each finalist by -1 / +1 (one at a time), VAL and TEST (report only)
rb = []
for i, f in enumerate(pre["finalist_formulas"], 1):
    nums = list(re.finditer(r"(>=|<=)\s*(-?\d+)", f))
    for j, mt in enumerate(nums):
        for dlt in (-1, 1):
            g = f[:mt.start(2)] + str(int(mt.group(2)) + dlt) + f[mt.end(2):]
            m = pd.Series(FM.mask(g, VA), index=ALL.index)
            for split, ss in (("VAL", lab.VAL), ("TEST", lab.TEST)):
                q = ALL.season.isin(ss); d = ALL[q]; mm = m[q]
                mv = lab.matched_volume(d, mm, "v4_score")
                rb.append({"id": f"F{i:02d}", "variant": g, "threshold": j + 1, "delta": dlt, "split": split, "selected": int(mm.sum()), "won": int(d.y[mm].sum()), "v4_matched_won": int(d.y[mv].sum())})
RB = pd.DataFrame(rb); RB.to_csv(f"{R}/formula_robustness.csv", index=False)

# ---------- accumulators: top 5/10/15/20 per window, only fixtures in the model's VAL top third may qualify ----------
acc = []
for nm in RANKERS:
    thr = Va[nm].quantile(0.67) if nm != "f12_consensus" else None
    for lab_, d in (("VAL 2025-26", Va), ("TEST 2026-27", Te)):
        q = (d[nm] >= thr) if thr is not None else (d[nm] >= d[nm].quantile(0.67) if lab_.startswith("VAL") else d[nm] >= Va[nm].quantile(0.67))
        for k in (5, 10, 15, 20):
            m = lab.topk_per_window(d, nm, k, qualify=q)
            per_w = d[m].groupby("window").y.agg(["size", "sum"])
            full = per_w[per_w["size"] == k]
            p = d.y[m].mean() if m.sum() else np.nan
            same_lg = d[m].groupby(["window", "league_id"]).y.agg(["size", "mean"])
            acc.append({"model": nm, "period": lab_, "k": k, "windows": d.window.nunique(), "windows_full": len(full),
                        "windows_short": d.window.nunique() - len(full), "selections_in_full": int(full["size"].sum()), "won_in_full": int(full["sum"].sum()),
                        "all_won_windows": int((full["sum"] == k).sum()), "k_minus_1_windows": int((full["sum"] == k - 1).sum()),
                        "expected_all_won_if_independent": round(len(full) * (full["sum"].sum() / max(1, full["size"].sum())) ** k, 2),
                        "hits_variance_observed": round(float(full["sum"].var()), 2) if len(full) > 1 else np.nan,
                        "hits_variance_if_independent": round(k * (full["sum"].sum() / max(1, full["size"].sum())) * (1 - full["sum"].sum() / max(1, full["size"].sum())), 2) if len(full) else np.nan})
AC = pd.DataFrame(acc); AC.to_csv(f"{R}/accumulators.csv", index=False)

pd.set_option("display.width", 260); pd.set_option("display.max_columns", 30); pd.set_option("display.max_colwidth", 80)
print(RT[["model", "period", "eligible", "base_won", "top5_won", "top10_won", "top15_won", "top20_sel", "top20_won", "top20_minus_v4", "brier"]].to_string())
print(BT.to_string())
print(FT[FT.split == "TEST"][["id", "formula", "selected", "won", "one_in", "v4_matched_won", "minus_v4"]].to_string())
print(FT.groupby("split")[["selected", "won", "v4_matched_won"]].sum())
print(AC[AC.period.str.startswith("TEST")][["model", "k", "windows", "windows_full", "won_in_full", "selections_in_full", "all_won_windows", "expected_all_won_if_independent", "hits_variance_observed", "hits_variance_if_independent"]].to_string())
