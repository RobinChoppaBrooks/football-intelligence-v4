"""
open_game.py  -  EXPERIMENTAL open-game filter (research only, 2 Nov 2026). Never used for selection.

Idea: two defensively vulnerable teams that both contribute goals and whose games stay open in the second half.
Definitions are the ones fixed on 2 Nov 2026 before any result was looked at (docs/research/2026-11-02_over25_research.md).
Do not change them without a new, documented test (docs/research_policy.md).

Inputs: football.db fixtures and fixture_events (download_events.py). Only league games of the 14 monitored leagues,
season 2026-27, whose goal events add up to the stored full-time score. Only games that kicked off before the cut-off
are used, so the assessment is always pre-match.

    python3 open_game.py history [--out reports/research/open_game_history_<date>.csv]
        re-runs the chronological test: every fixture with goal events where both sides have 5 earlier games with events

Used by research_groups.py to label the fixtures of each prediction run.
"""
import os, sys, sqlite3, datetime as dt
from collections import defaultdict
import pandas as pd

LEAGUE_IDS = {39: "Premier League", 40: "Championship", 41: "League One", 42: "League Two", 43: "National League", 50: "National League North",
              51: "National League South", 78: "Bundesliga", 88: "Eredivisie", 61: "Ligue 1", 203: "Super Lig", 179: "Scottish Premiership",
              140: "La Liga", 94: "Primeira Liga"}
FINISHED = ("FT", "AET", "PEN"); SEASON = 2026

# ---------------------------------------------------------------- scoreline rebuild from goal events
def rebuild(f, events):
    """Goals as (minute, extra, team_id) in order, or None when the events do not add up to the full-time score.
    Own goals are tried both ways (credited to the event's team, then to the other side), as in the 2 Nov study."""
    goals = [e for e in events if e["type"] == "Goal" and (e["detail"] or "") != "Missed Penalty"]
    goals.sort(key=lambda e: (e["minute"] if e["minute"] is not None else 999, e["extra"] or 0, e["seq"]))
    h, a = f["home_id"], f["away_id"]
    for swap_own_goals in (False, True):
        hg = ag = 0; out = []; bad = False
        for e in goals:
            t = e["team_id"]
            if swap_own_goals and (e["detail"] or "") == "Own Goal": t = a if t == h else h
            if t == h: hg += 1
            elif t == a: ag += 1
            else: bad = True; break
            out.append((e["minute"] or 0, e["extra"] or 0, t))
        if not bad and hg == f["ft_home"] and ag == f["ft_away"]: return out
    return None

# ---------------------------------------------------------------- per-game metrics (unchanged from 2 Nov)
def game_metrics(goals, gf, ga):
    """goals: list of (minute, extra, scored_by_this_team). Metrics from the team's point of view."""
    m = dict(gf=gf, ga=ga, scored=gf > 0, scored2=gf >= 2, conceded=ga > 0, conceded2=ga >= 2, cs=ga == 0,
             sh_gf=0, sh_ga=0, g60_gf=0, g60_ga=0, g75_gf=0, g75_ga=0, opps=[], progression=[])
    tf = ta = 0; seq = []
    for mi, ex, mine in goals:
        if mine: tf += 1
        else: ta += 1
        seq.append((mi, tf, ta))
        m["progression"].append(f"{tf}-{ta} ({mi}{'+' + str(ex) if ex else ''}{'' if mine else ' opp'})")
        side = "gf" if mine else "ga"
        if mi >= 46: m[f"sh_{side}"] += 1
        if mi >= 61: m[f"g60_{side}"] += 1
        if mi >= 76: m[f"g75_{side}"] += 1
    # an 'opportunity': 1-0, 0-1, 2-0 or 0-2 reached before the 75th minute; open = any later goal by either side
    for i, (mi, tf, ta) in enumerate(seq):
        if (tf, ta) in ((1, 0), (0, 1), (2, 0), (0, 2)) and mi < 75: m["opps"].append(i < len(seq) - 1)
    m["goal_after_60"] = (m["g60_gf"] + m["g60_ga"]) > 0
    return m

def summarise(games):
    s = dict(n=len(games))
    for k in ("scored", "scored2", "conceded", "conceded2", "cs", "goal_after_60"): s[k] = sum(1 for g in games if g["m"][k])
    for k in ("sh_gf", "sh_ga", "g60_gf", "g60_ga", "g75_gf", "g75_ga", "gf", "ga"): s[k] = sum(g["m"][k] for g in games)
    opps = [o for g in games for o in g["m"]["opps"]]; s["opps"] = len(opps); s["opps_open"] = sum(opps)
    return s

def team_points(s5):
    """The fixed 2 Nov rule on a team's last five games. Returns (points out of 7, flags met, shuts-games-down)."""
    p = 0; f = []
    if s5["conceded"] >= 4: p += 1; f.append(f"conceded in {s5['conceded']} of 5")
    if s5["conceded2"] >= 2: p += 1; f.append(f"conceded 2+ in {s5['conceded2']} of 5")
    if s5["cs"] <= 1: p += 1; f.append(f"{s5['cs']} clean sheets")
    if s5["scored"] >= 4: p += 1; f.append(f"scored in {s5['scored']} of 5")
    elif s5["scored"] >= 3: p += 0.5; f.append("scored in 3 of 5")
    sh = s5["sh_gf"] + s5["sh_ga"]
    if sh >= 6: p += 1; f.append(f"{sh} second-half goals in its games")
    elif sh >= 4: p += 0.5; f.append(f"{sh} second-half goals in its games")
    if s5["goal_after_60"] >= 3: p += 1; f.append(f"goal after 60' in {s5['goal_after_60']} of 5")
    if s5["opps"] >= 3 and s5["opps_open"] * 3 >= s5["opps"] * 2: p += 1; f.append(f"1-0/2-0 before 75' followed by another goal in {s5['opps_open']} of {s5['opps']}")
    elif s5["opps"] >= 2 and s5["opps_open"] * 2 >= s5["opps"]: p += 0.5; f.append(f"1-0/2-0 before 75' followed by another goal in {s5['opps_open']} of {s5['opps']}")
    shut = s5["cs"] >= 3 or s5["conceded"] <= 2
    return p, f, shut

