"""
analyse_fixtures.py  -  the 3+ goals fixture analysis (Rob's master prompt). Zero API calls: everything comes from football.db.

    python3 analyse_fixtures.py football.db fixtures.txt [--out over25_analysis_YYYYMMDD]

fixtures.txt: competition name on its own line (config.py names), then "Home v Away" lines. Only those fixtures are analysed.
Outputs: <out>.md (main table, green cards, shortlist), <out>.csv (every number), <out>.pdf via report_lights.py.
"""
import sys, os, re, pickle, sqlite3, argparse, numpy as np, pandas as pd
from features import build
from bands import predict as band_predict
from btts import predict as btts_predict, label as btts_label
from config import LEAGUES, CUPS, NONLEAGUE, ORDER

ALL = {**LEAGUES, **CUPS, **NONLEAGUE}
HERE = os.path.dirname(os.path.abspath(__file__))

def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))
ALIASES = {"afc emley": "emley", "warrington rylands": "rylands", "airdrieonians": "airdrie united", "queen of south": "queen of the south",
           "hamilton": "hamilton academical", "hyde utd": "hyde united", "hornchurch": "afc hornchurch", "halifax": "fc halifax town",
           "boston utd": "boston united", "carshalton": "carshalton athletic", "afc whyteleafe": "whyteleafe", "accrington stanley": "accrington st",
           "exeter": "exeter city", "swindon": "swindon town", "fleetwood": "fleetwood town", "raith": "raith rovers", "ayr": "ayr utd",
           "stirling": "stirling albion", "forfar": "forfar athletic", "elgin": "elgin city", "spartans fc": "spartans", "alloa": "alloa athletic"}

def match_team(name, teams):
    n = norm(ALIASES.get(name.lower().strip(), name))
    for tid, tn in teams.items():
        if norm(tn) == n: return tid
    cands = [tid for tid, tn in teams.items() if n in norm(tn) or norm(tn) in n]
    return cands[0] if len(cands) == 1 else None

def parse_list(path):
    comp, out = None, []
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if not s or s.startswith("#"): continue
        if s.rstrip(":") in ALL: comp = s.rstrip(":"); continue
        m = re.split(r"\s+v(?:s\.?)?\s+", s, flags=re.I)
        if len(m) == 2 and comp: out.append((comp, m[0].strip(), m[1].strip()))
        else: print(f"  could not read line: {s!r}")
    return out

def last_n(fx, tid, season, before, n, venue=None, league_only=True):
    g = fx[(fx.season == season) & (fx.kickoff_utc < before) & fx.ft_home.notna()]
    if league_only: g = g[g.is_cup == 0]
    if venue == "H": g = g[g.home_id == tid]
    elif venue == "A": g = g[g.away_id == tid]
    else: g = g[(g.home_id == tid) | (g.away_id == tid)]
    g = g.sort_values("kickoff_utc").tail(n)
    rows = []
    for r in g.itertuples():
        home = r.home_id == tid
        rows.append(dict(opp=r.away_id if home else r.home_id, ven="H" if home else "A", gf=int(r.ft_home if home else r.ft_away),
                         ga=int(r.ft_away if home else r.ft_home), tot=int(r.ft_home + r.ft_away), kickoff=r.kickoff_utc))
    return rows

