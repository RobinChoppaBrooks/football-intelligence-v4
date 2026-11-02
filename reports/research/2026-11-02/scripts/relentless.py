"""
relentless.py  -  research study: do teams keep scoring after going 2-0 up? (Rob, 2 Nov 2026). Research only: reads
fixtures and fixture_events from football.db, writes a markdown report and two CSVs under reports/research/. Nothing
here touches the model, classifications, BTTS rules or thresholds.

    python3 relentless.py [--db football.db] [--last 10] [--recent 5] [--out reports/research]

Needs goal events in fixture_events (download_events.py). A fixture is used only when the scoreline rebuilt from its
goal events matches the stored full-time score; everything else is listed as incomplete and left out.
Observed goals are not attacking intensity: a third goal says the team scored again, not how hard it pressed.
"""
import os, sys, sqlite3, argparse, csv, json
from collections import defaultdict
from datetime import datetime, timezone, timedelta

PRIORITY_14 = ["Premier League", "Championship", "League One", "League Two", "National League", "National League North",
               "National League South", "Bundesliga", "Eredivisie", "Ligue 1", "Super Lig", "Scottish Premiership", "La Liga", "Primeira Liga"]
LEAGUE_IDS = {39: "Premier League", 40: "Championship", 41: "League One", 42: "League Two", 43: "National League", 50: "National League North",
              51: "National League South", 78: "Bundesliga", 88: "Eredivisie", 61: "Ligue 1", 203: "Super Lig", 179: "Scottish Premiership",
              140: "La Liga", 94: "Primeira Liga"}
FINISHED = ("FT", "AET", "PEN"); SEASON = 2026

def mlabel(minute, extra): return f"{minute}+{extra}" if extra else f"{minute}"

def rebuild(fx, events):
    """Return (ok, convention, states) where states is the list of (minute, extra, scoring_team_id, home_goals, away_goals) after each goal."""
    goals = [e for e in events if e["type"] == "Goal" and (e["detail"] or "") != "Missed Penalty"]
    goals.sort(key=lambda e: (e["minute"] if e["minute"] is not None else 999, e["extra"] or 0, e["seq"]))
    h, a = fx["home_id"], fx["away_id"]
    for conv in ("A", "B"):     # A: event team is the team credited; B: own goals credited to the other side
        hg = ag = 0; states = []; bad = False
        for e in goals:
            t = e["team_id"]
            if conv == "B" and (e["detail"] or "") == "Own Goal": t = a if t == h else h
            if t == h: hg += 1
            elif t == a: ag += 1
            else: bad = True; break
            states.append((e["minute"], e["extra"] or 0, t, hg, ag))
        if not bad and hg == fx["ft_home"] and ag == fx["ft_away"]:
            return True, conv, states
    return False, None, []

