"""12_rob_logic.py - Rob's stated picking logic (23 Nov 2026) as exact count rules, tested on Sat-Sun fixtures, 14 leagues."""
import numpy as np, pandas as pd
import lab
X = lab.load(); U = lab.universe(X, [2023, 2024, 2025, 2026]).copy()
ko = pd.to_datetime(U.kickoff_utc, utc=True).dt.tz_convert("Europe/London")
U = U[ko.dt.weekday >= 5].copy(); ko = ko[U.index]
U["wk"] = (ko.dt.normalize() - pd.to_timedelta(ko.dt.weekday, unit="D")).dt.date
U["fair"] = U.season.isin([2025, 2026]); U["pool"] = U.v4_score >= 0.58084
cs_max = np.maximum(U.h_S5_cs, U.a_S5_cs)
U["veto3cs"] = cs_max >= 3; U["flag2cs"] = cs_max == 2
U["att_ok"] = (U.h_S5_s2 >= 3) & (U.a_S5_s2 >= 3)
U["def_ok"] = (U.h_S5_c2 >= 3) & (U.a_S5_c2 >= 3)
U["gate"] = U.att_ok & U.def_ok & ~U.veto3cs
U["drivers"] = U.h_S5_s2 + U.a_S5_s2 + U.h_S5_c2 + U.a_S5_c2
U["o3"] = U.h_S5_o25 + U.a_S5_o25; U["btts"] = U.h_S5_btts + U.a_S5_btts; U["ven"] = U.h_V3_o25 + U.a_V3_o25
U["route"] = np.maximum(np.minimum(U.h_S5_s2, U.a_S5_c2), np.minimum(U.a_S5_s2, U.h_S5_c2))
def show(nm, m, g):
    k = int(g.y[m].sum()); n = int(m.sum()); r = f"{k} of {n} (1 in {n/k:.2f})" if k else f"0 of {n}"
    return f"{nm}: {r}"
for lab_, g in (("FAIR SEASONS 2025-26 + 2026-27", U[U.fair]), ("ALL FOUR SEASONS", U)):
    print(f"\n== {lab_}: {g.wk.nunique()} weekends, {len(g)} fixtures, base {int(g.y.sum())} won (1 in {len(g)/g.y.sum():.2f})")
    print(" ", show("either side 3+ clean sheets", g.veto3cs, g), "|", show("neither", ~g.veto3cs, g))
    print(" ", show("either side exactly 2 clean sheets (max)", g.flag2cs, g), "|", show("max 0 or 1", (~g.veto3cs) & (~g.flag2cs), g))
    print(" ", show("both sides scored 2+ in 3+ of 5", g.att_ok, g), "|", show("not", ~g.att_ok, g))
    print(" ", show("both sides let in 2+ in 3+ of 5", g.def_ok, g), "|", show("not", ~g.def_ok, g))
    print(" ", show("FULL GATE (both attack and both defence 3+, no side 3+ clean sheets)", g.gate, g))
    print(" ", show("V4.1 pool", g.pool, g), "|", show("V4.1 pool that also passes the gate", g.pool & g.gate, g), "|", show("gate but NOT in V4.1 pool", g.gate & ~g.pool, g))
    per = g.groupby("wk").gate.sum(); print(f"  gate fixtures per weekend: fewest {per.min()}, most {per.max()}, weekends with 20+: {(per>=20).sum()}, weekends with under 10: {(per<10).sum()}")
    # matched volume: in each weekend take the same NUMBER of fixtures V4.1 ranks highest
    w_gate = int(g.y[g.gate].sum()); v = 0
    for wk, gg in g.groupby("wk"):
        n = int(gg.gate.sum()); v += int(gg.sort_values(["v4_score", "fixture_id"], ascending=[False, True]).head(n).y.sum())
    print(f"  gate picks {w_gate} won v V4.1's top picks in the same number per weekend: {v} won (same {int(g.gate.sum())} fixtures)")
    # Rob's ranker: no 3+ clean sheets, rank by drivers, then 3+ games, then venue, then BTTS
    g = g.copy(); g["rob"] = np.where(g.veto3cs, -99, g.drivers * 1000 + g.o3 * 100 + g.ven * 10 + g.btts)
    g["rob_route"] = np.where(g.veto3cs, -99, g.route * 10000 + g.drivers * 1000 + g.o3 * 100 + g.ven * 10 + g.btts)
    for k in (5, 10, 15, 20):
        a = g.sort_values(["v4_score", "fixture_id"], ascending=[False, True]).groupby("wk").head(k)
        b = g.sort_values(["rob", "v4_score"], ascending=[False, False]).groupby("wk").head(k)
        c = g.sort_values(["rob_route", "v4_score"], ascending=[False, False]).groupby("wk").head(k)
        print(f"  top {k:2d}: V4.1 {int(a.y.sum())} of {len(a)} | Rob's order {int(b.y.sum())} of {len(b)} | Rob's order + matched route first {int(c.y.sum())} of {len(c)}")
print("\n== V4.1 pool, both-attacks-3-of-5 fixtures chosen first, then V4.1 order")
for lab_, g in (("fair", U[U.fair]), ("all four", U)):
    out = []
    for k in (5, 10, 15, 20):
        a = g.sort_values(["v4_score", "fixture_id"], ascending=[False, True]).groupby("wk").head(k)
        gg = g.assign(pref=np.where(g.pool & g.att_ok, 1, 0)).sort_values(["pref", "v4_score"], ascending=[False, False]).groupby("wk").head(k)
        out.append(f"top{k} {int(gg.y.sum())} v V4.1 {int(a.y.sum())}")
    print(" ", lab_, " | ".join(out))
