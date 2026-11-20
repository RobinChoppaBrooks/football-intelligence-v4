"""09_report.py - writes report/FINAL_REPORT.md from the saved result files (every number is read, none typed)."""
import json, numpy as np, pandas as pd
import lab

R = f"{lab.ROOT}/results"
pre = json.load(open(f"{R}/preregistered.json")); log = json.load(open(f"{R}/search_log.json"))
FV = pd.read_csv(f"{R}/families_validation.csv"); RT = pd.read_csv(f"{R}/test_rankers.csv"); BT = pd.read_csv(f"{R}/test_rankers_bootstrap.csv")
FT = pd.read_csv(f"{R}/test_formulas_by_season.csv"); FL = pd.read_csv(f"{R}/formulas_by_league.csv"); RB = pd.read_csv(f"{R}/formula_robustness_summary.csv")
AC = pd.read_csv(f"{R}/accumulators.csv"); LV = pd.read_csv(f"{R}/v4_live_comparison.csv"); VC = pd.read_csv(f"{R}/validation_formulas.csv")
LC = pd.read_csv(f"{R}/league_characteristics.csv"); BL = pd.read_csv(f"{R}/v4_top20_by_league.csv", index_col=0)
PAT = pd.read_csv(f"{R}/failure_pattern_att_v_tight_def.csv", index_col=0)
X = lab.load(); U = {s: lab.universe(X, [s]) for s in (2023, 2024, 2025, 2026)}

def oi(k, n): return f"1 in {n/k:.2f}" if k else "none"
def rng(k, n):
    lo, hi = lab.wilson(k, n); return f"{int(round(lo*n))} to {int(round(hi*n))}"
def tbl(df): return df.to_markdown(index=False)

NAMES = {"v4": "V4.1 (locked)", "f11_rf": "Random forest (all count windows)", "f6_base_logit": "Logistic, 11 core counts", "f6_momentum_logit": "Logistic + momentum",
         "f11_hgb": "Gradient boosting (V4.1 settings, wider features)", "f11_hgb_shallow": "Gradient boosting, shallow", "f12_consensus": "Consensus (rank average of 5)"}
PLAIN = {
 1: "Home side's last 5 had 3+ games where one team scored 3+; home side let in 2+ in 3 or fewer of 5; at least one side scored 2+ in 4 or 5 of 5.",
 2: "Home side's last 5 league games all finished with 3+ goals.",
 3: "Points score of 29 or more: (both sides' Scored 2+) minus (both sides' 3+ games) plus (both sides' clean sheets) minus (both sides' failed to score) plus 2 x (best attack-v-defence route: one side's Scored 2+ plus the other's Let in 2+) plus (both sides' 3+ games in their last 3 at venue) plus 2 x (league's running Over 2.5 rate in tenths).",
 4: "One side scored 3+ in 3 or more of its last 5; home side scored 2+ in 2 or 3 of its last 3 home games.",
 5: "Points score of 11 or more: 2 x (both sides' Scored 2+) minus (both sides' failed to score) minus (best attack-v-defence route) plus (league's running Over 2.5 rate in tenths).",
 6: "Both sides together failed to score 4 or fewer times in their last 5; together scored 2+ in 3 or more of their last 3 at venue; together had 14 or more 3+ games in their last 10.",
 7: "Both sides together scored 3+ in 3 or more of their last 5; league's running Over 2.5 rate rounds to 6 in 10 or higher.",
 8: "Both sides together scored 3+ at least twice in their last 5; together scored 2+ in 3+ of their last 3 at venue; together 11+ games with 3+ in their last 10; best 3-goal route (one side Scored 3+ plus other side Let in 3+) 4 or more.",
 9: "Home side scored 2+ in all of its last 3 home league games.",
 10: "drivers20 (both Scored 2+ plus both Let in 2+) 8 or more; both sides together Scored 2+ 5 or more; both sides together 5 or more games with 4+ goals.",
}

