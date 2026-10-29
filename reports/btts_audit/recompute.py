"""Independent recomputation of the last-five evidence for every fixture in the 29 Oct 2026 weekend run.

Reads only football.db (stored final scores) and the run's committed outputs. Does not import the repo's analysis code,
so the two are independent. Writes recompute_<date>.csv with the recomputed counts next to the published ones.
"""
import sys, json, pickle, sqlite3, pandas as pd, numpy as np
repo, date, out = sys.argv[1], sys.argv[2], sys.argv[3]
c = sqlite3.connect(f"{repo}/football.db")
fx = pd.read_sql("select f.*, cp.is_cup from fixtures f join competitions cp on cp.league_id=f.league_id", c)
fx["kickoff_utc"] = pd.to_datetime(fx.kickoff_utc, utc=True)
teams = dict(c.execute("select team_id, name from teams"))
FIN = ("FT", "AET", "PEN")

pred = json.load(open(f"{repo}/reports/weekend/{date}/predictions_{date}.json"))
run_id = pred[0]["run_id"]
rows = []
for s in ("english", "european"):
    rows += pickle.load(open(f"{repo}/runs/{run_id}/analysis_{s}.pkl", "rb"))
byid = {d["fixture_id"]: d for d in rows}
assert len(byid) == len(pred) == 274, (len(byid), len(pred))

def last5(tid, season, before, venue=None, finished_only=True):
    g = fx[(fx.season == season) & (fx.kickoff_utc < before) & fx.ft_home.notna() & (fx.is_cup == 0)]
    if finished_only: g = g[g.status.isin(FIN)]
    if venue == "H": g = g[g.home_id == tid]
    elif venue == "A": g = g[g.away_id == tid]
    else: g = g[(g.home_id == tid) | (g.away_id == tid)]
    g = g.sort_values("kickoff_utc").tail(5)
    o = []
    for r in g.itertuples():
        home = r.home_id == tid
        o.append(dict(gf=int(r.ft_home if home else r.ft_away), ga=int(r.ft_away if home else r.ft_home), status=r.status, fid=int(r.fixture_id), ko=r.kickoff_utc))
    return o

def counts(rs):
    n = lambda f: sum(1 for x in rs if f(x))
    return dict(n=len(rs), s1=n(lambda x: x["gf"] >= 1), s2=n(lambda x: x["gf"] >= 2), c1=n(lambda x: x["ga"] >= 1), c2=n(lambda x: x["ga"] >= 2),
                btts=n(lambda x: x["gf"] > 0 and x["ga"] > 0), cs=n(lambda x: x["ga"] == 0), fts=n(lambda x: x["gf"] == 0), o25=n(lambda x: x["gf"] + x["ga"] >= 3),
                seq="; ".join(f"{x['gf']}-{x['ga']}" for x in rs))

recs = []
for p in pred:
    f = fx[fx.fixture_id == p["fixture_id"]].iloc[0]
    d = byid[p["fixture_id"]]
    rec = dict(fixture_id=p["fixture_id"], competition=p["competition"], kickoff_uk=p["kickoff_uk"], home=p["home"], away=p["away"],
               classification=p["classification"], btts=p["btts"], btts_likelihood=p["btts_likelihood"], pattern=p["pattern"], p_btts=d["p_btts"], model_score=p["model_score"],
               status_now=f.status, risk=p["risk"])
    for side, tid, pub in (("h", f.home_id, "home"), ("a", f.away_id, "away")):
        r5 = last5(tid, f.season, f.kickoff_utc)
        r5_any = last5(tid, f.season, f.kickoff_utc, finished_only=False)
        v5 = last5(tid, f.season, f.kickoff_utc, "H" if side == "h" else "A")
        cnt = counts(r5); cv = counts(v5)
        for k, v in cnt.items(): rec[f"{side}_{k}"] = v
        for k in ("n", "btts", "cs", "fts", "o25", "s1", "c1"): rec[f"{side}v_{k}"] = cv[k]
        rec[f"{side}_nonfinished_in_window"] = sum(1 for x in r5_any if x["status"] not in FIN)
        # published values
        pr = d["hr"] if side == "h" else d["ar"]
        rec[f"{side}_pub_seq"] = "; ".join(f"{x['gf']}-{x['ga']}" for x in pr)
        rec[f"{side}_pub_s2"] = p[f"{pub}_scored2"]; rec[f"{side}_pub_c2"] = p[f"{pub}_letin2"]
        rec[f"{side}_seq_match"] = rec[f"{side}_pub_seq"] == cnt["seq"]
    recs.append(rec)
R = pd.DataFrame(recs)
R.to_csv(out, index=False)
print(len(R), "fixtures recomputed")
print("sequence mismatches home/away:", int((~R.h_seq_match).sum()), int((~R.a_seq_match).sum()))
print("scored2 mismatches:", int((R.h_s2 != R.h_pub_s2).sum() + (R.a_s2 != R.a_pub_s2).sum()), " letin2 mismatches:", int((R.h_c2 != R.h_pub_c2).sum() + (R.a_c2 != R.a_pub_c2).sum()))
print("non-finished (ABD/AWD/Canc) games inside a last-5 window:", int(R.h_nonfinished_in_window.sum() + R.a_nonfinished_in_window.sum()))
print("sides with fewer than 5 league games:", int(((R.h_n < 5) | (R.a_n < 5)).sum()))