def pattern_text(hn, an, hr, ar, hv5, av5, catches):
    """Goal pattern (counts only): both contribute / one side dominates / low scoring; plus why, main risk and scoring route."""
    n = lambda rs, f: sum(1 for x in rs if f(x))
    hs2, as2 = n(hr, lambda x: x["gf"] >= 2), n(ar, lambda x: x["gf"] >= 2)
    hc2, ac2 = n(hr, lambda x: x["ga"] >= 2), n(ar, lambda x: x["ga"] >= 2)
    hs1, as1 = n(hr, lambda x: x["gf"] >= 1), n(ar, lambda x: x["gf"] >= 1)
    hbt, abt = n(hr, lambda x: x["gf"] > 0 and x["ga"] > 0), n(ar, lambda x: x["gf"] > 0 and x["ga"] > 0)
    ho, ao = n(hr, lambda x: x["tot"] >= 3), n(ar, lambda x: x["tot"] >= 3)
    hvo, avo = n(hv5, lambda x: x["tot"] >= 3), n(av5, lambda x: x["tot"] >= 3)
    hc1, ac1 = n(hr, lambda x: x["ga"] >= 1), n(ar, lambda x: x["ga"] >= 1)
    route_h = hs2 >= 3 or ac2 >= 3; route_a = as2 >= 3 or hc2 >= 3
    # "Both teams contribute" also requires each side to be scoring (4 of 5) and conceding (3 of 5): validated 59% BTTS
    # on 2,190 fixtures v 55% base (21 Oct 2026). The BTTS verdict is YES exactly when this pattern holds, so the two never disagree.
    both_scoring = hs1 >= 4 and as1 >= 4 and hc1 >= 3 and ac1 >= 3
    if route_h and route_a and both_scoring: pattern, route = "Both teams contribute", f"two routes: {hn} attack v {an} defence, and {an} attack v {hn} defence; both sides scoring in {hs1} and {as1} of 5"
    elif route_h and route_a:
        if hs1 < 4 or as1 < 4: gap = f"{hn if hs1 < 4 else an} have scored in only {min(hs1, as1)} of 5"
        else: gap = f"{hn if hc1 < 3 else an} have conceded in only {min(hc1, ac1)} of 5"
        pattern, route = "One side dominates", f"two routes on paper but {gap}, so the goals lean one way"
    elif route_h: pattern, route = "One side dominates", f"one route: {hn} scoring ({hs2} of {len(hr)} with 2+) against a {an} defence letting in 2+ in {ac2} of {len(ar)}"
    elif route_a: pattern, route = "One side dominates", f"one route: {an} scoring ({as2} of {len(ar)} with 2+) against a {hn} defence letting in 2+ in {hc2} of {len(hr)}"
    else: pattern, route = "Low scoring", "no clear route: neither attack scores 2+ regularly and neither defence leaks 2+ regularly"
    why = (f"{hn} {ho} of {len(hr)} games with 3+ and {an} {ao} of {len(ar)}; both scored in {hbt} of {len(hr)} ({hn}) and {abt} of {len(ar)} ({an}). "
           f"Venue: {hn} {hvo} of {len(hv5)} home games with 3+, {an} {avo} of {len(av5)} away.")
    risk = catches[0] if catches else ("Both teams scored in fewer than 3 of 5 for one side" if min(hbt, abt) < 3 else "No major warning in the last five")
    return pattern, why, risk, route

def seq(rows): return " | ".join(f"{r['gf']}-{r['ga']}" for r in rows) if rows else "no league games yet"
def cnt(rows, f): return sum(1 for r in rows if f(r))

def rate(x, y, strong_a, strong_b):
    """attack-vs-defence match-up. x = attacker rows, y = defender rows."""
    if len(x) < 3 or len(y) < 3: return "NEUTRAL", "sample under 3 games"
    a2 = cnt(x, lambda r: r["gf"] >= 2); d2 = cnt(y, lambda r: r["ga"] >= 2)
    a1 = cnt(x, lambda r: r["gf"] >= 1); d1 = cnt(y, lambda r: r["ga"] >= 1)
    agf = np.mean([r["gf"] for r in x]); dga = np.mean([r["ga"] for r in y])
    txt = f"scored in {a1}/{len(x)}, 2+ in {a2}/{len(x)} ({agf:.1f}/g) v conceded in {d1}/{len(y)}, 2+ in {d2}/{len(y)} ({dga:.1f}/g)"
    score = a2 + d2                      # 0 to 10: how often the attack scores twice plus how often the defence lets in two
    if score >= 6 and a1 >= 4 and d1 >= 4: return "STRONG", txt
    if score <= 3 or a1 <= 2 or d1 <= 2: return "WEAK", txt
    return "NEUTRAL", txt

