"""
features.py  -  Phase 2. One row per fixture, every feature computed from matches that kicked off strictly before it.

    python3 features.py football.db            -> features.pkl and features.csv next to the db
    python3 features.py football.db --test     -> also runs the leakage test on 300 random rows

Windows: season-to-date at venue (league matches only), last 5 and last 10 at any venue and any competition,
last 5 at venue. Rates are per game. Nothing is imputed: a missing stat stays NaN and has_* flags say why.
"""
import sys, os, sqlite3, numpy as np, pandas as pd

FINISHED = ("FT", "AET", "PEN")
STAT_COLS = ["shots", "shots_on_target", "shots_inside_box", "corners", "xg"]

def load(db, upcoming_to=None):
    c = sqlite3.connect(db)
    fx = pd.read_sql(f"""SELECT f.*, cp.is_cup, cp.name comp FROM fixtures f JOIN competitions cp ON cp.league_id=f.league_id""", c, parse_dates=["kickoff_utc"])
    st = pd.read_sql(f"SELECT fixture_id, team_id, {','.join(STAT_COLS)} FROM fixture_stats", c)
    c.close()
    keep = fx.status.isin(FINISHED) & fx.ft_home.notna() & fx.ft_away.notna()
    if upcoming_to is not None:
        keep |= (fx.status == "NS") & (pd.to_datetime(fx.kickoff_utc, utc=True) <= pd.Timestamp(upcoming_to, tz="UTC"))
    fx = fx[keep].copy()
    fx["kickoff_utc"] = pd.to_datetime(fx.kickoff_utc, utc=True)
    return fx.sort_values("kickoff_utc").reset_index(drop=True), st

def long_table(fx, st):
    """One row per team per match with for/against goals and stats."""
    rows = []
    for venue, me, opp, gf, ga in (("H", "home_id", "away_id", "ft_home", "ft_away"), ("A", "away_id", "home_id", "ft_away", "ft_home")):
        d = fx[["fixture_id", "kickoff_utc", "season", "league_id", "is_cup", me, opp, gf, ga, "ht_home", "ht_away"]].copy()
        d.columns = ["fixture_id", "kickoff_utc", "season", "league_id", "is_cup", "team_id", "opp_id", "gf", "ga", "ht_home", "ht_away"]
        d["venue"] = venue
        rows.append(d)
    L = pd.concat(rows, ignore_index=True)
    own = st.rename(columns={c: f"{c}_f" for c in STAT_COLS})
    opp = st.rename(columns={"team_id": "opp_id", **{c: f"{c}_a" for c in STAT_COLS}})
    L = L.merge(own, on=["fixture_id", "team_id"], how="left").merge(opp, on=["fixture_id", "opp_id"], how="left")
    tot = L.gf + L.ga
    L["over25"] = (tot >= 3).astype(float); L["btts"] = ((L.gf > 0) & (L.ga > 0)).astype(float)
    L["cs"] = (L.ga == 0).astype(float); L["fts"] = (L.gf == 0).astype(float); L["tot"] = tot.astype(float)
    L["gf2"] = (L.gf >= 2).astype(float); L["ga2"] = (L.ga >= 2).astype(float); L["gf3"] = (L.gf >= 3).astype(float); L["ga3"] = (L.ga >= 3).astype(float)
    L["tot4"] = (tot >= 4).astype(float)
    L["htg"] = ((L.ht_home.fillna(-1) + L.ht_away.fillna(-1)) > 0).astype(float).where(L.ht_home.notna() & L.ht_away.notna())
    for col in ("over25","btts","cs","fts","gf2","ga2","gf3","ga3","tot4","htg"): L.loc[L.gf.isna(), col] = np.nan
    # opponent quality: the opponent's league goals-for per game before this match (season-to-date, shifted)
    L = L.sort_values(["team_id", "kickoff_utc"]).reset_index(drop=True)
    key = L.team_id.astype(str) + "_" + L.season.astype(str)
    lg = L[L.is_cup == 0]
    pre = lg.groupby(key[lg.index])["gf"].transform(lambda x: x.shift(1).expanding().mean())
    L["own_gf_pre"] = pre
    opp_pre = L[["fixture_id", "team_id", "own_gf_pre"]].rename(columns={"team_id": "opp_id", "own_gf_pre": "opp_gf_pre"})
    L = L.merge(opp_pre, on=["fixture_id", "opp_id"], how="left")
    L["has_stats"] = L.shots_f.notna().astype(float); L["has_xg"] = L.xg_f.notna().astype(float)
    return L.sort_values(["team_id", "kickoff_utc"]).reset_index(drop=True)

