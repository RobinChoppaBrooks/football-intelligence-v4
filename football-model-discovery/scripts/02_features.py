"""02_features.py - point-in-time feature library for the Over 2.5 discovery lab.

Every feature for a fixture is built only from league matches that kicked off BEFORE it (shift(1) inside each team's
ordered history; league baselines use strictly earlier calendar days). Counts, not averages, wherever possible.

Usage: python3 -I scripts/02_features.py <football.db> <out.parquet>
"""
import sys, sqlite3, numpy as np, pandas as pd

ROB14 = [39, 40, 41, 42, 43, 50, 51, 78, 88, 61, 203, 179, 140, 94]
FORM_STATUS = ("FT", "AET", "PEN")          # past games used for form (as production)
METRICS = ["gf", "ga", "s1", "s2", "s3", "fts", "c1", "c2", "c3", "cs", "o15", "o25", "o35", "btts", "one3", "both2", "sbh", "g"]
WIN_S = [3, 5, 10, 15]     # this season, league only, any venue
WIN_X = [10, 15]           # league only, rolling across seasons
WIN_V = [3, 5]             # this season, league only, at this venue


def load(db):
    c = sqlite3.connect(db)
    fx = pd.read_sql("""SELECT f.fixture_id, f.league_id, f.season, f.kickoff_utc, f.home_id, f.away_id, f.status,
                        f.ht_home, f.ht_away, f.ft_home, f.ft_away, cp.is_cup, cp.name comp
                        FROM fixtures f JOIN competitions cp ON cp.league_id=f.league_id""", c)
    tn = pd.read_sql("SELECT team_id, name FROM teams", c); c.close()
    fx["kickoff_utc"] = pd.to_datetime(fx.kickoff_utc, utc=True)
    fx = fx[(fx.is_cup == 0) & fx.status.isin(FORM_STATUS) & fx.ft_home.notna() & fx.ft_away.notna()].copy()
    return fx.sort_values(["kickoff_utc", "fixture_id"]).reset_index(drop=True), tn


def long_table(fx):
    parts = []
    for v, me, op, gf, ga, hf, ha in (("H", "home_id", "away_id", "ft_home", "ft_away", "ht_home", "ht_away"),
                                      ("A", "away_id", "home_id", "ft_away", "ft_home", "ht_away", "ht_home")):
        d = fx[["fixture_id", "league_id", "season", "kickoff_utc", me, op, gf, ga, hf, ha]].copy()
        d.columns = ["fixture_id", "league_id", "season", "kickoff_utc", "team_id", "opp_id", "gf", "ga", "htf", "hta"]
        d["venue"] = v; parts.append(d)
    L = pd.concat(parts, ignore_index=True)
    t = L.gf + L.ga
    L["s1"] = L.gf >= 1; L["s2"] = L.gf >= 2; L["s3"] = L.gf >= 3; L["fts"] = L.gf == 0
    L["c1"] = L.ga >= 1; L["c2"] = L.ga >= 2; L["c3"] = L.ga >= 3; L["cs"] = L.ga == 0
    L["o15"] = t >= 2; L["o25"] = t >= 3; L["o35"] = t >= 4; L["btts"] = (L.gf > 0) & (L.ga > 0)
    L["one3"] = (L.gf >= 3) | (L.ga >= 3); L["both2"] = (L.gf >= 2) & (L.ga >= 2)
    L["sbh"] = ((L.htf > 0) & ((L.gf - L.htf) > 0)).where(L.htf.notna(), np.nan)   # scored in both halves
    L["g"] = t
    for m in METRICS:
        L[m] = L[m].astype(float)
    L = L.sort_values(["kickoff_utc", "fixture_id"]).reset_index(drop=True)
    # opponent strength BEFORE each past game: opponent's season-to-date league goals for / against per game
    L["_k"] = L.team_id.astype(str) + "_" + L.season.astype(str)
    g = L.groupby("_k")
    n_pre = g.cumcount()
    L["gf_rate_pre"] = (g.gf.cumsum() - L.gf) / n_pre.replace(0, np.nan)
    L["ga_rate_pre"] = (g.ga.cumsum() - L.ga) / n_pre.replace(0, np.nan)
    opp = L[["fixture_id", "team_id", "gf_rate_pre", "ga_rate_pre"]].rename(
        columns={"team_id": "opp_id", "gf_rate_pre": "opp_gf_rate", "ga_rate_pre": "opp_ga_rate"})
    L = L.merge(opp, on=["fixture_id", "opp_id"], how="left")
    # opponent-adjusted goals: what the team scored minus what that opponent usually concedes (and vice versa)
    L["adj_gf"] = L.gf - L.opp_ga_rate
    L["adj_ga"] = L.ga - L.opp_gf_rate
    return L.drop(columns="_k")


