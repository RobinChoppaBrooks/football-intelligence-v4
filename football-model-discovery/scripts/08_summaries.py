"""08_summaries.py - league characteristics, V4.1 failure analysis (descriptive only, no new filters), formula robustness
summary, and the master workbook of every tested formula. Writes results/*.csv and results/master_formulas.xlsx"""
import json, numpy as np, pandas as pd
import lab

R = f"{lab.ROOT}/results"
X = lab.load()
ALL = lab.universe(X, lab.DEV + lab.VAL + lab.TEST)

# league characteristics (all FT league fixtures, counts)
G = X[X.eval_ok & X.season.isin(lab.DEV + lab.VAL + lab.TEST)]
lc = G.groupby(["league_id", "season"]).agg(fixtures=("y", "size"), over25=("y", "sum"), home_goals=("ft_home", "sum"), away_goals=("ft_away", "sum")).reset_index()
lc["league"] = lc.league_id.map(lab.LEAGUE_NAMES); lc["season"] = lc.season.map(lab.SEASON_NAMES); lc["one_in"] = (lc.fixtures / lc.over25).round(2)
lc.to_csv(f"{R}/league_characteristics.csv", index=False)
piv = lc.pivot(index="league", columns="season", values="over25").astype(int).astype(str) + " of " + lc.pivot(index="league", columns="season", values="fixtures").astype(int).astype(str)
print(piv.to_string())

# V4.1 by league, top 20 a window, VAL + TEST (out of its training seasons)
VT = ALL[ALL.season.isin(lab.VAL + lab.TEST)]
m = lab.topk_per_window(VT, "v4_score", 20)
bl = VT.assign(sel=m).groupby("league_id").agg(eligible=("y", "size"), base_won=("y", "sum")).join(VT[m].groupby("league_id").y.agg(selected="size", won="sum"))
bl.index = bl.index.map(lab.LEAGUE_NAMES); bl.to_csv(f"{R}/v4_top20_by_league.csv"); print(bl.to_string())

# failure analysis: V4.1 top-20 selections that lost v won (VAL + TEST), mean of key counts (description only)
S = VT[m].copy()
keys = ["h_S5_s2", "a_S5_s2", "h_S5_c2", "a_S5_c2", "h_S5_cs", "a_S5_cs", "h_S5_fts", "a_S5_fts", "h_S5_o25", "a_S5_o25"]
fa = S.groupby("y")[keys].mean().T.rename(columns={0: "lost_avg", 1: "won_avg"}).round(2)
fa["lost_n"] = int((S.y == 0).sum()); fa["won_n"] = int(S.y.sum())
# the 'strong attacks meet a resilient defence' pattern Rob asked about
S["strong_att_v_tight_def"] = ((S.h_S5_s2 >= 3) & (S.a_S5_cs >= 2)) | ((S.a_S5_s2 >= 3) & (S.h_S5_cs >= 2))
pat = S.groupby("strong_att_v_tight_def").y.agg(["size", "sum"])
fa.to_csv(f"{R}/failure_analysis.csv"); pat.to_csv(f"{R}/failure_pattern_att_v_tight_def.csv")
print(fa.to_string()); print(pat)
# losing scorelines among V4 top-20
print(S[S.y == 0].assign(score=lambda d: d.ft_home.astype(int).astype(str) + "-" + d.ft_away.astype(int).astype(str)).score.value_counts().head(6))

# robustness summary for finalists
RB = pd.read_csv(f"{R}/formula_robustness.csv")
rs = RB.groupby(["id", "split"]).apply(lambda g: pd.Series({"variants": len(g), "variants_beating_v4": int((g.won > g.v4_matched_won).sum())})).reset_index()
rs.to_csv(f"{R}/formula_robustness_summary.csv", index=False); print(rs.pivot(index="id", columns="split", values="variants_beating_v4"))

# master workbook
C = pd.read_csv(f"{R}/validation_formulas.csv")
C.insert(0, "formula_id", [f"S{i:05d}" for i in range(1, len(C) + 1)])
pre = json.load(open(f"{R}/preregistered.json"))
fin_id = {f: f"F{i:02d}" for i, f in enumerate(pre["finalist_formulas"], 1)}
C["finalist"] = C.formula.map(fin_id)
FT = pd.read_csv(f"{R}/test_formulas_by_season.csv")
tt = FT[FT.split == "TEST"].set_index("formula")
C["test_selected"] = C.formula.map(tt.selected); C["test_won"] = C.formula.map(tt.won); C["test_v4_matched_won"] = C.formula.map(tt.v4_matched_won)
log = json.load(open(f"{R}/search_log.json"))
with pd.ExcelWriter(f"{R}/master_formulas.xlsx") as w:
    pd.DataFrame([{k: v for k, v in log.items() if not isinstance(v, list)}]).T.rename(columns={0: "value"}).to_excel(w, sheet_name="search_space")
    C.to_excel(w, sheet_name="shortlist_dev_val_test", index=False)
    FT.to_excel(w, sheet_name="finalists_by_season", index=False)
    pd.read_csv(f"{R}/formulas_by_league.csv").to_excel(w, sheet_name="finalists_by_league", index=False)
    RB.to_excel(w, sheet_name="finalists_robustness", index=False)
    pd.read_csv(f"{R}/families_validation.csv").to_excel(w, sheet_name="families_walkforward", index=False)
    pd.read_csv(f"{R}/test_rankers.csv").to_excel(w, sheet_name="rankers_val_test", index=False)
    pd.read_csv(f"{R}/test_rankers_bootstrap.csv").to_excel(w, sheet_name="rankers_test_bootstrap", index=False)
    pd.read_csv(f"{R}/accumulators.csv").to_excel(w, sheet_name="accumulators", index=False)
    pd.read_csv(f"{R}/v4_live_comparison.csv").to_excel(w, sheet_name="v4_live_log", index=False)
    pd.DataFrame(log["null_search"]).to_excel(w, sheet_name="null_search", index=False)
    pd.DataFrame(log["real_best_by_band"]).to_excel(w, sheet_name="real_best_dev_by_band", index=False)
    lc.to_excel(w, sheet_name="league_characteristics", index=False)
print("workbook written", len(C), "shortlisted formulas")
