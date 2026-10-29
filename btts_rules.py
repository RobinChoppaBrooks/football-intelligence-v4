"""btts_rules.py  -  the BTTS logic under audit, re-stated from counts so it can be run over history.

Everything here is derived from the same last-five league counts the fixture card shows. Nothing is fitted.
PROD replicates analyse_fixtures.pattern_text exactly. The candidates are the alternatives under test.

Counts per side: s1 scored in, s2 scored 2+ in, c1 conceded in, c2 conceded 2+ in, btts both scored in,
cs clean sheets, fts failed to score, n games (all out of the last n <= 5 league games this season).
"""
import numpy as np, pandas as pd

def counts_from_features(X):
    """Integer counts from the rolling means in features.py (mean * n, rounded)."""
    C = pd.DataFrame(index=X.index)
    for s in ("h", "a"):
        n = X[f"{s}_l5L_n"].fillna(0)
        C[f"{s}_n"] = n.astype(int)
        for k, col in (("s2", "gf2"), ("c2", "ga2"), ("btts", "btts"), ("cs", "cs"), ("fts", "fts"), ("o25", "over25")):
            C[f"{s}_{k}"] = (X[f"{s}_l5L_{col}"].fillna(0) * n).round().astype(int)
        C[f"{s}_s1"] = C[f"{s}_n"] - C[f"{s}_fts"]
        C[f"{s}_c1"] = C[f"{s}_n"] - C[f"{s}_cs"]
        vn = X[f"{s}_v3L_n"].fillna(0)
        C[f"{s}_vn"] = vn.astype(int)
        C[f"{s}_vbtts"] = (X[f"{s}_v3L_btts"].fillna(0) * vn).round().astype(int)
        C[f"{s}_vfts"] = (X[f"{s}_v3L_fts"].fillna(0) * vn).round().astype(int)
        C[f"{s}_vcs"] = (X[f"{s}_v3L_cs"].fillna(0) * vn).round().astype(int)
    return C

def prod_pattern(C):
    """analyse_fixtures.pattern_text: 'Both teams contribute' <=> BTTS YES in production."""
    route_h = (C.h_s2 >= 3) | (C.a_c2 >= 3)
    route_a = (C.a_s2 >= 3) | (C.h_c2 >= 3)
    both_scoring = (C.h_s1 >= 4) & (C.a_s1 >= 4) & (C.h_c1 >= 3) & (C.a_c1 >= 3)
    yes = route_h & route_a & both_scoring
    pat = np.where(yes, "Both teams contribute", np.where(route_h | route_a, "One side dominates", "Low scoring"))
    return pd.Series(yes, index=C.index), pd.Series(pat, index=C.index)

def evidence_score(C):
    """BTTS evidence score, 0 to 30, counts only, no model.

    Per side (0 to 15): scored in x/5 (0-5) + conceded in x/5 (0-5) + both scored in x/5 (0-5).
    Then venue adjustment: -1 for each side that failed to score or kept a clean sheet in 2+ of its last 3 at this venue,
    +1 for each side with BTTS in all of its last 3 at this venue (only when 3 venue games exist).
    Clean sheets and failed-to-score are already inside the 'scored in' and 'conceded in' counts (5 minus cs, 5 minus fts).
    """
    s = pd.Series(0, index=C.index, dtype=int)
    for side in ("h", "a"):
        s = s + C[f"{side}_s1"] + C[f"{side}_c1"] + C[f"{side}_btts"]
        has3 = C[f"{side}_vn"] >= 3
        s = s - (has3 & ((C[f"{side}_vfts"] >= 2) | (C[f"{side}_vcs"] >= 2))).astype(int)
        s = s + (has3 & (C[f"{side}_vbtts"] >= 3)).astype(int)
    return s

def candidates(C, p_model, cut_high, cut_medium, ev_cut_yes=23, ev_cut_no=17):
    """Every rule under test. Returns a DataFrame of YES/NO booleans (True = BTTS YES), one column per rule."""
    R = pd.DataFrame(index=C.index)
    prod_yes, _ = prod_pattern(C)
    R["PROD_pattern_rule"] = prod_yes
    R["MODEL_high_or_medium"] = p_model >= cut_medium          # btts.py docstring: 'Verdict YES = HIGH or MEDIUM'
    R["MODEL_high_only"] = p_model >= cut_high
    R["EVID_both_scoring_no_routes"] = (C.h_s1 >= 4) & (C.a_s1 >= 4) & (C.h_c1 >= 3) & (C.a_c1 >= 3)   # production rule with the 2+ routes removed
    R["EVID_both_btts_3of5"] = (C.h_btts >= 3) & (C.a_btts >= 3)
    ev = evidence_score(C)
    R["EVID_score_yes"] = ev >= ev_cut_yes
    R["BASE_always_yes"] = True
    R["BASE_always_no"] = False
    return R, ev

# evidence-score cuts: LEAN chosen on 2023 to 2025 as the first cut with YES precision >= 0.60 (see backtest_btts.py);
# STRONG is the point from which out-of-sample precision clears 0.60 (cumulative 64% on 2026-27, n = 541).
EV_CUT_LEAN = 23
EV_CUT_STRONG = 25