def prev_window_sums(L, key, cols, n):
    """sum of each col over the previous n rows in the group (excluding the current row)."""
    L = L.sort_values(["kickoff_utc", "fixture_id"])
    g = L.groupby(key, sort=False)
    out = {}
    cnt = g.cumcount()                        # number of earlier rows in group
    out["n"] = np.minimum(cnt, n)
    for c in cols:
        v = L[c].fillna(0.0)
        cs = v.groupby(L[key]).cumsum()
        before = cs - v                        # sum of all earlier rows
        lag = before.groupby(L[key]).shift(n).fillna(0.0)   # sum of rows earlier than the last n
        # shift(n) of "before" = sum through row i-n-1 ... correct: before_i - before_{i-n} = rows i-n .. i-1
        out[c] = before - lag
    D = pd.DataFrame(out, index=L.index)
    return D.reindex(sorted(D.index))


def team_feats(L):
    L = L.sort_values(["kickoff_utc", "fixture_id"]).reset_index(drop=True)
    L["k_s"] = L.team_id.astype(str) + "_" + L.season.astype(str)
    L["k_x"] = L.team_id.astype(str)
    L["k_v"] = L.k_s + "_" + L.venue
    F = [L[["fixture_id", "team_id", "venue"]]]
    cols = METRICS + ["adj_gf", "adj_ga"]
    for n in WIN_S:
        D = prev_window_sums(L, "k_s", cols, n); F.append(D.add_prefix(f"S{n}_"))
    for n in WIN_X:
        D = prev_window_sums(L, "k_x", cols, n); F.append(D.add_prefix(f"X{n}_"))
    for n in WIN_V:
        D = prev_window_sums(L, "k_v", cols, n); F.append(D.add_prefix(f"V{n}_"))
    # season-to-date (this season, league) totals: games, goals for/against
    g = L.groupby("k_s")
    F.append(pd.DataFrame({"STD_n": g.cumcount(), "STD_gf": g.gf.cumsum() - L.gf, "STD_ga": g.ga.cumsum() - L.ga}))
    return pd.concat(F, axis=1)


def league_base(fx):
    """league-season goals and O2.5 counts from matches on strictly earlier calendar days, plus last season's totals."""
    d = fx[["fixture_id", "league_id", "season", "kickoff_utc", "ft_home", "ft_away"]].copy()
    d["day"] = d.kickoff_utc.dt.floor("D")
    d["g"] = d.ft_home + d.ft_away; d["o"] = (d.g >= 3).astype(float); d["hg"] = d.ft_home; d["ag"] = d.ft_away; d["one"] = 1.0
    day = d.groupby(["league_id", "season", "day"])[["g", "o", "hg", "ag", "one"]].sum().reset_index()
    day = day.sort_values("day")
    for c in ["g", "o", "hg", "ag", "one"]:
        day[f"cb_{c}"] = day.groupby(["league_id", "season"])[c].cumsum() - day[c]
    d = d.merge(day[["league_id", "season", "day"] + [f"cb_{c}" for c in ["g", "o", "hg", "ag", "one"]]], on=["league_id", "season", "day"])
    prev = d.groupby(["league_id", "season"]).agg(pl_n=("one", "sum"), pl_o=("o", "sum"), pl_g=("g", "sum"), pl_hg=("hg", "sum"), pl_ag=("ag", "sum")).reset_index()
    prev["season"] += 1
    d = d.merge(prev, on=["league_id", "season"], how="left")
    return d[["fixture_id", "cb_one", "cb_o", "cb_g", "cb_hg", "cb_ag", "pl_n", "pl_o", "pl_g", "pl_hg", "pl_ag"]].rename(
        columns={"cb_one": "lg_n", "cb_o": "lg_o25", "cb_g": "lg_goals", "cb_hg": "lg_hgoals", "cb_ag": "lg_agoals"})


