"""11_v42_rob_weights.py - V4.2 candidate: Rob's own weights (23 Nov 2026) on counts only, no training.
Each factor is a count from both sides' last 5 league games this season (venue: last 3 at venue), scaled 0 to 1 by its
maximum; clean sheets and failed to score count against. Compared with V4.1 on Saturday-Sunday fixtures, Rob's 14 leagues."""
import numpy as np, pandas as pd, json
import lab
from sklearn.linear_model import LogisticRegression
W = {"Games with 3+": 20, "Scored 2+": 15, "Let in 2+": 15, "Goals in their games": 11, "Failed to score": 11,
     "Clean sheets": 11, "Both teams scored": 7, "Home at home / away away": 6, "League scoring rate": 3}

def factors(d):
    lr = np.where(d.lg_n >= 30, d.lg_o25 / d.lg_n.replace(0, np.nan), d.pl_o / d.pl_n)
    return pd.DataFrame({
        "Games with 3+": (d.h_S5_o25 + d.a_S5_o25) / 10,
        "Scored 2+": (d.h_S5_s2 + d.a_S5_s2) / 10,
        "Let in 2+": (d.h_S5_c2 + d.a_S5_c2) / 10,
        "Goals in their games": np.minimum((d.h_S5_g + d.a_S5_g) / 40, 1),
        "Failed to score": -(d.h_S5_fts + d.a_S5_fts) / 10,
        "Clean sheets": -(d.h_S5_cs + d.a_S5_cs) / 10,
        "Both teams scored": (d.h_S5_btts + d.a_S5_btts) / 10,
        "Home at home / away away": (d.h_V3_o25 + d.a_V3_o25) / 6,
        "League scoring rate": np.nan_to_num(lr, nan=0.53)}, index=d.index).fillna(0)

X = lab.load(); U = lab.universe(X, [2023, 2024, 2025, 2026]).copy()
Fz = factors(U)
U["v42"] = sum(W[k] * Fz[k] for k in W)
# reference: same 9 count factors, weights chosen by the data (fitted on 2023-24 + 2024-25 only)
tr = U.season.isin([2023, 2024]); m = LogisticRegression(max_iter=3000).fit(Fz[tr], U.y[tr]); U["data_weights"] = m.decision_function(Fz)
ko = pd.to_datetime(U.kickoff_utc, utc=True).dt.tz_convert("Europe/London")
U = U[ko.dt.weekday >= 5].copy(); ko = ko[U.index]
U["wk"] = (ko.dt.normalize() - pd.to_timedelta(ko.dt.weekday, unit="D")).dt.date
rows = []
for s, g in U.groupby("season"):
    for mname in ("v4_score", "v42", "data_weights"):
        r = {"season": lab.SEASON_NAMES[s], "model": {"v4_score": "V4.1", "v42": "V4.2 (Rob's weights)", "data_weights": "Same counts, data's weights"}[mname], "weekends": g.wk.nunique()}
        for k in (5, 10, 15, 20):
            t = g.sort_values([mname, "fixture_id"], ascending=[False, True]).groupby("wk").head(k)
            r[f"top{k}"] = int(t.y.sum()); r[f"top{k}_n"] = len(t)
        rows.append(r)
R = pd.DataFrame(rows)
R.to_csv(f"{lab.ROOT}/results/v42_rob_weights_by_season.csv", index=False)
for _, r in R.iterrows():
    print(f"{r.season} {r.model:28s} " + "  ".join(f"top{k} {r[f'top{k}']} of {r[f'top{k}_n']}" for k in (5, 10, 15, 20)))
rng = np.random.default_rng(1)
for seasons, lab_ in (([2025, 2026], "fair seasons (2025-26 + 2026-27)"), ([2023, 2024, 2025, 2026], "all four seasons")):
    g = U[U.season.isin(seasons)]; d = []
    for _, w in g.groupby("wk"):
        a = w.sort_values(["v4_score", "fixture_id"], ascending=[False, True]).head(20).y.sum()
        b = w.sort_values(["v42", "fixture_id"], ascending=[False, True]).head(20).y.sum(); d.append(b - a)
    d = np.array(d); bs = [d[rng.integers(0, len(d), len(d))].sum() for _ in range(5000)]
    print(f"top 20, V4.2 minus V4.1, {lab_}: {d.sum()} over {len(d)} weekends (95% range {np.percentile(bs,2.5):.0f} to {np.percentile(bs,97.5):.0f}); better {int((d>0).sum())}, same {int((d==0).sum())}, worse {int((d<0).sum())}")
print("data's own weights on the same counts (relative, positive = more goals):", {k: round(float(c), 2) for k, c in zip(W, m.coef_[0])})
# counts only, team v team, NO league rate, weights chosen by the data on 2023-24 + 2024-25
FT = [k for k in W if k != "League scoring rate"]
Xa = lab.universe(X, [2023, 2024, 2025, 2026]).copy(); Fa = factors(Xa)
tr = Xa.season.isin([2023, 2024]); m2 = LogisticRegression(max_iter=3000).fit(Fa.loc[tr, FT], Xa.y[tr])
U["team_only"] = m2.decision_function(factors(U)[FT])
for s, g in U.groupby("season"):
    r = []
    for k in (5, 10, 15, 20):
        a = g.sort_values(["v4_score", "fixture_id"], ascending=[False, True]).groupby("wk").head(k).y.sum()
        b = g.sort_values(["team_only", "fixture_id"], ascending=[False, True]).groupby("wk").head(k).y.sum()
        r.append(f"top{k} {b} v V4.1 {a}")
    print(lab.SEASON_NAMES[s], "counts, team only, data weights:", " | ".join(r))
g = U[U.season.isin([2025, 2026])]; d = []
for _, w in g.groupby("wk"):
    d.append(w.sort_values(["team_only", "fixture_id"], ascending=[False, True]).head(20).y.sum() - w.sort_values(["v4_score", "fixture_id"], ascending=[False, True]).head(20).y.sum())
d = np.array(d); bs = [d[rng.integers(0, len(d), len(d))].sum() for _ in range(5000)]
print(f"top 20 team-only counts minus V4.1, fair seasons: {d.sum()} (95% range {np.percentile(bs,2.5):.0f} to {np.percentile(bs,97.5):.0f}); better {int((d>0).sum())}, same {int((d==0).sum())}, worse {int((d<0).sum())}")
co = dict(zip(FT, m2.coef_[0])); tot = sum(abs(v) for v in co.values())
print("team-only data weights out of 100 (sign = more or fewer goals):", {k: round(v / tot * 100) for k, v in sorted(co.items(), key=lambda kv: -abs(kv[1]))})