METRICS = ["gf", "ga", "tot", "over25", "btts", "cs", "fts", "gf2", "ga2", "gf3", "ga3", "tot4", "htg", "opp_gf_pre", "shots_f", "shots_on_target_f", "shots_a", "shots_on_target_a", "xg_f", "xg_a"]

def rolling_block(L, mask, n, tag):
    """Shifted rolling means over the rows where mask is true, per team. n=None -> expanding (season-to-date)."""
    # Rolling values are computed on the masked rows (e.g. league games only) INCLUDING the current game, carried
    # forward onto every row of the team (so a cup tie sees the team's latest league form), then shifted one row
    # within the team so each row only sees games before it. Fix 19 Oct 2026: cup rows previously got NaN.
    sub = L[mask].copy()
    g = sub.groupby("team_id")
    raw = pd.DataFrame(index=sub.index)
    for m in METRICS:
        raw[f"{tag}_{m}"] = g[m].transform(lambda x: x.expanding().mean() if n is None else x.rolling(n, min_periods=1).mean())
    raw[f"{tag}_n"] = g["gf"].transform(lambda x: x.expanding().count() if n is None else x.rolling(n, min_periods=1).count())
    raw[f"{tag}_n_stats"] = g["shots_f"].transform(lambda x: x.expanding().count() if n is None else x.rolling(n, min_periods=1).count())
    full = raw.reindex(L.index)
    gl = full.groupby(L["team_id"])
    out = gl.ffill().groupby(L["team_id"]).shift(1)
    return out

def team_features(L):
    F = pd.DataFrame(index=L.index)
    # season-to-date at venue, league matches only, reset each season
    key = L.team_id.astype(str) + "_" + L.season.astype(str) + "_" + L.venue
    Ls = L.copy(); Ls["team_id"] = key
    F = F.join(rolling_block(Ls, (Ls.is_cup == 0), None, "std_v"))
    # last 5 and last 10, any venue, any competition (rolls across seasons: August form uses May games)
    F = F.join(rolling_block(L, pd.Series(True, index=L.index), 5, "l5"))
    F = F.join(rolling_block(L, pd.Series(True, index=L.index), 10, "l10"))
    # last 5 at this venue, any competition
    Lv = L.copy(); Lv["team_id"] = L.team_id.astype(str) + "_" + L.venue
    F = F.join(rolling_block(Lv, pd.Series(True, index=Lv.index), 5, "l5_v"))
    # THIS SEASON, LEAGUE ONLY: last 5 any venue (l5L) and last 3 at this venue (v3L). The analysis prompt's windows.
    Lk = L.copy(); Lk["team_id"] = L.team_id.astype(str) + "_" + L.season.astype(str)
    F = F.join(rolling_block(Lk, (Lk.is_cup == 0), 5, "l5L"))
    mx = Lk[Lk.is_cup == 0].groupby("team_id")["tot"].transform(lambda x: x.rolling(5, min_periods=1).max()).reindex(L.index)
    F["l5L_maxtot"] = mx.groupby(Lk["team_id"]).ffill().groupby(Lk["team_id"]).shift(1)
    Lkv = L.copy(); Lkv["team_id"] = L.team_id.astype(str) + "_" + L.season.astype(str) + "_" + L.venue
    F = F.join(rolling_block(Lkv, (Lkv.is_cup == 0), 3, "v3L"))
    # previous 5 before the last 5 (for trend)
    g = L.groupby("team_id")
    for m in ("gf", "ga", "shots_on_target_f", "shots_on_target_a", "xg_f", "xg_a"):
        F[f"p5_{m}"] = g[m].transform(lambda x: x.shift(6).rolling(5, min_periods=3).mean())
        F[f"trend_{m}"] = F[f"l5_{m}"] - F[f"p5_{m}"]
    return pd.concat([L[["fixture_id", "team_id", "venue"]], F], axis=1)