def profile(m1, m2, hrows, arows):
    hga2 = cnt(hrows, lambda r: r["ga"] >= 2); aga2 = cnt(arows, lambda r: r["ga"] >= 2)
    hgf2 = cnt(hrows, lambda r: r["gf"] >= 2); agf2 = cnt(arows, lambda r: r["gf"] >= 2)
    if m1 == "STRONG" and m2 == "STRONG": return "Open"
    if "STRONG" in (m1, m2) and "WEAK" in (m1, m2): return "Dominant"
    if m1 == "STRONG" or m2 == "STRONG":          # one strong route, the other neutral: open if the quieter attack still scores twice sometimes
        quiet_gf2 = agf2 if m1 == "STRONG" else hgf2
        return "Open" if quiet_gf2 >= 2 else "Dominant"
    if hga2 >= 3 and aga2 >= 3 and hgf2 <= 2 and agf2 <= 2: return "Chaos"
    return "Mixed"

def against(hrows, arows, hv, av, names):
    out = []
    for lab, rows in (("Home", hrows), ("Away", arows)):
        if len(rows) < 5: out.append(f"{lab} side has only {len(rows)} league games this season"); continue
        cs = cnt(rows, lambda r: r["ga"] == 0); fts = cnt(rows, lambda r: r["gf"] == 0)
        if cs >= 2: out.append(f"{lab} side kept {cs}/5 clean sheets")
        if fts >= 2: out.append(f"{lab} side failed to score in {fts}/5")
        # 19 Oct 2026: the "average leans on one big game" catch was removed. Tested on 51,551 historical fixtures it
        # pointed the wrong way (flagged sides went over slightly MORE often), and the dots already show each game.
        und = cnt(rows, lambda r: r["tot"] <= 2)
        if und >= 3: out.append(f"{lab} side's last 5: {und}/5 finished under 2.5")
    for lab, rows, v in (("Home", hv, "home"), ("Away", av, "away")):
        if len(rows) < 3: out.append(f"{lab} side has only {len(rows)} {v} league games this season")
        elif cnt(rows, lambda r: r["tot"] >= 3) <= 1: out.append(f"{lab} side's last 3 {v} games: only {cnt(rows, lambda r: r['tot'] >= 3)}/3 went over")
    return out

def for_(hrows, arows, hv, av):
    out = []
    for lab, rows in (("Home", hrows), ("Away", arows)):
        if len(rows) < 3: continue
        o = cnt(rows, lambda r: r["tot"] >= 3); b = cnt(rows, lambda r: r["gf"] > 0 and r["ga"] > 0)
        gf2 = cnt(rows, lambda r: r["gf"] >= 2); ga2 = cnt(rows, lambda r: r["ga"] >= 2)
        bits = []
        if o >= 4: bits.append(f"{o}/{len(rows)} games over 2.5")
        if gf2 >= 3: bits.append(f"scored 2+ in {gf2}/{len(rows)}")
        if ga2 >= 3: bits.append(f"conceded 2+ in {ga2}/{len(rows)}")
        if b >= 4: bits.append(f"BTTS in {b}/{len(rows)}")
        if bits: out.append(f"{lab} side: " + ", ".join(bits))
    for lab, rows, v in (("Home", hv, "home"), ("Away", av, "away")):
        if len(rows) >= 3 and cnt(rows, lambda r: r["tot"] >= 3) == 3: out.append(f"{lab} side's last 3 {v} games all over 2.5 ({sum(r['gf'] for r in rows)}-{sum(r['ga'] for r in rows)})")
    return out

