"""opengame.py  -  research: two defensively vulnerable, goal-contributing teams whose games stay open in the second half.
Inputs: the relentless team_matches CSV (goal minutes per team-game, 1,404 fixtures), football.db (fixtures, stats), a midweek
predictions CSV (official V4.1 classification). Research only; nothing touches V4.1."""
import sys, os, re, sqlite3, json, csv
import pandas as pd
from collections import defaultdict

TM, DB, PRED, OUT = sys.argv[1:5]
ORDER = ["Premier League", "Championship", "League One", "League Two", "National League", "National League North", "National League South",
         "Bundesliga", "Eredivisie", "Ligue 1", "Super Lig", "Scottish Premiership", "La Liga", "Primeira Liga"]

def parse_goals(s):
    out = []
    if not isinstance(s, str) or not s.strip(): return out
    for tok in s.split(";"):
        tok = tok.strip(); opp = "(opp)" in tok; tok = tok.replace("(opp)", "").strip()
        m = re.match(r"(\d+)(?:\+(\d+))?", tok)
        if not m: continue
        out.append((int(m.group(1)), int(m.group(2) or 0), not opp))
    return out

def game_metrics(goals, gf, ga):
    """goals: list of (minute, extra, scored_by_team). Per-game metrics from the team's perspective."""
    m = dict(gf=gf, ga=ga, scored=gf > 0, scored2=gf >= 2, conceded=ga > 0, conceded2=ga >= 2, cs=ga == 0,
             sh_gf=0, sh_ga=0, g60_gf=0, g60_ga=0, g75_gf=0, g75_ga=0, late_gf=0,
             scored_behind=0, scored_after_eq=0, scored_after_lead=0, conc_behind=0, conc_two_down=0, scored_two_down=0,
             sh_any=False, sh_two=False, opps=[], progression=[])
    tf = ta = 0; equalised = False; sh_count = 0; seq = []
    for mi, ex, mine in goals:
        prev = (tf, ta); second = mi >= 46
        if mine: tf += 1
        else: ta += 1
        seq.append((mi, ex, mine, tf, ta))
        m["progression"].append(f"{tf}-{ta} ({mi}{'+' + str(ex) if ex else ''}{'' if mine else ' opp'})")
        if second: sh_count += 1
        if mine:
            if second: m["sh_gf"] += 1
            if mi >= 61: m["g60_gf"] += 1
            if mi >= 76: m["g75_gf"] += 1; m["late_gf"] += 1
            if prev[0] < prev[1]: m["scored_behind"] += 1
            if prev[0] - prev[1] <= -2: m["scored_two_down"] += 1
            if prev[0] > prev[1]: m["scored_after_lead"] += 1
            if equalised: m["scored_after_eq"] += 1
            if tf == ta and prev[0] < prev[1]: equalised = True
        else:
            if second: m["sh_ga"] += 1
            if mi >= 61: m["g60_ga"] += 1
            if mi >= 76: m["g75_ga"] += 1
            if prev[0] < prev[1]: m["conc_behind"] += 1
            if prev[0] - prev[1] <= -2: m["conc_two_down"] += 1
    # opportunities: a 1-0 / 0-1 / 2-0 / 0-2 scoreline reached before the 75th minute; was there any later goal (either side)?
    for i, (mi, ex, mine, tf, ta) in enumerate(seq):
        if (tf, ta) in ((1, 0), (0, 1), (2, 0), (0, 2)) and mi < 75:
            m["opps"].append([f"{tf}-{ta}", mi, i < len(seq) - 1])
    m["sh_any"] = sh_count >= 1; m["sh_two"] = sh_count >= 2
    return m

def summarise(games):
    n = len(games); s = dict(n=n)
    for k in ("scored", "scored2", "conceded", "conceded2", "cs", "sh_any", "sh_two"): s[k] = sum(1 for g in games if g[k])
    for k in ("sh_gf", "sh_ga", "g60_gf", "g60_ga", "g75_gf", "g75_ga", "late_gf", "scored_behind", "scored_after_eq", "scored_after_lead", "conc_behind", "conc_two_down", "scored_two_down", "gf", "ga"): s[k] = sum(g[k] for g in games)
    opps = [o for g in games for o in g["opps"]]; s["opps"] = len(opps); s["opps_open"] = sum(1 for o in opps if o[2])
    # consecutive conceding: longest run of games conceding
    run = best = 0
    for g in games:
        run = run + 1 if g["conceded"] else 0; best = max(best, run)
    s["conc_streak"] = best; s["games3plus"] = sum(1 for g in games if g["gf"] + g["ga"] >= 3)
    return s

