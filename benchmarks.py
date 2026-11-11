"""
benchmarks.py  -  the one place the benchmark numbers come from (Phase 0 clean-up, 2 Nov 2026; V4.2 rules 11 Nov 2026).

    python3 benchmarks.py [football.db]     recompute and write config/benchmarks.json
    from benchmarks import text, cups_text  one-line summaries for reports (read config/benchmarks.json, no recompute)

Before this file the benchmark was typed by hand in three scripts and they disagreed (65% / 69% / 69% on different
windows). Now every report reads config/benchmarks.json, which this script writes from football.db.

What is measured: every finished league fixture of season 2026-27 in Rob's 14 leagues (config/competitions.json),
classified exactly as production does: model score against the cut points (bands_model.pkl), rejected when a side has
fewer than 3 league games, and Rob's V4.2 whale trump card (a side with 16+ goals in its last 5 league games, opponent kept
fewer than 2 clean sheets, both sides with 5 games) counted on its own, not inside High. FT results only. 2026-27 is the only clean out-of-sample season: the model was
trained on 2023-24 and 2024-25 and its cut points were chosen on 2025-26. Counts only. Nothing here changes a prediction.

Cup competitions (Champions, Europa and Conference League and the domestic cups of the 14 leagues' countries; added to every run on 3 Nov 2026 at Rob's request) are
measured separately in "european_cups", same season and same rules, because cup ties are not part of the 14-league benchmark.
"""
import os, sys, json, pickle
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "config", "benchmarks.json")
SEASON = 2026
WHALE_GOALS = 16

def _classify(X, bb):
    """V4.2: counts-only model score against the stored 3-decimal cut points, rejected when a side has fewer than 3 league
    games, and Rob's whale trump card (16+ goals in a side's last 5, opponent kept fewer than 2 clean sheets) on its own."""
    import numpy as np
    from bands import predict as band_predict, band_of
    X = X.copy(); X["p"] = band_predict(bb, X).round(3)
    full = (X.h_l5_n >= 5) & (X.a_l5_n >= 5)
    trump = full & (((X.h_l5_gf_cnt >= WHALE_GOALS) & (X.a_l5_cs_cnt < 2)) | ((X.a_l5_gf_cnt >= WHALE_GOALS) & (X.h_l5_cs_cnt < 2)))
    thin = (X.h_l5_n.fillna(0) < 3) | (X.a_l5_n.fillna(0) < 3)
    cls = np.array([band_of(p, bb) for p in X.p], dtype=object); cls[thin.values] = "rejected"
    X["cls"] = np.where(trump & ~thin, "Trump card", cls)
    y = X.target_over25 == 1
    kn = lambda m, t: {"hits": int((t & m).sum()), "n": int(m.sum())}
    over = {c: kn(X.cls == c, y) for c in ("High", "Medium", "Weak", "Trump card", "rejected")}
    over["Selected (High, Medium, Weak, Trump card)"] = kn(X.cls != "rejected", y)
    return over, int(len(X))

def compute(db):
    from features import build
    comp = json.load(open(os.path.join(HERE, "config", "competitions.json")))
    allc = comp["english"] + comp["european"]
    leagues = [c["league_id"] for c in allc if not c.get("is_cup")]
    cups = [c["league_id"] for c in allc if c.get("is_cup")]
    X = build(db)
    X = X[(X.season == SEASON) & X.target_over25.notna()]
    bb = pickle.load(open(os.path.join(HERE, "bands_model.pkl"), "rb"))
    L = X[X.league_id.isin(leagues)]
    over, n = _classify(L, bb)
    res = {"as_of": str(L.kickoff_utc.max().tz_convert("Europe/London").date()), "season": "2026-27", "fixtures": n,
           "scope": "every finished league fixture in Rob's 14 leagues, season 2026-27, classified as production does",
           "why_this_window": "only clean out-of-sample season: model trained on 2023-24 and 2024-25, cut points chosen on 2025-26",
           "model_version": bb.get("model_version", "v4.1"), "over25": over, "note": "classified with information up to each kick-off; a live run uses information up to the run, so a few fixtures sit either side of a line differently", "written_by": "benchmarks.py"}
    if cups:
        C = X[X.league_id.isin(cups)]
        co, cn = _classify(C, bb)
        res["european_cups"] = {"fixtures": cn, "scope": "every finished fixture of season 2026-27 in the cup competitions of config/competitions.json (Champions, Europa and Conference League and the domestic cups; qualifiers and early rounds included), same rules; a side with fewer than 3 domestic league games is rejected",
                                "over25": co}
    return res

def _load():
    return json.load(open(OUT)) if os.path.exists(OUT) else None

def _c(d): return f"{d['hits']} of {d['n']}"

def text():
    b = _load()
    if not b: return "Benchmark unavailable (config/benchmarks.json missing)."
    o = b["over25"]
    return (f"Benchmark, season {b['season']} to {b['as_of']} ({b['fixtures']} finished fixtures, Rob's 14 leagues, clean out of sample): "
            f"3+ goals in High {_c(o['High'])}, Medium {_c(o['Medium'])}, Weak {_c(o['Weak'])}, trump card {_c(o['Trump card'])}, rejected {_c(o['rejected'])}. "
            "Band counts, not the chance of any one fixture.")

def cups_text():
    b = _load()
    if not b or "european_cups" not in b: return ""
    e = b["european_cups"]; o = e["over25"]
    return (f"Cup competitions (European and domestic cups), measured separately, season {b['season']} ({e['fixtures']} finished ties): "
            f"3+ goals in High {_c(o['High'])}, Medium {_c(o['Medium'])}, Weak {_c(o['Weak'])}, trump card {_c(o['Trump card'])}, rejected {_c(o['rejected'])}. "
            "Cup ties are outside the 14-league benchmark; treat cup selections with that in mind.")

if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "football.db")
    res = compute(db)
    json.dump(res, open(OUT, "w"), indent=1)
    print(json.dumps(res, indent=1)); print(text()); print(cups_text())