def opp_quality(rows, fx, season, before, lg_ga):
    """average goals-against per game (season, league) of the five opponents, versus the league average."""
    vals = []
    for r in rows:
        g = fx[(fx.season == season) & (fx.kickoff_utc < before) & (fx.is_cup == 0) & fx.ft_home.notna() & ((fx.home_id == r["opp"]) | (fx.away_id == r["opp"]))]
        if len(g) == 0: continue
        ga = np.where(g.home_id == r["opp"], g.ft_away, g.ft_home).mean(); vals.append(ga)
    if not vals: return None
    return float(np.mean(vals)), float(lg_ga)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("db"); ap.add_argument("list"); ap.add_argument("--out", default=None); ap.add_argument("--allow-played", action="store_true", help="reproduction tests: analyse fixtures already played, as of their kick-off")
    a = ap.parse_args()
    c = sqlite3.connect(a.db); teams = dict(c.execute("SELECT team_id, name FROM teams"))
    fx = pd.read_sql("SELECT f.*, cp.is_cup FROM fixtures f JOIN competitions cp ON cp.league_id=f.league_id", c, parse_dates=["kickoff_utc"])
    fx["kickoff_utc"] = pd.to_datetime(fx.kickoff_utc, utc=True)
    wanted = parse_list(a.list)
    ids = []
    for comp, h, aw in wanted:
        lid = ALL[comp][0]; th, ta = match_team(h, teams), match_team(aw, teams)
        if th is None or ta is None: print(f"  team not found: {h if th is None else aw} ({comp})"); continue
        row = fx[(fx.league_id == lid) & (fx.home_id == th) & (fx.away_id == ta) & ((fx.status == "NS") | a.allow_played)]
        if a.allow_played and len(row) > 1: row = row.sort_values("kickoff_utc").tail(1)
        if len(row) == 0: print(f"  fixture not found or not scheduled: {h} v {aw} ({comp})"); continue
        ids.append((comp, int(row.iloc[0].fixture_id)))
    horizon = fx[fx.fixture_id.isin([i for _, i in ids])].kickoff_utc.max()
    X = build(a.db, upcoming_to=str(horizon)); X = X[X.fixture_id.isin([i for _, i in ids])].copy()
    bundle = pickle.load(open(os.path.join(HERE, "bands_model.pkl"), "rb"))
    X["p"] = band_predict(bundle, X); G, Amb = bundle["green"], bundle["amber"]
    bb = pickle.load(open(os.path.join(HERE, "btts_model.pkl"), "rb")); X["p_btts"] = btts_predict(bb, X)
    X["light"] = np.where(X.p >= G, "GREEN", np.where(X.p >= Amb, "AMBER", "RED"))
    compof = {i: cpt for cpt, i in ids}; X["comp"] = X.fixture_id.map(compof)
    X["order"] = X.comp.map({n: i for i, n in enumerate(ORDER)})
    X["home"] = X.home_id.map(teams); X["away"] = X.away_id.map(teams)
    X = X.sort_values(["order", "home"])
    lg_ga = {}
    for lid in X.league_id.unique():
        g = fx[(fx.league_id == lid) & (fx.season == 2026) & fx.ft_home.notna()]; lg_ga[lid] = float((g.ft_home + g.ft_away).mean() / 2) if len(g) else np.nan
    rows, cards, short = [], [], []
    for r in X.itertuples():
        hr = last_n(fx, r.home_id, r.season, r.kickoff_utc, 5); ar = last_n(fx, r.away_id, r.season, r.kickoff_utc, 5)
        hv = last_n(fx, r.home_id, r.season, r.kickoff_utc, 3, "H"); av = last_n(fx, r.away_id, r.season, r.kickoff_utc, 3, "A")
        hv5 = last_n(fx, r.home_id, r.season, r.kickoff_utc, 5, "H"); av5 = last_n(fx, r.away_id, r.season, r.kickoff_utc, 5, "A")
        m1, t1 = rate(hr, ar, 3, 3); m2, t2 = rate(ar, hr, 3, 3); prof = profile(m1, m2, hr, ar)
        ev_for, ev_against = for_(hr, ar, hv, av), against(hr, ar, hv, av, teams)
        light = r.light
        if len(hr) < 3 or len(ar) < 3: light = "RED"; ev_against.append("Fewer than 3 league games for one side: not enough evidence")
        if light == "GREEN" and prof == "Mixed": light = "AMBER"; ev_against.append("Match-up contradicts the headline numbers (neither attack-v-defence route is strong)")
        if prof == "Chaos": ev_against.append("Goals rely on poor defending rather than proven attacks")
        oq_h = opp_quality(hr, fx, r.season, r.kickoff_utc, lg_ga[r.league_id]); oq_a = opp_quality(ar, fx, r.season, r.kickoff_utc, lg_ga[r.league_id])
        xg = "Unavailable"
        if not np.isnan(r.h_l5_xg_f) and not np.isnan(r.a_l5_xg_f):
            xg = (f"Home xG {r.h_l5_xg_f:.2f} for / {r.h_l5_xg_a:.2f} against per game, SOT {r.h_l5_shots_on_target_f:.1f}; "
                  f"Away xG {r.a_l5_xg_f:.2f} for / {r.a_l5_xg_a:.2f} against, SOT {r.a_l5_shots_on_target_f:.1f} (last 5, all competitions)")
        elif not np.isnan(r.h_l5_shots_on_target_f) and not np.isnan(r.a_l5_shots_on_target_f):
            xg = f"Shots on target per game: home {r.h_l5_shots_on_target_f:.1f} for / {r.h_l5_shots_on_target_a:.1f} faced; away {r.a_l5_shots_on_target_f:.1f} for / {r.a_l5_shots_on_target_a:.1f} faced. xG not covered"
        btts_lab = btts_label(bb, float(r.p_btts))
        pattern, why, risk, route = pattern_text(r.home, r.away, hr, ar, hv5, av5, ev_against)
        btts_yes = pattern == "Both teams contribute"      # verdict follows the pattern; the model gives the likelihood
        d = dict(comp=r.comp, hv5=hv5, av5=av5, p_btts=round(float(r.p_btts), 3), btts=("YES" if btts_yes else "NO"), btts_lik=btts_lab.title(),
                 pattern=pattern, why=why, risk=risk, route=route, kickoff=r.kickoff_utc.tz_convert("Europe/London").strftime("%a %d %b %H:%M"), fixture=f"{r.home} v {r.away}",
                 h_l5=f"{sum(x['gf'] for x in hr)}-{sum(x['ga'] for x in hr)}", h_seq=seq(hr), h_over=f"{cnt(hr, lambda x: x['tot']>=3)}/{len(hr)}",
                 a_l5=f"{sum(x['gf'] for x in ar)}-{sum(x['ga'] for x in ar)}", a_seq=seq(ar), a_over=f"{cnt(ar, lambda x: x['tot']>=3)}/{len(ar)}",
                 h_ven=f"{sum(x['gf'] for x in hv)}-{sum(x['ga'] for x in hv)} ({len(hv)})", a_ven=f"{sum(x['gf'] for x in av)}-{sum(x['ga'] for x in av)} ({len(av)})",
                 profile=prof, light=light, m1=m1, m1txt=t1, m2=m2, m2txt=t2, xg=xg, ev_for=ev_for, ev_against=ev_against, p=round(float(r.p), 3),
                 oq_h=oq_h, oq_a=oq_a, hr=hr, ar=ar, hv=hv, av=av, home=r.home, away=r.away, fixture_id=int(r.fixture_id))
        rows.append(d)
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.db)), f"over25_analysis_{pd.Timestamp.now():%Y%m%d}")
    pd.DataFrame([{k: v for k, v in d.items() if k not in ("hr", "ar", "hv", "av", "hv5", "av5", "ev_for", "ev_against")} | {"ev_for": "; ".join(d["ev_for"]), "ev_against": "; ".join(d["ev_against"])} for d in rows]).to_csv(out + ".csv", index=False)
    pickle.dump(rows, open(out + ".pkl", "wb"))
    # structured prediction log (one row per fixture per run), scored later by review.py
    logp = os.path.join(os.path.dirname(os.path.abspath(a.db)), "predictions_log.csv")
    cnt_ = lambda rs, f: sum(1 for x in rs if f(x))
    log = pd.DataFrame([dict(run_date=pd.Timestamp.now().strftime("%Y-%m-%d"), model_version="v4", generated_at=pd.Timestamp.now(tz="Europe/London").strftime("%Y-%m-%d %H:%M"),
                             fixture_id=d["fixture_id"], league_id=ALL[d["comp"]][0], comp=d["comp"], fixture=d["fixture"], home=d["home"], away=d["away"], kickoff=d["kickoff"],
                             over25=("YES" if d["light"] != "RED" else "NO"), confidence={"GREEN": "High", "AMBER": "Medium", "RED": "Rejected"}[d["light"]], p=d["p"],
                             btts=d["btts"], btts_likelihood=d["btts_lik"], p_btts=d["p_btts"], pattern=d["pattern"],
                             h_over=cnt_(d["hr"], lambda x: x["tot"] >= 3), a_over=cnt_(d["ar"], lambda x: x["tot"] >= 3),
                             h_s1=cnt_(d["hr"], lambda x: x["gf"] >= 1), a_s1=cnt_(d["ar"], lambda x: x["gf"] >= 1), h_s2=cnt_(d["hr"], lambda x: x["gf"] >= 2), a_s2=cnt_(d["ar"], lambda x: x["gf"] >= 2),
                             h_c1=cnt_(d["hr"], lambda x: x["ga"] >= 1), a_c1=cnt_(d["ar"], lambda x: x["ga"] >= 1), h_c2=cnt_(d["hr"], lambda x: x["ga"] >= 2), a_c2=cnt_(d["ar"], lambda x: x["ga"] >= 2),
                             h_btts=cnt_(d["hr"], lambda x: x["gf"] > 0 and x["ga"] > 0), a_btts=cnt_(d["ar"], lambda x: x["gf"] > 0 and x["ga"] > 0),
                             h_cs=cnt_(d["hr"], lambda x: x["ga"] == 0), a_cs=cnt_(d["ar"], lambda x: x["ga"] == 0), h_fts=cnt_(d["hr"], lambda x: x["gf"] == 0), a_fts=cnt_(d["ar"], lambda x: x["gf"] == 0),
                             h_n=len(d["hr"]), a_n=len(d["ar"]), hv_over=cnt_(d["hv5"], lambda x: x["tot"] >= 3), hv_n=len(d["hv5"]), av_over=cnt_(d["av5"], lambda x: x["tot"] >= 3), av_n=len(d["av5"]),
                             catch="; ".join(d["ev_against"]), why=d["why"], risk=d["risk"], score="", over25_result="", btts_result="") for d in rows])
    if os.path.exists(logp):
        old = pd.read_csv(logp); old = old[~(old.fixture_id.isin(log.fixture_id) & (old.run_date == log.run_date.iloc[0]))]; log = pd.concat([old, log])
    log.to_csv(logp, index=False)
    write_md(rows, out + ".md", teams)
    print(f"{len(rows)} fixtures analysed -> {out}.md / .csv")
    print(pd.Series([d["light"] for d in rows]).value_counts().to_string())