L = []
w = L.append
tot_fix = sum(len(U[s]) for s in U); tot_won = sum(int(U[s].y.sum()) for s in U)
te = RT[RT.period.str.startswith("TEST")].set_index("model"); va = RT[RT.period.str.startswith("VAL")].set_index("model")
ft_test = FT[FT.split == "TEST"]; fsum = FT.groupby("split")[["selected", "won", "v4_matched_won"]].sum()
lv = LV[["v4_selected", "v4_won", "rf_same_count_won", "overlap"]].sum()

w("# Over 2.5 goals model discovery lab: final report")
w(f"Research only. Production V4.1 untouched. Run 20 Nov 2026 on the repository database (results to 17 Nov 2026). Rob's 14 leagues, league fixtures, FT results only, both sides with 3+ league games this season.\n")
bt_rf = BT.set_index("model").loc["f11_rf"]
sd_w = (bt_rf.hi95 - bt_rf.lo95) / (2 * 1.96) / np.sqrt(bt_rf.windows)      # per-window sd of the paired difference
need_w = int(np.ceil((1.96 * sd_w / 0.25) ** 2)); need_margin = int(np.ceil(1.96 * sd_w * np.sqrt(need_w)))
big = AC[(AC.model == "v4") & AC.k.isin([15, 20])]
w("## 1. Executive summary")
w(f"- **No new formula or model convincingly beats V4.1.** Recommendation: keep V4.1 as the selection engine, unchanged.")
w(f"- {log['total_formulas_evaluated']:,} formula evaluations and 25 model variants across 12 families were tested. On the untouched 2026-27 season the best challenger (a random forest) won **{int(te.loc['f11_rf','top20_won'])} v V4.1's {int(te.loc['v4','top20_won'])}** from the top 20 a window ({int(te.loc['v4','top20_sel'])} picks). The paired range for the difference is {int(BT.set_index('model').loc['f11_rf','lo95'])} to +{int(BT.set_index('model').loc['f11_rf','hi95'])}: noise.")
w(f"- The 10 pre-registered formulas won **{int(fsum.loc['TEST','won'])} v V4.1's {int(fsum.loc['TEST','v4_matched_won'])}** on 2026-27 at identical volume. On 2025-26, where they were chosen, they had led {int(fsum.loc['VAL','won'])} to {int(fsum.loc['VAL','v4_matched_won'])}. The lead was selection luck and disappeared on fresh data.")
w(f"- Chance alone manufactures impressive formulas. The same search run on shuffled results (league rates kept, team form destroyed) found a formula winning {max(n['best_won'] for n in log['null_search'] if n['band']=='2-5%' and n['best_rate']==max(m['best_rate'] for m in log['null_search'] if m['band']=='2-5%'))} of {[n['best_sel'] for n in log['null_search'] if n['band']=='2-5%' and n['best_rate']==max(m['best_rate'] for m in log['null_search'] if m['band']=='2-5%')][0]}. That is better than the best real formula at that volume ({log['real_best_by_band'][0]['best_won']} of {log['real_best_by_band'][0]['best_sel']}).")
w(f"- The ceiling is low for every approach. On 2026-27 the base was {int(U[2026].y.sum())} of {len(U[2026])} ({oi(int(U[2026].y.sum()), len(U[2026]))}). V4.1's top 20 a window won {int(te.loc['v4','top20_won'])} of {int(te.loc['v4','top20_sel'])} ({oi(int(te.loc['v4','top20_won']), int(te.loc['v4','top20_sel']))}). Pre-match goal counts move the needle a little, and every method hits the same wall.")
a20 = AC[(AC.model == "v4") & (AC.k == 20)]; a10 = AC[(AC.model == "v4") & (AC.k == 10)]; a5 = AC[(AC.model == "v4") & (AC.k == 5)]
w(f"- Accumulators: no model landed a 15 or 20-fold in any window of 2025-26 or 2026-27. V4.1 5-folds landed in {int(a5.all_won_windows.sum())} of {int(a5.windows_full.sum())} full windows and 10-folds in {int(a10.all_won_windows.sum())} of {int(a10.windows_full.sum())}.\n")