def build(db):
    fx, tn = load(db)
    L = long_table(fx)
    T = team_feats(L)
    H = T[T.venue == "H"].drop(columns=["venue"]).add_prefix("h_").rename(columns={"h_fixture_id": "fixture_id"})
    A = T[T.venue == "A"].drop(columns=["venue"]).add_prefix("a_").rename(columns={"a_fixture_id": "fixture_id"})
    X = fx.merge(H, on="fixture_id").merge(A, on="fixture_id").merge(league_base(fx), on="fixture_id", how="left")
    X = X.merge(tn.rename(columns={"team_id": "home_id", "name": "home"}), on="home_id", how="left")
    X = X.merge(tn.rename(columns={"team_id": "away_id", "name": "away"}), on="away_id", how="left")
    X["total"] = X.ft_home + X.ft_away
    X["y"] = (X.total >= 3).astype(int)
    X["eval_ok"] = X.status == "FT"          # Rob: a result counts only if FT (AET/PEN playoffs excluded)
    X["rob14"] = X.league_id.isin(ROB14)
    ld = X.kickoff_utc.dt.tz_convert("Europe/London")
    X["date_uk"] = ld.dt.date.astype(str)
    # betting windows: weekend = Fri-Sun, midweek = Mon-Thu; window id = the Monday of that week + type
    wd = ld.dt.weekday
    monday = (ld.dt.normalize() - pd.to_timedelta(wd, unit="D")).dt.date.astype(str)
    X["window"] = np.where(wd >= 4, monday + "_WE", monday + "_MW")
    return X.sort_values(["kickoff_utc", "fixture_id"]).reset_index(drop=True)


def leakage_test(db, X, n=400, seed=1):
    """recompute S5 goals for/against and S5 clean sheets straight from the raw table for random fixtures."""
    fx, _ = load(db)
    rng = np.random.default_rng(seed); bad = 0; chk = 0
    S = X.sample(n, random_state=seed)
    for _, r in S.iterrows():
        for side, tid in (("h", r.home_id), ("a", r.away_id)):
            prev = fx[((fx.home_id == tid) | (fx.away_id == tid)) & (fx.season == r.season) & (fx.kickoff_utc < r.kickoff_utc)].tail(5)
            gf = np.where(prev.home_id == tid, prev.ft_home, prev.ft_away)
            ga = np.where(prev.home_id == tid, prev.ft_away, prev.ft_home)
            for col, val in ((f"{side}_S5_gf", gf.sum()), (f"{side}_S5_ga", ga.sum()), (f"{side}_S5_cs", (ga == 0).sum()), (f"{side}_S5_n", len(prev)), (f"{side}_S5_s2", (gf >= 2).sum())):
                chk += 1; bad += abs(r[col] - val) > 1e-9
    print(f"leakage test: {chk} values recomputed from raw results, {bad} mismatches")
    return bad


if __name__ == "__main__":
    db, out = sys.argv[1:3]
    X = build(db)
    X.to_parquet(out, compression="zstd")
    print(f"{len(X)} league fixtures, {X.shape[1]} columns -> {out}")
    print(X[X.rob14].groupby("season").agg(n=("y", "size"), over=("y", "sum")))
    b = leakage_test(db, X[X.rob14])
    sys.exit(1 if b else 0)