def team_view(fx, states, team):
    """Metrics for one team in one fixture."""
    home = fx["home_id"] == team; opp = fx["away_id"] if home else fx["home_id"]
    seq = []   # (minute, extra, scorer_is_team, gf, ga)
    for m, x, t, hg, ag in states:
        gf, ga = (hg, ag) if home else (ag, hg)
        seq.append((m, x, t == team, gf, ga))
    ft_gf, ft_ga = (fx["ft_home"], fx["ft_away"]) if home else (fx["ft_away"], fx["ft_home"])
    ht_gf, ht_ga = (fx["ht_home"], fx["ht_away"]) if home else (fx["ht_away"], fx["ht_home"])
    r = dict(fixture_id=fx["fixture_id"], league=LEAGUE_IDS[fx["league_id"]], kickoff=fx["kickoff_utc"][:10], team=team, opp=opp, home=home,
             gf=ft_gf, ga=ft_ga, ht=f"{ht_gf}-{ht_ga}", score=f"{fx['ft_home']}-{fx['ft_away']}", goal_minutes=[mlabel(m, x) + ("" if s else " (opp)") for m, x, s, _, _ in seq],
             lead2_type=None, lead2_minute=None, lead2_score=None, after_lead_goals=0, after_lead_minutes=[], after_lead_conceded=0,
             third_goal_minute=None, fourth_plus=0, late70=0, late80=0, late70_minutes=[], finished_2_0=False, no_more_after_2_0=None,
             one_nil_to_three=False, one_nil_ht_to_three=False, behind2_type=None, behind2_minute=None, conceded_after_behind=0, conceded_after_behind_minutes=[])
    lead_found = behind_found = False; reached_1_0 = False
    for i, (m, x, s, gf, ga) in enumerate(seq):
        prev_gf, prev_ga = (seq[i-1][3], seq[i-1][4]) if i else (0, 0)
        if gf == 1 and ga == 0: reached_1_0 = True
        # late goals while already two or more ahead before this goal
        if s and prev_gf - prev_ga >= 2:
            if m >= 70: r["late70"] += 1; r["late70_minutes"].append(mlabel(m, x))
            if m >= 80: r["late80"] += 1
        if lead_found and s:
            r["after_lead_goals"] += 1; r["after_lead_minutes"].append(mlabel(m, x))
            if r["lead2_type"] == "2-0" and gf == 3 and r["third_goal_minute"] is None: r["third_goal_minute"] = mlabel(m, x)
            if r["lead2_type"] == "2-0" and gf >= 4: r["fourth_plus"] += 1
        if lead_found and not s: r["after_lead_conceded"] += 1
        if behind_found and not s:
            r["conceded_after_behind"] += 1; r["conceded_after_behind_minutes"].append(mlabel(m, x))
        if not lead_found and gf - ga == 2:
            lead_found = True; r["lead2_type"] = "2-0" if (gf == 2 and ga == 0) else "other"; r["lead2_minute"] = mlabel(m, x); r["lead2_score"] = f"{gf}-{ga}"
        if not behind_found and ga - gf == 2:
            behind_found = True; r["behind2_type"] = "0-2" if (ga == 2 and gf == 0) else "other"; r["behind2_minute"] = mlabel(m, x)
    if r["lead2_type"] == "2-0":
        r["finished_2_0"] = (ft_gf == 2 and ft_ga == 0); r["no_more_after_2_0"] = (r["after_lead_goals"] == 0)
    r["one_nil_to_three"] = reached_1_0 and ft_gf >= 3 and ft_ga == 0
    r["one_nil_ht_to_three"] = (ht_gf == 1 and ht_ga == 0) and ft_gf >= 3 and ft_ga == 0
    return r

def pct(k, n): return f"{k} of {n} ({round(100*k/n)}%)" if n else "0 of 0"

def summarise(rows):
    """rows: team-match rows for one team (chronological). Returns the aggregate dict."""
    n = len(rows)
    opp20 = [r for r in rows if r["lead2_type"] == "2-0"]; oppo = [r for r in rows if r["lead2_type"] == "other"]
    again20 = [r for r in opp20 if r["after_lead_goals"] > 0]; againo = [r for r in oppo if r["after_lead_goals"] > 0]
    beh = [r for r in rows if r["behind2_type"]]; behc = [r for r in beh if r["conceded_after_behind"] > 0]
    return dict(n=n, opp_2_0=len(opp20), again_2_0=len(again20), third=sum(1 for r in opp20 if r["third_goal_minute"]),
                fourth_plus_goals=sum(r["fourth_plus"] for r in opp20), finished_2_0=sum(r["finished_2_0"] for r in opp20),
                lead_minutes=[r["lead2_minute"] for r in opp20], extra_goal_minutes=[m for r in opp20 for m in r["after_lead_minutes"]],
                opp_other=len(oppo), again_other=len(againo), late70=sum(r["late70"] for r in rows), late80=sum(r["late80"] for r in rows),
                late70_minutes=[m for r in rows for m in r["late70_minutes"]],
                one_nil_to_three=sum(r["one_nil_to_three"] for r in rows), one_nil_ht_to_three=sum(r["one_nil_ht_to_three"] for r in rows),
                behind2=len(beh), behind2_conceded_again=len(behc), conceded_after_behind_goals=sum(r["conceded_after_behind"] for r in beh),
                goals_for=sum(r["gf"] for r in rows), matches_3plus=sum(1 for r in rows if r["gf"] + r["ga"] >= 3))