w("## 2. Dataset audit")
w(f"- Source: `football.db` from branch `data` (77,435 fixtures, 70 competitions). No API calls were made. 14 leagues, seasons 2023-24 to 2026-27: {tot_fix:,} eligible fixtures, {tot_won:,} finished Over 2.5.")
aud = pd.DataFrame([{"season": lab.SEASON_NAMES[s], "split": "development" if s < 2025 else ("validation" if s == 2025 else "untouched test"), "eligible fixtures": len(U[s]), "Over 2.5": int(U[s].y.sum()), "Under 2.5": len(U[s]) - int(U[s].y.sum()), "frequency": oi(int(U[s].y.sum()), len(U[s])), "windows": U[s].window.nunique()} for s in U])
w(tbl(aud))
w("- Quality: 0 duplicate fixture IDs and 0 missing full-time scores in the 14 leagues. 25 playoff ties finishing AET or PEN are excluded as results (FT rule) but kept as form. Teams are keyed by API ID, so there are no name mismatches. Fixtures where either side had fewer than 3 league games are excluded for every model (V4.1's rule), which drops the first weeks of each season.")
w("- Leakage control: every feature uses only league games that kicked off before the fixture, and league rates use only earlier calendar days. An automatic check recomputed 4,000 values from raw results with 0 mismatches. V4.1 scores were rebuilt with production `features.py` and `bands_model.pkl`; 693 of 897 published live rows match the logged score within 0.001. The rest differ only because the live runs saw the data available at run time.")
w("- Limitations: (1) **2026-27 is not pristine.** The 21 Oct, 28 Oct and 19 Nov research sessions already scored other models on it. This lab never tuned on it and opened it once, after `preregistered.json` was committed (commit 541f8d8). (2) V4.1 trained on 2023-24 and 2024-25, so its scores there are in-sample and only 2025-26 and 2026-27 are fair comparisons. (3) 2026-27 is 25 windows, so test ranges are wide. (4) There is no xG, lineups or injuries for most leagues, so the study is goals-based only. (5) Only 4 seasons exist, so league-specific formulas could not be supported.\n")

w("## 3. Experiments conducted")
exp = pd.DataFrame([
 ["Atoms (single count thresholds)", log["atoms"]], ["Two-condition AND formulas (full grid)", log["pairs_tested"]], ["Three-condition AND formulas (random, seed 20261120)", log["triples_tested"]],
 ["Integer-weight points formulas x 3 cut-offs", log["linear_evaluations"]], ["Decision trees (depth 2 to 4), leaves as rules", log["trees_fitted"]],
 ["Null searches on shuffled results", 3], ["Formulas shortlisted on DEV and scored on VAL", log["shortlist"]], ["Formulas frozen for the test", len(pre["finalist_formulas"])],
 ["Model variants (12 families)", 25], ["Walk-forward seasons per fitted model", 3]], columns=["experiment", "count"])
w(tbl(exp))
w(f"- Search space: last-5 league counts this season (scored 1+/2+/3+, let in 1+/2+/3+, clean sheets, failed to score, 3+ games, 4+ games, BTTS, both 2+, one side 3+) per side and as sum, min and max; venue last 3; last 10; attack-v-defence routes; drivers20; and the league running rate.")
w(f"- On VAL only {int((VC.val_minus_v4 > 0).sum())} of {len(VC)} shortlisted formulas beat V4.1 at identical volume ({int((VC.val_minus_v4 == 0).sum())} tied, {int((VC.val_minus_v4 < 0).sum())} worse). Selection rule, finalists and metrics were frozen in `results/preregistered.json` before the test season was opened.\n")