def team_points(s5):
    """Fixed a priori rule (2 Nov 2026). Returns (points out of 7, flags)."""
    p = 0; f = []
    if s5["conceded"] >= 4: p += 1; f.append("conceded in 4+ of 5")
    if s5["conceded2"] >= 2: p += 1; f.append("conceded 2+ in 2+ of 5")
    if s5["cs"] <= 1: p += 1; f.append("1 or 0 clean sheets")
    if s5["scored"] >= 4: p += 1; f.append("scored in 4+ of 5")
    elif s5["scored"] >= 3: p += 0.5; f.append("scored in 3 of 5")
    sh = s5["sh_gf"] + s5["sh_ga"]
    if sh >= 6: p += 1; f.append(f"{sh} second-half goals in its games")
    elif sh >= 4: p += 0.5; f.append(f"{sh} second-half goals in its games")
    if s5.get("games_g60", 0) >= 3: p += 1; f.append(f"goal after 60' in {s5['games_g60']} of 5")
    if s5["opps"] >= 3 and s5["opps_open"] * 3 >= s5["opps"] * 2: p += 1; f.append(f"1-0/2-0 before 75' followed by another goal in {s5['opps_open']} of {s5['opps']}")
    elif s5["opps"] >= 2 and s5["opps_open"] * 2 >= s5["opps"]: p += 0.5; f.append(f"1-0/2-0 before 75' followed by another goal in {s5['opps_open']} of {s5['opps']}")
    shut = s5["cs"] >= 3 or s5["conceded"] <= 2
    return p, f, shut

def category(pa, pb, shut_a, shut_b, pers_a, pers_b):
    if shut_a or shut_b: return "C"
    if pa >= 5.5 and pb >= 5.5 and (pers_a or pers_b): return "A"
    if (pa >= 4 and pb >= 4) or (max(pa, pb) >= 5.5 and min(pa, pb) >= 3.5): return "B"
    return "C"

# ---------- load
tm = pd.read_csv(TM); tm["goals"] = tm.goal_minutes.map(parse_goals)
tm = tm.sort_values(["team", "kickoff"])
games = {}   # team -> list of (kickoff, fixture_id, home, opp, metrics)
for r in tm.itertuples():
    mt = game_metrics(r.goals, int(r.gf), int(r.ga)); mt["games_g60"] = 1 if (mt["g60_gf"] + mt["g60_ga"]) > 0 else 0
    games.setdefault(r.team, []).append(dict(kickoff=r.kickoff, fixture_id=r.fixture_id, home=bool(r.home), opp=r.opp_name, score=r.score, ht=r.ht, m=mt, league=r.league, name=r.team_name))
names = {t: g[0]["name"] for t, g in games.items()}

def summ(gs):
    s = summarise([g["m"] for g in gs]); s["games_g60"] = sum(g["m"]["games_g60"] for g in gs); return s