def league_baselines(fx):
    """Per league-season, expanding averages using only matches that kicked off strictly before this one."""
    up = fx[fx.ft_home.isna()]
    fx = fx[fx.ft_home.notna()]
    d = fx.sort_values("kickoff_utc")[["fixture_id", "league_id", "season", "kickoff_utc", "ft_home", "ft_away"]].copy()
    d["tot"] = d.ft_home + d.ft_away; d["o25"] = (d.tot >= 3).astype(float); d["btts"] = ((d.ft_home > 0) & (d.ft_away > 0)).astype(float)
    d["one"] = 1.0
    out = {}
    for m in ("tot", "ft_home", "ft_away", "o25", "btts", "one"):
        cs = d.groupby(["league_id", "season"])[m].cumsum()
        # subtract this kickoff's own group so ties (same-time kickoffs) are excluded
        same = d.groupby(["league_id", "season", "kickoff_utc"])[m].transform("sum")
        cum_before = cs - same
        out[m] = cum_before
    n = out["one"]
    B = pd.DataFrame({"fixture_id": d.fixture_id, "lg_n": n,
                      "lg_tot": out["tot"] / n.replace(0, np.nan), "lg_home_gf": out["ft_home"] / n.replace(0, np.nan),
                      "lg_away_gf": out["ft_away"] / n.replace(0, np.nan), "lg_o25": out["o25"] / n.replace(0, np.nan),
                      "lg_btts": out["btts"] / n.replace(0, np.nan)})
    # previous season's final averages as a prior for the first weeks
    prev = d.groupby(["league_id", "season"]).agg(pl_tot=("tot", "mean"), pl_home_gf=("ft_home", "mean"), pl_away_gf=("ft_away", "mean"), pl_o25=("o25", "mean")).reset_index()
    prev["season"] = prev.season + 1
    B = B.merge(d[["fixture_id", "league_id", "season"]], on="fixture_id")
    if len(up):
        tot = d.groupby(["league_id", "season"]).agg(lg_n=("one", "sum"), lg_tot=("tot", "mean"), lg_home_gf=("ft_home", "mean"),
                                                     lg_away_gf=("ft_away", "mean"), lg_o25=("o25", "mean"), lg_btts=("btts", "mean")).reset_index()
        U = up[["fixture_id", "league_id", "season"]].merge(tot, on=["league_id", "season"], how="left")
        B = pd.concat([B, U], ignore_index=True)
    B = B.merge(prev, on=["league_id", "season"], how="left").drop(columns=["league_id", "season"])
    return B

