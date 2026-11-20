"""lab.py - shared loading, splits and scoring helpers. Splits are fixed here and nowhere else.

DEV  = 2023-24 + 2024-25   (formula search, model fitting)
VAL  = 2025-26             (model selection; V4.1 cut points were also set here, its fit never saw it)
TEST = 2026-27 to date     (opened once, after selections are frozen in results/preregistered.json)
"""
import os, numpy as np, pandas as pd
from math import sqrt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEV, VAL, TEST = [2023, 2024], [2025], [2026]
LEAGUE_NAMES = {39: "Premier League", 40: "Championship", 41: "League One", 42: "League Two", 43: "National League",
                50: "National League North", 51: "National League South", 78: "Bundesliga", 88: "Eredivisie",
                61: "Ligue 1", 203: "Super Lig", 179: "Scottish Premiership", 140: "La Liga", 94: "Primeira Liga"}
SEASON_NAMES = {2023: "2023-24", 2024: "2024-25", 2025: "2025-26", 2026: "2026-27"}


def load(all_leagues=False):
    X = pd.read_parquet(f"{ROOT}/data/features.parquet")
    V = pd.read_parquet(f"{ROOT}/data/v4_scores.parquet")[["fixture_id", "v4_score"]]
    X = X.merge(V, on="fixture_id", how="left")
    X["eligible"] = (X.h_S5_n >= 3) & (X.a_S5_n >= 3) & X.eval_ok & X.season.isin(DEV + VAL + TEST)
    if not all_leagues:
        X = X[X.rob14]
    return X.reset_index(drop=True)


def universe(X, seasons):
    """the one fixture universe every model is judged on: Rob's 14 leagues, FT results, both sides 3+ league games."""
    return X[X.rob14 & X.eligible & X.season.isin(seasons)]


def wilson(k, n, z=1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def one_in(k, n):
    return round(n / k, 2) if k else float("inf")


def summarise(sel, y):
    """counts for a boolean selection over outcomes y."""
    n = int(sel.sum()); k = int(y[sel].sum())
    lo, hi = wilson(k, n)
    return {"selected": n, "won": k, "lost": n - k, "one_in": one_in(k, n), "lo95": lo, "hi95": hi}


def topk_per_window(df, score_col, k, qualify=None):
    """mask of the top-k fixtures by score inside each betting window; ties broken by fixture_id (stable, pre-match).
    qualify: optional boolean Series; non-qualifying fixtures are never used to fill a window."""
    d = df[[score_col, "window", "fixture_id"]].copy()
    if qualify is not None:
        d = d[qualify.reindex(d.index).fillna(False).values]
    d = d.sort_values([score_col, "fixture_id"], ascending=[False, True])
    r = d.groupby("window").cumcount()
    m = pd.Series(False, index=df.index)
    m.loc[r[r < k].index] = True
    return m


def matched_volume(df, sel, score_col):
    """for a rule's selection, take the same NUMBER of fixtures per window ranked by score_col (paired, equal volume)."""
    cnt = sel.groupby(df.window).sum()
    d = df[[score_col, "window", "fixture_id"]].sort_values([score_col, "fixture_id"], ascending=[False, True])
    r = d.groupby("window").cumcount()
    lim = d.window.map(cnt).fillna(0)
    m = pd.Series(False, index=df.index); m.loc[r[r < lim].index] = True
    return m


def brier(p, y): return float(np.mean((p - y) ** 2))


def logloss(p, y):
    p = np.clip(p, 1e-6, 1 - 1e-6); return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