def persistent(s10):
    """Weakness holds over the last ten: conceded 2+ in at least 4 in 10 and clean sheets in at most 3 in 10."""
    return s10["conceded2"] * 10 >= s10["n"] * 4 and s10["cs"] * 10 <= s10["n"] * 3

def category(pa, pb, shut_a, shut_b, pers_a, pers_b):
    if shut_a or shut_b: return "C"
    if pa >= 5.5 and pb >= 5.5 and (pers_a or pers_b): return "A"
    if (pa >= 4 and pb >= 4) or (max(pa, pb) >= 5.5 and min(pa, pb) >= 3.5): return "B"
    return "C"

# ---------------------------------------------------------------- data access
def load_games(db_path):
    """team_id -> chronological list of usable league games (with metrics). Also returns team names and per-fixture coverage."""
    db = sqlite3.connect(db_path); db.row_factory = sqlite3.Row
    ids = list(LEAGUE_IDS)
    fx = [dict(r) for r in db.execute(f"SELECT * FROM fixtures WHERE season=? AND league_id IN ({','.join('?' * len(ids))}) AND status IN ({','.join('?' * len(FINISHED))}) ORDER BY kickoff_utc",
                                      (SEASON, *ids, *FINISHED))]
    has_events = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fixture_events'")}
    ev = defaultdict(list)
    if has_events:
        for r in db.execute("SELECT * FROM fixture_events"): ev[r["fixture_id"]].append(dict(r))
    names = {r["team_id"]: r["name"] for r in db.execute("SELECT team_id, name FROM teams")}
    games = defaultdict(list); usable = set()
    for f in fx:
        if f.get("events_fetched") != 1 and not ev.get(f["fixture_id"]):
            if (f["ft_home"] or 0) + (f["ft_away"] or 0) > 0: continue          # no events: cannot rebuild the scoreline
        g = rebuild(f, ev.get(f["fixture_id"], []))
        if g is None: continue
        usable.add(f["fixture_id"])
        for team, opp, home in ((f["home_id"], f["away_id"], True), (f["away_id"], f["home_id"], False)):
            gf, ga = (f["ft_home"], f["ft_away"]) if home else (f["ft_away"], f["ft_home"])
            games[team].append(dict(fixture_id=f["fixture_id"], kickoff=f["kickoff_utc"], home=home, opp=names.get(opp, str(opp)), score=f"{f['ft_home']}-{f['ft_away']}",
                                    ht=f"{f['ht_home']}-{f['ht_away']}" if home else f"{f['ht_away']}-{f['ht_home']}",
                                    m=game_metrics([(mi, ex, t == team) for mi, ex, t in g], gf, ga)))
    return games, names, usable, fx

def assess(games, home_id, away_id, before_utc):
    """Open-game assessment of one fixture from games strictly before before_utc. None when a side has fewer than 5 usable games."""
    ph = [g for g in games.get(home_id, []) if g["kickoff"] < before_utc]; pa = [g for g in games.get(away_id, []) if g["kickoff"] < before_utc]
    if len(ph) < 5 or len(pa) < 5: return None
    h5, a5, h10, a10 = summarise(ph[-5:]), summarise(pa[-5:]), summarise(ph[-10:]), summarise(pa[-10:])
    p1, f1, s1 = team_points(h5); p2, f2, s2 = team_points(a5)
    q1, q2 = persistent(h10), persistent(a10)
    ex = lambda gs: [f"{g['kickoff'][:10]} {'H' if g['home'] else 'A'} v {g['opp']} {g['score']} (HT {g['ht']}): " + (" > ".join(g["m"]["progression"]) or "0-0") for g in gs[-5:]]
    return dict(category=category(p1, p2, s1, s2, q1, q2), points_home=p1, points_away=p2, flags_home=f1, flags_away=f2, shuts_home=s1, shuts_away=s2,
                persistent_home=q1, persistent_away=q2, home5=h5, away5=a5, home10=h10, away10=a10,
                home_venue5=summarise([g for g in ph if g["home"]][-5:]), away_venue5=summarise([g for g in pa if not g["home"]][-5:]),
                examples_home=ex(ph), examples_away=ex(pa))

def history(db_path, out):
    games, names, usable, fx = load_games(db_path)
    rows = []
    for f in fx:
        if f["fixture_id"] not in usable: continue
        a = assess(games, f["home_id"], f["away_id"], f["kickoff_utc"])
        if a is None: continue
        tot = f["ft_home"] + f["ft_away"]
        rows.append(dict(fixture_id=f["fixture_id"], league=LEAGUE_IDS[f["league_id"]], kickoff=f["kickoff_utc"], home=names.get(f["home_id"]), away=names.get(f["away_id"]),
                         score=f"{f['ft_home']}-{f['ft_away']}", over=tot >= 3, cat=a["category"], pts=a["points_home"] + a["points_away"]))
    H = pd.DataFrame(rows); os.makedirs(os.path.dirname(out) or ".", exist_ok=True); H.to_csv(out, index=False)
    print(f"{len(H)} fixtures -> {out}")
    if len(H): print(H.groupby("cat").over.agg(["sum", "size"]).to_string())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "history":
        out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"reports/research/open_game_history_{dt.date.today():%Y-%m-%d}.csv"
        history("football.db", out)
    else:
        print(__doc__)