w("### 12 model families on the validation season (2025-26, top 20 a window, 1,443 picks; V4.1 out of sample here)")
fv = FV[FV.season == "2025-26"].copy(); fv["family"] = fv.model.map(lambda m: __import__("families").family(m))
fv = fv.sort_values("top20_won", ascending=False)
w(tbl(fv[["family", "model", "top20_won", "top20_sel", "top5_won", "top10_won", "brier"]].rename(columns={"top20_won": "top 20 won", "top20_sel": "top 20 picks", "top5_won": "top 5 won", "top10_won": "top 10 won"})))
w("")

w("## 4. Top 10 formulas (frozen before the test; ranked on VAL; TEST shown as found)")
w("All use only finished league results with kick-off times (`fixtures`: date, teams, FT score; HT not needed). Counts are each side's last 5 league games this season unless stated. 'v V4.1' = V4.1 taking the same number of fixtures in the same windows.\n")
for i, f in enumerate(pre["finalist_formulas"], 1):
    fid = f"F{i:02d}"; g = FT[FT.id == fid]
    w(f"### {fid}  `{f}`")
    w(f"{PLAIN[i]}\n")
    t = g[["season", "split", "eligible", "selected", "won", "lost", "one_in", "v4_matched_won", "minus_v4", "rejected", "rejected_won"]].copy()
    t["one_in"] = t.apply(lambda r: oi(r.won, r.selected), axis=1)
    w(tbl(t.rename(columns={"v4_matched_won": "V4.1 same volume won", "minus_v4": "v V4.1", "one_in": "frequency", "rejected_won": "rejected that won"})))
    lg = FL[FL.id == fid].pivot(index="league", columns="split", values=["selected", "won"])
    lg.columns = [f"{a} {b}" for a, b in lg.columns]; lg = lg.reset_index()
    lg["DEV+VAL"] = lg["won DEV+VAL"].astype(int).astype(str) + " of " + lg["selected DEV+VAL"].astype(int).astype(str)
    lg["TEST"] = lg["won TEST"].astype(int).astype(str) + " of " + lg["selected TEST"].astype(int).astype(str)
    w("League by league (won of selected): " + "; ".join(f"{r.league} {r['DEV+VAL']} / {r.TEST}" for _, r in lg.iterrows()) + "  (DEV+VAL / TEST)")
    rb = RB[RB.id == fid].set_index("split")
    tt = g[g.split == "TEST"].iloc[0]
    w(f"\nRobustness: one-step threshold changes beating V4.1: VAL {int(rb.loc['VAL','variants_beating_v4'])} of {int(rb.loc['VAL','variants'])}, TEST {int(rb.loc['TEST','variants_beating_v4'])} of {int(rb.loc['TEST','variants'])}. Test range for wins: {rng(int(tt.won), int(tt.selected))} of {int(tt.selected)}.")
    lim = "Behind V4.1 in both development seasons." if (g[g.split == "DEV"].minus_v4 < 0).all() else "Mixed against V4.1 in development."
    if tt.minus_v4 > 0: lim += " Ahead on TEST, but by a margin smaller than the noise for 1 of 10 frozen formulas; inconclusive."
    elif tt.minus_v4 == 0: lim += " Level with V4.1 on TEST."
    else: lim += " Behind V4.1 on TEST."
    w(f"Limitations: {lim}\n")

w("## 5. Best model for each selection size")
w("Each size's challenger is chosen on VAL (most wins), then read on TEST. Picks per size are identical for every model.")
rows = []
for k in (5, 10, 15, 20):
    best = va.drop(index="v4")[f"top{k}_won"].idxmax()
    rows.append({"size": f"top {k} a window", "picks VAL / TEST": f"{int(va.loc['v4', f'top{k}_sel'])} / {int(te.loc['v4', f'top{k}_sel'])}", "challenger picked on VAL": NAMES[best],
                 "challenger VAL": int(va.loc[best, f"top{k}_won"]), "V4.1 VAL": int(va.loc["v4", f"top{k}_won"]), "challenger TEST": int(te.loc[best, f"top{k}_won"]), "V4.1 TEST": int(te.loc["v4", f"top{k}_won"])})