# ---------- historical, chronological: category from each team's previous 5 games (events only), outcome from the score
db = sqlite3.connect(DB)
fx = pd.read_sql("select fixture_id, league_id, kickoff_utc, home_id, away_id, ft_home, ft_away from fixtures", db).set_index("fixture_id")
pl = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(DB)), "data", "predictions", "predictions_log.csv"), dtype=str)
pl = pl[pl.published == "1"].drop_duplicates("fixture_id", keep="last").set_index("fixture_id")
hist = []
seen = set()
for t, gs in games.items():
    for i, g in enumerate(gs):
        if g["fixture_id"] in seen: continue
        f = fx.loc[g["fixture_id"]]; h, a = int(f.home_id), int(f.away_id)
        def prior(team, before):
            return [x for x in games.get(team, []) if x["kickoff"] < before]
        ph, pa = prior(h, g["kickoff"]), prior(a, g["kickoff"])
        if len(ph) < 5 or len(pa) < 5: continue
        seen.add(g["fixture_id"])
        sh, sa = summ(ph[-5:]), summ(pa[-5:]); lh, la = summ(ph[-10:]), summ(pa[-10:])
        p1, f1, s1 = team_points(sh); p2, f2, s2 = team_points(sa)
        pers1 = lh["conceded2"] * 10 >= lh["n"] * 4 and lh["cs"] * 10 <= lh["n"] * 3; pers2 = la["conceded2"] * 10 >= la["n"] * 4 and la["cs"] * 10 <= la["n"] * 3
        cat = category(p1, p2, s1, s2, pers1, pers2)
        tot = int(f.ft_home) + int(f.ft_away)
        cls = pl.classification.get(str(g["fixture_id"]), None); sc = pl.model_score.get(str(g["fixture_id"]), None)
        hist.append(dict(fixture_id=g["fixture_id"], league=g["league"], kickoff=g["kickoff"], home=names[h], away=names[a], score=f"{int(f.ft_home)}-{int(f.ft_away)}", over=tot >= 3, cat=cat, pts=p1 + p2, v41=cls, model_score=sc))
H = pd.DataFrame(hist)
H.to_csv(OUT + "_history.csv", index=False)

# ---------- upcoming midweek
pred = pd.read_csv(PRED)
teams_by_name = {v: k for k, v in names.items()}
stats = pd.read_sql("select fs.fixture_id, fs.team_id, fs.shots, fs.shots_on_target, f.kickoff_utc from fixture_stats fs join fixtures f using(fixture_id) where f.season=2026", db)
rows = []
for r in pred.itertuples():
    hn, an = r.fixture.split(" v ", 1)
    th, ta = teams_by_name.get(hn), teams_by_name.get(an)
    if th is None or ta is None: rows.append(dict(fixture=r.fixture, note="no event data for a side")); continue
    gh, ga = games[th], games[ta]
    sh5, sa5, sh10, sa10 = summ(gh[-5:]), summ(ga[-5:]), summ(gh[-10:]), summ(ga[-10:])
    vh, va = summ([g for g in gh if g["home"]][-5:]), summ([g for g in ga if not g["home"]][-5:])
    p1, f1, s1 = team_points(sh5); p2, f2, s2 = team_points(sa5)
    pers1 = sh10["conceded2"] * 10 >= sh10["n"] * 4 and sh10["cs"] * 10 <= sh10["n"] * 3; pers2 = sa10["conceded2"] * 10 >= sa10["n"] * 4 and sa10["cs"] * 10 <= sa10["n"] * 3
    cat = category(p1, p2, s1, s2, pers1, pers2)
    def shots(team):
        s = stats[stats.team_id == team].sort_values("kickoff_utc").tail(5)
        return (len(s), int(s.shots.fillna(0).sum()), int(s.shots_on_target.fillna(0).sum())) if len(s) else (0, 0, 0)
    def ex(gs):
        return [f"{g['kickoff'][5:]} {'H' if g['home'] else 'A'} {g['opp']} {g['score']} (HT {g['ht']}): " + (" > ".join(g["m"]["progression"]) or "0-0") for g in gs[-5:]]
    rows.append(dict(league=r.competition, fixture=r.fixture, date=r.date, v41=r.model_confidence, model_score=r.model_score, cat=cat, pts_home=p1, pts_away=p2,
                     home=hn, away=an, h5=sh5, a5=sa5, h10=sh10, a10=sa10, hv=vh, av=va, hf=f1, af=f2, shut_h=s1, shut_a=s2, pers_h=pers1, pers_a=pers2,
                     shots_h=shots(th), shots_a=shots(ta), ex_h=ex(gh), ex_a=ex(ga)))
json.dump(rows, open(OUT + "_midweek.json", "w"), indent=1, default=str)
# summary prints
print("history fixtures:", len(H))
print(H.groupby("cat").over.agg(["sum", "size"]).to_string())
print(H[H.v41.notna()].groupby(["cat", "v41"]).over.agg(["sum", "size"]).to_string())
print("upcoming:", len(rows), "categories:", pd.Series([x.get("cat") for x in rows]).value_counts().to_dict())