def tier(s):
    opp = s["opp_2_0"] + s["opp_other"]; again = s["again_2_0"] + s["again_other"]
    if opp >= 3 and again >= 3: return "Strong"
    if opp >= 3 and again == 2: return "Moderate"
    if opp >= 3: return "Weak (3+ leads, scored again in 1 or 0)"
    if opp == 2 and again == 2: return "Two matches only"
    if opp >= 1: return "Thin (1 or 2 leads)"
    return "No two-goal lead"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--db", default="football.db"); ap.add_argument("--last", type=int, default=10)
    ap.add_argument("--recent", type=int, default=5); ap.add_argument("--out", default="reports/research"); ap.add_argument("--days-ahead", type=int, default=7)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    db = sqlite3.connect(a.db); db.row_factory = sqlite3.Row
    teams = {r["team_id"]: r["name"] for r in db.execute("SELECT team_id, name FROM teams")}
    ids = list(LEAGUE_IDS)
    fx = [dict(r) for r in db.execute(f"SELECT * FROM fixtures WHERE season=? AND league_id IN ({','.join('?'*len(ids))}) AND status IN ({','.join('?'*len(FINISHED))}) ORDER BY kickoff_utc", (SEASON, *ids, *FINISHED))]
    ev = defaultdict(list)
    for r in db.execute("SELECT * FROM fixture_events"): ev[r["fixture_id"]].append(dict(r))
    # each team's last N league games
    by_team = defaultdict(list)
    for f in fx: by_team[f["home_id"]].append(f); by_team[f["away_id"]].append(f)
    wanted = {}
    for t, fs in by_team.items():
        for f in fs[-a.last:]: wanted[f["fixture_id"]] = f
    # rebuild scorelines, coverage per league
    cov = defaultdict(lambda: dict(wanted=0, no_events=0, mismatch=0, ok=0, own_goal_swap=0)); states = {}; incomplete = []
    for fid, f in wanted.items():
        lg = LEAGUE_IDS[f["league_id"]]; cov[lg]["wanted"] += 1
        if f["events_fetched"] != 1 or (not ev.get(fid) and (f["ft_home"] or 0) + (f["ft_away"] or 0) > 0):
            cov[lg]["no_events"] += 1; incomplete.append((lg, f, "no events fetched")); continue
        ok, conv, st = rebuild(f, ev.get(fid, []))
        if not ok: cov[lg]["mismatch"] += 1; incomplete.append((lg, f, "events do not add up to the full-time score")); continue
        cov[lg]["ok"] += 1; cov[lg]["own_goal_swap"] += (conv == "B"); states[fid] = st
    # team-match rows
    tm = defaultdict(list)
    for t, fs in by_team.items():
        for f in fs[-a.last:]:
            if f["fixture_id"] in states: tm[t].append(team_view(f, states[f["fixture_id"]], t))
    # aggregates
    agg = {}
    for t, rows in tm.items():
        if not rows: continue
        lg = rows[-1]["league"]
        agg[t] = dict(team=teams.get(t, str(t)), league=lg, all=summarise(rows), recent=summarise(rows[-a.recent:]),
                      home=summarise([r for r in rows if r["home"]]), away=summarise([r for r in rows if not r["home"]]), rows=rows)
        agg[t]["tier"] = tier(agg[t]["all"])
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # ---- CSV: team-match rows
    with open(f"{a.out}/relentless_{today}_team_matches.csv", "w", newline="", encoding="utf-8") as fh:
        w = None
        for t, rows in tm.items():
            for r in rows:
                o = {k: ("; ".join(v) if isinstance(v, list) else v) for k, v in r.items()}; o["team_name"] = teams.get(t, t); o["opp_name"] = teams.get(r["opp"], r["opp"])
                if w is None: w = csv.DictWriter(fh, fieldnames=list(o)); w.writeheader()
                w.writerow(o)
    # ---- CSV: team summary
    with open(f"{a.out}/relentless_{today}_teams.csv", "w", newline="", encoding="utf-8") as fh:
        w = None
        for t, g in agg.items():
            o = dict(team=g["team"], league=g["league"], tier=g["tier"])
            for scope in ("all", "recent", "home", "away"):
                for k, v in g[scope].items(): o[f"{scope}_{k}"] = "; ".join(v) if isinstance(v, list) else v
            if w is None: w = csv.DictWriter(fh, fieldnames=list(o)); w.writeheader()
            w.writerow(o)
    # ---- markdown report
    L = [f"# Relentless attacking study, {today}", "", f"Research only. Each team's last {a.last} completed league games (season 2026-27, {len(LEAGUE_IDS)} leagues), most recent {a.recent} shown separately. "
         "Scorelines rebuilt from API-Football goal events; a fixture is used only when the rebuilt score equals the stored full-time score. "
         "A 'two-goal lead' is the first moment a side led by exactly two goals; exact 2-0 is reported separately from other two-goal scorelines (3-1, 4-2). "
         "'Scored again' means at least one further goal after that moment. Late goals are goals scored at 70' or later (80' or later) when the side was already two or more ahead before the goal. "
         "Observed goals are not attacking intensity: that needs shot or chance data, which this study does not use.", ""]
    L += ["## Coverage", "", "| league | fixtures wanted | usable | no events | events do not match score | own-goal side swapped |", "|---|---|---|---|---|---|"]
    for lg in PRIORITY_14:
        c = cov.get(lg, dict(wanted=0, ok=0, no_events=0, mismatch=0, own_goal_swap=0))
        L.append(f"| {lg} | {c['wanted']} | {c['ok']} | {c['no_events']} | {c['mismatch']} | {c['own_goal_swap']} |")
    if incomplete:
        L += ["", f"Excluded fixtures ({len(incomplete)}):", ""] + [f"- {lg}: {teams.get(f['home_id'])} v {teams.get(f['away_id'])} {f['kickoff_utc'][:10]} ({f['ft_home']}-{f['ft_away']}), {why}, fixture_id {f['fixture_id']}" for lg, f, why in incomplete[:80]]
    L += ["", "## League by league ranking", "", "Ranked within each league by two-goal leads followed by another goal, then by late goals while two or more ahead. "
          "Strong = three or more two-goal leads and scored again in three or more of them. Moderate = three or more leads, scored again in two. "
          "Weak = three or more leads but scored again in one or none. Two matches only / Thin = one or two qualifying matches: not evidence of a pattern either way.", ""]
    for lg in PRIORITY_14:
        g = [x for x in agg.values() if x["league"] == lg]
        if not g: L += [f"### {lg}", "", "No usable fixtures.", ""]; continue
        g.sort(key=lambda x: (-(x["all"]["again_2_0"] + x["all"]["again_other"]), -x["all"]["late70"], -(x["all"]["opp_2_0"] + x["all"]["opp_other"]), x["team"]))
        L += [f"### {lg}", "", "| team | tier | games | exact 2-0 leads | scored again (2-0) | 3rd goal | 4th+ goals | finished 2-0 | other 2-goal leads | scored again (other) | late 70'+ / 80'+ | 1-0 to 3-0+ (HT 1-0) | last 5: 2-0 leads, scored again | home / away leads, scored again |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for x in g:
            s, r5, h, aw = x["all"], x["recent"], x["home"], x["away"]
            L.append(f"| {x['team']} | {x['tier']} | {s['n']} | {s['opp_2_0']} | {pct(s['again_2_0'], s['opp_2_0'])} | {s['third']} | {s['fourth_plus_goals']} | {s['finished_2_0']} | {s['opp_other']} | {pct(s['again_other'], s['opp_other'])} | {s['late70']} / {s['late80']} | {s['one_nil_to_three']} ({s['one_nil_ht_to_three']}) | {r5['opp_2_0'] + r5['opp_other']}, {r5['again_2_0'] + r5['again_other']} | {h['opp_2_0'] + h['opp_other']} / {h['again_2_0'] + h['again_other']}, {aw['opp_2_0'] + aw['opp_other']} / {aw['again_2_0'] + aw['again_other']} |")
        L.append("")
        for x in g:
            if x["tier"] in ("Strong", "Moderate"):
                L += [f"**{x['team']}** ({x['tier']}): lead minutes {', '.join(x['all']['lead_minutes']) or 'none at 2-0'}; extra goals after 2-0 at {', '.join(x['all']['extra_goal_minutes']) or 'none'}; late goals while 2+ ahead at {', '.join(x['all']['late70_minutes']) or 'none'}.", ""]
                for r in x["rows"]:
                    if r["lead2_type"]:
                        L.append(f"- {r['kickoff']} {'H' if r['home'] else 'A'} v {teams.get(r['opp'])}: {r['score']} (HT {r['ht']}), two-goal lead {r['lead2_score']} at {r['lead2_minute']}, then scored {r['after_lead_goals']} more{(' at ' + ', '.join(r['after_lead_minutes'])) if r['after_lead_minutes'] else ''}, conceded {r['after_lead_conceded']} after; goals {', '.join(r['goal_minutes'])}")
                L.append("")
    # ---- secondary: conceding when two down
    L += ["## Teams that concede again after going two behind", "", "| league | team | games | fell two behind (exact 0-2) | conceded again | further goals conceded | last 5: behind, conceded again |", "|---|---|---|---|---|---|---|"]
    conc = sorted([x for x in agg.values() if x["all"]["behind2"] >= 2], key=lambda x: (-x["all"]["behind2_conceded_again"], -x["all"]["conceded_after_behind_goals"]))
    for x in conc:
        s, r5 = x["all"], x["recent"]; ex = sum(1 for r in x["rows"] if r["behind2_type"] == "0-2")
        L.append(f"| {x['league']} | {x['team']} | {s['n']} | {s['behind2']} ({ex}) | {pct(s['behind2_conceded_again'], s['behind2'])} | {s['conceded_after_behind_goals']} | {r5['behind2']}, {r5['behind2_conceded_again']} |")
    # ---- upcoming matchups
    lo = datetime.now(timezone.utc).isoformat(timespec="seconds"); hi = (datetime.now(timezone.utc) + timedelta(days=a.days_ahead)).isoformat(timespec="seconds")
    up = db.execute(f"SELECT * FROM fixtures WHERE season=? AND league_id IN ({','.join('?'*len(ids))}) AND status='NS' AND kickoff_utc>=? AND kickoff_utc<? ORDER BY kickoff_utc", (SEASON, *ids, lo, hi)).fetchall()
    strong = {t for t, x in agg.items() if x["tier"] in ("Strong", "Moderate")}
    leaky = {t for t, x in agg.items() if x["all"]["behind2"] >= 2 and x["all"]["behind2_conceded_again"] >= 2}
    L += ["", f"## Possible matchups in the next {a.days_ahead} days (Strong or Moderate scorer v side that conceded again when two down in 2+ games)", ""]
    found = False
    for f in up:
        for t, o in ((f["home_id"], f["away_id"]), (f["away_id"], f["home_id"])):
            if t in strong and o in leaky:
                found = True; L.append(f"- {LEAGUE_IDS[f['league_id']]}, {f['kickoff_utc'][:16]} UTC: {teams.get(f['home_id'])} v {teams.get(f['away_id'])}: {teams.get(t)} ({agg[t]['tier']}) against {teams.get(o)} (two behind in {agg[o]['all']['behind2']}, conceded again in {agg[o]['all']['behind2_conceded_again']})")
    if not found: L.append("None found.")
    L += ["", "## Worth monitoring", "", "Teams rated Strong above, with their last-five count holding up (at least two two-goal leads in the last five with a further goal in each). "
          "Nothing here is a selection rule: before it could be, the same measure would have to be computed on the 2025-26 and 2026-27 history already in football.db (events for all seasons), "
          "scored chronologically out of sample (does a team's relentless count over its previous 10 games predict 3+ goals in its next game, over and above the locked model's score?), "
          "with counts, ranges and by-league results, as section 11 of over25_model_v4_methodology.md requires.", ""]
    strong_list = [x for x in agg.values() if x["tier"] == "Strong" and (x["recent"]["again_2_0"] + x["recent"]["again_other"]) >= 2]
    for x in sorted(strong_list, key=lambda x: (PRIORITY_14.index(x["league"]), x["team"])):
        s, r5 = x["all"], x["recent"]
        L.append(f"- {x['league']}: {x['team']}, two-goal leads {s['opp_2_0'] + s['opp_other']} and scored again in {s['again_2_0'] + s['again_other']}; last five {r5['opp_2_0'] + r5['opp_other']} and {r5['again_2_0'] + r5['again_other']}; late goals while 2+ ahead {s['late70']}")
    if not strong_list: L.append("- none meets the bar yet")
    path = f"{a.out}/relentless_{today}.md"; open(path, "w", encoding="utf-8").write("\n".join(L))
    print(json.dumps(dict(report=path, teams=len(agg), usable_fixtures=len(states), incomplete=len(incomplete), strong=len([x for x in agg.values() if x['tier']=='Strong']), coverage={k: dict(v) for k, v in cov.items()}), indent=1))

if __name__ == "__main__":
    main()