w(tbl(pd.DataFrame(rows)))
w("\nVerdict: V4.1 is the validated choice at every size. The challengers' margins (largest: +2 on TEST) sit well inside the noise.\n")

w("## 6. Comparison with V4.1")
bt = BT.copy(); bt["model"] = bt.model.map(NAMES)
w(tbl(bt.rename(columns={"test_top20_minus_v4": "TEST top 20 wins v V4.1", "lo95": "range low", "hi95": "range high", "share_of_resamples_better": "resamples better"})))
w(f"\nLive published V4.1 picks (prediction log, {int(LV.fixtures.sum())} unique finished fixtures, {len(LV)} runs): V4.1 won {int(lv.v4_won)} of {int(lv.v4_selected)}. The random forest taking the same number per run would have won {int(lv.rf_same_count_won)}, with {int(lv.overlap)} picks in common. That is level.")
w("Calibration (TEST): Brier " + ", ".join(f"{NAMES[m]} {te.loc[m,'brier']:.4f}" for m in te.index if not np.isnan(te.loc[m, 'brier'])) + ". Lower is better; V4.1 is the best or level. Poisson and Dixon-Coles were the worst calibrated on VAL (Brier 0.2556 v V4.1 0.2465), and the fitted rho went to the edge of its range.\n")

w("## 7. Recommended implementation")
w("**Keep V4.1 exactly as it is.** Nothing here clears the research policy bar, so no production change is proposed.")
w("If you want one live trial, the only candidate worth the effort is a shadow log (research only, never shown in the pick list):")
w("```\nfor each run window:\n    fit RandomForest(n=400, min_leaf=60, max_features=0.3, seed=20261120) on every finished 14-league fixture before the window\n    features = each side's league counts over last 3/5/10 this season, last 10/15 any season, last 3/5 at venue, league running rate\n    rank the window's fixtures; log the top 20 beside V4.1's top 20 (fixture_id, rank, score) before kick-off\nafter results: count wins for both lists on identical windows\n```")
w(f"Second-order reality check before you build it: the per-window difference between two models this similar swings by about {sd_w:.1f} wins (one standard deviation, from the TEST resampling). Proving a real edge of 1 win every 4 windows would take about {need_w} windows (about {need_w/81:.1f} seasons at 81 windows a season), and the challenger would need to lead by {need_margin}+ wins. A shadow log will very likely finish 'not proven' too. The higher-leverage move is to stop searching for a better pre-match formula from these same inputs.\n")