def build(db, upcoming_to=None):
    fx, st = load(db, upcoming_to)
    L = long_table(fx, st)
    T = team_features(L)
    H = T[T.venue == "H"].drop(columns=["venue"]).add_prefix("h_").rename(columns={"h_fixture_id": "fixture_id"})
    A = T[T.venue == "A"].drop(columns=["venue"]).add_prefix("a_").rename(columns={"a_fixture_id": "fixture_id"})
    X = fx[["fixture_id", "league_id", "comp", "season", "is_cup", "kickoff_utc", "home_id", "away_id", "ft_home", "ft_away", "ht_home", "ht_away"]].merge(H, on="fixture_id").merge(A, on="fixture_id")
    X = X.merge(league_baselines(fx), on="fixture_id", how="left")
    X["target_over25"] = ((X.ft_home + X.ft_away) >= 3).astype(float).where(X.ft_home.notna())
    X["target_btts"] = ((X.ft_home > 0) & (X.ft_away > 0)).astype(float).where(X.ft_home.notna())
    # matchup features (goals; stats versions where present)
    X["m_gf_sum_l5"] = X.h_l5_gf + X.a_l5_gf; X["m_ga_sum_l5"] = X.h_l5_ga + X.a_l5_ga
    X["m_o25_l10"] = (X.h_l10_over25 + X.a_l10_over25) / 2; X["m_btts_l10"] = (X.h_l10_btts + X.a_l10_btts) / 2
    X["m_sot_sum_l5"] = X.h_l5_shots_on_target_f + X.a_l5_shots_on_target_f
    X["m_sota_sum_l5"] = X.h_l5_shots_on_target_a + X.a_l5_shots_on_target_a
    X["m_xg_sum_l5"] = X.h_l5_xg_f + X.a_l5_xg_f; X["m_xga_sum_l5"] = X.h_l5_xg_a + X.a_l5_xg_a
    X["m_hatt_x_adef_xg"] = X.h_l5_xg_f * X.a_l5_xg_a; X["m_aatt_x_hdef_xg"] = X.a_l5_xg_f * X.h_l5_xg_a
    # availability flags and tier
    X["has_shots"] = (X.h_l5_n_stats.fillna(0) >= 3) & (X.a_l5_n_stats.fillna(0) >= 3)
    X["has_xg"] = X.h_l5_xg_f.notna() & X.a_l5_xg_f.notna() & X.has_shots
    X["tier"] = np.where(X.has_xg, "A", np.where(X.has_shots, "B", "D"))
    X["early"] = (X.h_std_v_n.fillna(0) < 3) | (X.a_std_v_n.fillna(0) < 3)
    return X.sort_values("kickoff_utc").reset_index(drop=True)

def leakage_test(db, X, n=300, seed=0):
    """Recompute a few features from the raw fixtures table using only kickoff < this kickoff."""
    c = sqlite3.connect(db)
    raw = pd.read_sql("SELECT fixture_id, kickoff_utc, home_id, away_id, ft_home, ft_away, status FROM fixtures WHERE ft_home IS NOT NULL", c, parse_dates=["kickoff_utc"]); c.close()
    raw = raw[raw.status.isin(FINISHED)]; raw["kickoff_utc"] = pd.to_datetime(raw.kickoff_utc, utc=True)
    rng = np.random.default_rng(seed); bad = 0; checked = 0
    for _, r in X.sample(min(n, len(X)), random_state=seed).iterrows():
        for side, tid, col in (("h", r.home_id, "h_l5_gf"), ("a", r.away_id, "a_l5_gf")):
            prev = raw[((raw.home_id == tid) | (raw.away_id == tid)) & (raw.kickoff_utc < r.kickoff_utc)].sort_values("kickoff_utc").tail(5)
            if len(prev) == 0:
                ok = np.isnan(r[col])
            else:
                gf = np.where(prev.home_id == tid, prev.ft_home, prev.ft_away).mean()
                ok = abs(gf - r[col]) < 1e-9
            checked += 1; bad += (not ok)
    print(f"leakage test: {checked} values checked, {bad} mismatches")
    return bad == 0

if __name__ == "__main__":
    db = sys.argv[1]
    X = build(db)
    out = os.path.join(os.path.dirname(os.path.abspath(db)), "features.pkl")
    X.to_pickle(out); X.to_csv(out.replace(".pkl", ".csv"), index=False)
    print(f"{len(X)} fixtures, {X.shape[1]} columns -> {out}")
    print(X.groupby(["season", "tier"]).size().unstack(fill_value=0))
    if "--test" in sys.argv:
        leakage_test(db, X)