LIGHT = {"GREEN": "🟢", "AMBER": "🟡", "RED": "🔴"}

def write_md(rows, path, teams):
    L = ["# 3+ Goals Fixture Analysis", ""]
    L.append("Light: 🟢 go, 🟡 possible with a stated catch, 🔴 no. L5 = goals for-against over the last 5 league games this season, oldest to newest. "
             "Venue = last 3 home (or away) league games, games in brackets. Profile: Open = both ends, Dominant = one-way, Chaos = both defences leaking, Mixed = contradictory.")
    L.append("")
    cur = None
    for d in rows:
        if d["comp"] != cur:
            cur = d["comp"]; L += ["", f"## {cur}", "", "| Fixture | When | Home L5 | Home 3+ | Away L5 | Away 3+ | Home venue | Away venue | Profile | Light |", "|---|---|---|---|---|---|---|---|---|---|"]
        L.append(f"| {d['fixture']} | {d['kickoff']} | {d['h_l5']} · {d['h_seq']} | {d['h_over']} | {d['a_l5']} · {d['a_seq']} | {d['a_over']} | {d['h_ven']} | {d['a_ven']} | {d['profile']} | {LIGHT[d['light']]} |")
    greens = [d for d in rows if d["light"] == "GREEN"]
    L += ["", "# Green fixture cards", ""]
    for d in greens:
        hr, ar = d["hr"], d["ar"]
        L += [f"## {d['fixture']}  ({d['comp']}, {d['kickoff']})", "",
              f"**{d['home']}, last 5:** {d['h_seq']}  ·  GF {sum(x['gf'] for x in hr)} GA {sum(x['ga'] for x in hr)}  ·  {sum(x['gf'] for x in hr)/max(len(hr),1):.1f} / {sum(x['ga'] for x in hr)/max(len(hr),1):.1f} per game  ·  3+ in {d['h_over']}  ·  BTTS in {cnt(hr, lambda x: x['gf']>0 and x['ga']>0)}/{len(hr)}",
              f"Opponents: " + ", ".join(f"{teams[x['opp']]} ({x['ven']})" for x in hr), "",
              f"**{d['away']}, last 5:** {d['a_seq']}  ·  GF {sum(x['gf'] for x in ar)} GA {sum(x['ga'] for x in ar)}  ·  {sum(x['gf'] for x in ar)/max(len(ar),1):.1f} / {sum(x['ga'] for x in ar)/max(len(ar),1):.1f} per game  ·  3+ in {d['a_over']}  ·  BTTS in {cnt(ar, lambda x: x['gf']>0 and x['ga']>0)}/{len(ar)}",
              f"Opponents: " + ", ".join(f"{teams[x['opp']]} ({x['ven']})" for x in ar), "",
              f"**Venue:** {d['home']} last 3 home {d['h_ven']}, 3+ in {cnt(d['hv'], lambda x: x['tot']>=3)}/{len(d['hv'])}  ·  {d['away']} last 3 away {d['a_ven']}, 3+ in {cnt(d['av'], lambda x: x['tot']>=3)}/{len(d['av'])}", "",
              f"**Home attack v away defence: {d['m1']}.** {d['m1txt']}", f"**Away attack v home defence: {d['m2']}.** {d['m2txt']}", "",
              f"**Opposition quality:** " + (f"{d['home']}'s opponents concede {d['oq_h'][0]:.2f}/g (division average {d['oq_h'][1]:.2f}); " if d['oq_h'] else "") + (f"{d['away']}'s opponents concede {d['oq_a'][0]:.2f}/g (division average {d['oq_a'][1]:.2f})" if d['oq_a'] else ""), "",
              f"**Underlying performance:** {d['xg']}", "", f"**Profile:** {d['profile']}", "",
              "**Evidence for 3+:** " + ("; ".join(d["ev_for"]) if d["ev_for"] else "none beyond the division rate"), "",
              "**Evidence against 3+:** " + ("; ".join(d["ev_against"]) if d["ev_against"] else "no specific counter-evidence in the last 5 or venue games"), ""]
    L += ["", "# Strongest 3+ goal candidates", "", "| League | Fixture | Profile | Key supporting evidence | Main risk |", "|---|---|---|---|---|"]
    for d in greens:
        L.append(f"| {d['comp']} | {d['fixture']} | {d['profile']} | {d['ev_for'][0] if d['ev_for'] else 'division rate'} | {d['ev_against'][0] if d['ev_against'] else 'none identified'} |")
    open(path, "w", encoding="utf-8").write("\n".join(L))

if __name__ == "__main__":
    main()