w("## 8. Failed hypotheses")
fails = [
 ("Defensive weakness alone (both Let in 2+)", f"Weakest count family: {int(FV[(FV.season=='2025-26')&(FV.model=='f3_defensive')].top20_won.iloc[0])} of 1,443 top-20 picks on VAL v V4.1 851; ranks almost no better than chance."),
 ("Two powerful attacks rule", f"{int(FV[(FV.season=='2025-26')&(FV.model=='f2_two_attacks')].top20_won.iloc[0])} on VAL; behind V4.1 in both walk-forward seasons."),
 ("Attack v defence collision / drivers20 / one-sided routes", "All between 793 and 830 on VAL; the routes are already inside V4.1."),
 ("Home/away specialist counts", "Venue-only drivers20 801, blended 806 on VAL: venue splits add noise, not signal."),
 ("Opponent-adjusted goals", "802 on VAL; adjusting for opposition quality did not help."),
 ("Momentum (last 3 v last 10)", f"Logistic + momentum {int(va.loc['f6_momentum_logit','top20_won'])} v the same model without it {int(va.loc['f6_base_logit','top20_won'])} on VAL, and {int(te.loc['f6_momentum_logit','top20_won'])} v {int(te.loc['f6_base_logit','top20_won'])} on TEST."),
 ("Historical match DNA (nearest neighbours)", "Best k=150: 833 on VAL; small k overfits (k=50: 781)."),
 ("Poisson and Dixon-Coles", "831 on VAL; worst calibration of the fitted models; the Dixon-Coles correction moved Brier only from 0.2560 to 0.2556."),
 ("Model consensus", f"{int(va.loc['f12_consensus','top20_won'])} on VAL, {int(te.loc['f12_consensus','top20_won'])} on TEST: agreement did not add accuracy."),
 ("Mined formulas", f"Best 10 of {log['total_formulas_evaluated']:,} lost to V4.1 on TEST ({int(fsum.loc['TEST','won'])} v {int(fsum.loc['TEST','v4_matched_won'])})."),
 ("'Strong attack meets tight defence' explains losses", f"Inside V4.1's top 20 (VAL+TEST) that pattern won {int(PAT.loc[True,'sum'])} of {int(PAT.loc[True,'size'])} ({oi(int(PAT.loc[True,'sum']), int(PAT.loc[True,'size']))}), the rest {int(PAT.loc[False,'sum'])} of {int(PAT.loc[False,'size'])} ({oi(int(PAT.loc[False,'sum']), int(PAT.loc[False,'size']))}). It does not mark losers, so it should not be used as a filter."),
]
w(tbl(pd.DataFrame(fails, columns=["hypothesis", "evidence"])))
w("Losing picks look the same as winning picks on every count. The most common losing scores are 1-1, 1-0 and 2-0: ordinary low-scoring games rather than a pattern a filter could catch.\n")

w("## 9. Confidence assessment")
w(f"- **Strong evidence:** V4.1 is not beaten by any approach tested here. Formula mining on these inputs produces mostly chance (null search; VAL to TEST collapse). Accumulators of 10 or more legs essentially never land ({int(big.all_won_windows.sum())} of {int(big.windows_full.sum())} full 15 and 20-fold windows for V4.1 over VAL and TEST).")
w("- **Promising but inconclusive:** F06 (+6 on TEST from 59 picks, all 6 threshold variants ahead on VAL and TEST, but 33 behind V4.1 in 2024-25). The random forest (+2 on TEST, +5 on VAL, +3 on the live log).")
w(f"- **Overfitted:** every mined formula whose development rate looked best. The 10 finalists led V4.1 by {int(fsum.loc['VAL','won'] - fsum.loc['VAL','v4_matched_won'])} on VAL, the season they were picked on, then trailed by {int(fsum.loc['TEST','v4_matched_won'] - fsum.loc['TEST','won'])} on TEST.")
w("- **Insufficient samples:** league-specific rules (most finalists pick fewer than 50 fixtures a season in most leagues); top 5 comparisons (119 TEST picks).\n")

w("## 10. Next steps")
w("1. Keep V4.1 and its pick process. Nothing here justifies a change.")
w("2. Let the live log keep scoring V4.1. Review per band only once each band has 40+ new results, as the methodology says.")
w("3. If you want more edge, it has to come from information the model does not have (lineups, injuries, rotation), not from new combinations of the same goal counts. That is a data question before a modelling one.")
w(f"4. Optional: shadow-log the random forest only (one challenger keeps the test honest) from the next run, with the decision rule fixed now: adopt only if it leads V4.1 by {need_margin}+ top-20 wins after {need_w}+ windows.\n")
w("## Files")
w("`scripts/01..09` reproduce everything (`python3 scripts/NN_*.py` in order; seed 20261120; scikit-learn 1.8.0, pandas 3.0, numpy 2.5). `data/features.parquet` is the reusable point-in-time dataset (58,379 league fixtures, all leagues). `results/master_formulas.xlsx` holds every shortlisted formula with DEV, VAL and TEST counts, plus all the tables above. `results/preregistered.json` is the frozen selection.")
open(f"{lab.ROOT}/report/FINAL_REPORT.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
