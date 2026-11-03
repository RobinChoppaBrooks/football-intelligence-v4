"""
benchmarks.py  -  the one place the V4.1 benchmark numbers come from (Phase 0 clean-up, 2 Nov 2026).

    python3 benchmarks.py [football.db]     recompute and write config/benchmarks.json
    from benchmarks import text, btts_text  one-line summaries for reports (read config/benchmarks.json, no recompute)

Before this file the benchmark was typed by hand in three scripts and they disagreed (65% / 69% / 69% on different
windows). Now every report reads config/benchmarks.json, which this script writes from football.db.

What is measured: every finished league fixture of season 2026-27 in Rob's 14 leagues (config/competitions.json),
classified exactly as production does: model score against the locked cut points (bands_model.pkl), rejected when a side has
fewer than 3 league games, and Rob's trump card (both attacks scored 2+ in 4+ of 5, both defences let in 2+ in 1 or fewer,
both sides with 5 games) counted on its own, not inside High. 2026-27 is the only clean out-of-sample season: the model was
trained on 2023-24 and 2024-25 and its cut points were chosen on 2025-26. Counts only. Nothing here changes a prediction.

European cups (Champions League, Europa League, Conference League; added to every run on 3 Nov 2026 at Rob's request) are
measured separately in "european_cups", same season and same rules, because cup ties are not part of the 14-league benchmark.
"""
import os, sys, json, pickle
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "config", "benchmarks.json")
SEASON = 2026

def _classify(X, bb, tb):
    import numpy as np
    from bands import predict as band_predict
    from btts import predict as btts_predict
    X = X.copy(); X["p"] = band_predict(bb, X); X["pb"] = btts_predict(tb, X)
    cnt = lambda col: np.rint(5 * X[col]).astype("Int64")
    full = (X.h_l5L_n >= 5) & (X.a_l5L_n >= 5)
    trump = full & (cnt("h_l5L_gf2") >= 4) & (cnt("a_l5L_gf2") >= 4) & (cnt("h_l5L_ga2") <= 1) & (cnt("a_l5L_ga2") <= 1)
    thin = (X.h_l5L_n.fillna(0) < 3) | (X.a_l5L_n.fillna(0) < 3)
    cls = np.where(thin, "rejected", np.where(X.p >= bb["green"], "High", np.where(X.p >= bb["amber"], "Medium", "rejected")))
    X["cls"] = np.where(trump & ~thin, "Trump card", cls)
    y, yb = X.target_over25 == 1, X.target_btts == 1
    kn = lambda m, t: {"hits": int((t & m).sum()), "n": int(m.sum())}
    over = {c: kn(X.cls == c, y) for c in ("High", "Medium", "Trump card", "rejected")}
    over["Selected (High, Medium, Trump card)"] = kn(X.cls != "rejected", y)
    btts = {"High band": kn(X.pb >= tb["high"], yb), "Medium band": kn((X.pb >= tb["medium"]) & (X.pb < tb["high"]), yb), "Low band": kn(X.pb < tb["medium"], yb)}
    return over, btts, int(len(X))

def compute(db):
    from features import build
    comp = json.load(open(os.path.join(HERE, "config", "competitions.json")))
    allc = comp["english"] + comp["european"]
    leagues = [c["league_id"] for c in allc if not c.get("is_cup")]
    cups = [c["league_id"] for c in allc if c.get("is_cup")]
    X = build(db)
    X = X[(X.season == SEASON) & X.target_over25.notna()]
    bb = pickle.load(open(os.path.join(HERE, "bands_model.pkl"), "rb")); tb = pickle.load(open(os.path.join(HERE, "btts_model.pkl"), "rb"))
    L = X[X.league_id.isin(leagues)]
    over, btts, n = _classify(L, bb, tb)
    res = {"as_of": str(L.kickoff_utc.max().tz_convert("Europe/London").date()), "season": "2026-27", "fixtures": n,
           "scope": "every finished league fixture in Rob's 14 leagues, season 2026-27, classified as production does",
           "why_this_window": "only clean out-of-sample season: model trained on 2023-24 and 2024-25, cut points chosen on 2025-26",
           "over25": over, "btts": btts, "note": "classified with information up to each kick-off; a live run uses information up to the run, so a few fixtures sit either side of a line differently", "written_by": "benchmarks.py"}
    if cups:
        C = X[X.league_id.isin(cups)]
        co, cb, cn = _classify(C, bb, tb)
        res["european_cups"] = {"fixtures": cn, "scope": "every finished Champions League, Europa League and Conference League fixture of season 2026-27 (qualifiers included), same rules; a side with fewer than 3 domestic league games is rejected",
                                "over25": co, "btts": cb}
    return res

def _load():
    return json.load(open(OUT)) if os.path.exists(OUT) else None

def _c(d): return f"{d['hits']} of {d['n']}"

def text():
    b = _load()
    if not b: return "Benchmark unavailable (config/benchmarks.json missing)."
    o = b["over25"]
    return (f"Benchmark, season {b['season']} to {b['as_of']} ({b['fixtures']} finished fixtures, Rob's 14 leagues, clean out of sample): "
            f"3+ goals in High {_c(o['High'])}, Medium {_c(o['Medium'])}, trump card {_c(o['Trump card'])}, rejected {_c(o['rejected'])}. "
            "Band counts, not the chance of any one fixture.")

def cups_text():
    b = _load()
    if not b or "european_cups" not in b: return ""
    e = b["european_cups"]; o = e["over25"]
    return (f"European cups (Champions, Europa and Conference League), measured separately, season {b['season']} ({e['fixtures']} finished ties): "
            f"3+ goals in High {_c(o['High'])}, Medium {_c(o['Medium'])}, trump card {_c(o['Trump card'])}, rejected {_c(o['rejected'])}. "
            "Cup ties are outside the 14-league benchmark; treat cup selections with that in mind.")

def btts_text():
    b = _load()
    if not b: return ""
    t = b["btts"]
    return f"BTTS model bands, same fixtures: High {_c(t['High band'])}, Medium {_c(t['Medium band'])}, Low {_c(t['Low band'])} had both teams score."

if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "football.db")
    res = compute(db)
    json.dump(res, open(OUT, "w"), indent=1)
    print(json.dumps(res, indent=1)); print(text()); print(btts_text()); print(cups_text())
