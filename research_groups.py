"""
research_groups.py  -  research watchlists for each prediction run, and their scoring in the results review (2 Nov 2026).
Reporting only: reads the run's own outputs and never changes a classification, score, threshold or BTTS call.

    python3 research_groups.py build <run_id>     after run_v4.py: writes reports/research_groups/<run_id>.csv
    python3 research_groups.py review             after run_v4.py review: writes reports/performance/research_groups_<date>.md

build: one row per fixture of the run (the run's rows in data/predictions/predictions_log.csv are the canonical record; the
       combined CSV adds the display fields). Adds, frozen before kick-off:
         rank_all          position by V4.1 model score, highest first (all eligible fixtures)
         top10_rejected    1..10 for the ten highest-scoring fixtures V4.1 classified as rejected, else blank
         open_game         EXPERIMENTAL category A / B / C from open_game.py (2 Nov definitions), blank when a side lacks
                           five earlier games with goal events
       The file is written once per run and never regenerated (pass --force only to rebuild a run that has not kicked off).

review: for every run that has a groups file, scores five groups on completed fixtures only (results_log.csv, which holds
        FT / AET / PEN results only, so postponed, abandoned and void games are excluded exactly as in the main review):
          A official High   B official Medium (includes the report's Weak)   C top 10 rejected   D open-game category A
          E all eligible fixtures (baseline)
        with overlaps, so nothing is double-counted, and for group D whether the 3+ goals came from both sides or one.
"""
import os, sys, json, math, datetime as dt
import pandas as pd

LOGP, RESP, GDIR = "data/predictions/predictions_log.csv", "data/results/results_log.csv", "reports/research_groups"
MEDIUM_CUT = 0.58084   # from config/model_config.json (cut_medium), for display only ('how far below the line')

def _paths(run_id):
    mode, st = run_id.split("_")[0], run_id.split("_")[1]; date = f"{st[:4]}-{st[4:6]}-{st[6:8]}"
    return mode, date, f"reports/{'range' if mode == 'range' else mode}/{date}"

def build(run_id, force=False):
    out = f"{GDIR}/{run_id}.csv"
    if os.path.exists(out) and not force:
        print(f"{out} exists; groups are frozen at run time and are not regenerated"); return out
    mode, date, outdir = _paths(run_id)
    log = pd.read_csv(LOGP, dtype=str); R = log[log.run_id == run_id].copy()
    if R.empty: raise SystemExit(f"no rows for {run_id} in {LOGP}")
    R["model_score"] = R.model_score.astype(float)
    comb = f"{outdir}/combined_{date}.csv"
    if os.path.exists(comb):
        C = pd.read_csv(comb, dtype={"fixture_id": str})[["fixture_id", "model_confidence", "rejection_reason", "home_scores", "away_scores"]]
        R = R.merge(C.rename(columns={"model_confidence": "report_label"}), on="fixture_id", how="left")
    else:
        R["report_label"] = R.classification; R["rejection_reason"] = ""; R["home_scores"] = R.home_last5; R["away_scores"] = R.away_last5
    R = R.sort_values("model_score", ascending=False).reset_index(drop=True); R["rank_all"] = R.index + 1
    rej = R[R.classification == "rejected"].head(10).index
    R["top10_rejected"] = ""; R.loc[rej, "top10_rejected"] = [str(i + 1) for i in range(len(rej))]
    # experimental open-game category, pre-match: only games that kicked off before this run was generated
    R["open_game"] = ""; R["open_game_detail"] = ""
    try:
        from open_game import load_games, assess
        games, names, usable, _ = load_games("football.db")
        by_name = {}
        for t in games: by_name.setdefault(names.get(t), t)
        cutoff = pd.Timestamp(R.generated_at.iloc[0], tz="Europe/London").tz_convert("UTC").isoformat()
        import sqlite3
        db = sqlite3.connect("football.db")
        ids = dict(((str(f), (h, a)) for f, h, a in db.execute("SELECT fixture_id, home_id, away_id FROM fixtures")))
        for i, r in R.iterrows():
            h, a = ids.get(str(r.fixture_id), (None, None))
            res = assess(games, h, a, cutoff) if h else None
            if res is None: continue
            R.at[i, "open_game"] = res["category"]
            R.at[i, "open_game_detail"] = json.dumps(dict((k, v) for k, v in res.items() if k not in ("examples_home", "examples_away")) | {"examples_home": res["examples_home"], "examples_away": res["examples_away"]})
    except Exception as e:
        print(f"open-game labels skipped: {e}")
    keep = ["run_id", "fixture_id", "competition", "kickoff_uk", "home", "away", "model_score", "classification", "report_label", "rank_all", "top10_rejected", "open_game",
            "h_s2", "h_c2", "a_s2", "a_c2", "h_cs", "a_cs", "h_fts", "a_fts", "drivers20", "home_scores", "away_scores", "rejection_reason", "open_game_detail"]
    os.makedirs(GDIR, exist_ok=True); R[[c for c in keep if c in R.columns]].to_csv(out, index=False)
    print(f"{out}: {len(R)} fixtures, top-10 rejected {len(rej)}, open-game A {int((R.open_game == 'A').sum())}, labelled {int((R.open_game != '').sum())}")
    return out

def _wilson(k, n):
    if n == 0: return "-"
    p = k / n; z = 1.96; d = 1 + z * z / n; c = p + z * z / (2 * n); s = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return f"{(c - s) / d * 100:.0f} to {(c + s) / d * 100:.0f}%"

def review():
    if not os.path.isdir(GDIR): print("no research groups yet"); return
    res = pd.read_csv(RESP, dtype=str) if os.path.exists(RESP) else pd.DataFrame(columns=["run_id", "fixture_id", "score", "over25_result"])
    frames = [pd.read_csv(f"{GDIR}/{f}", dtype=str) for f in sorted(os.listdir(GDIR)) if f.endswith(".csv")]
    if not frames: print("no research groups yet"); return
    G = pd.concat(frames).merge(res[["run_id", "fixture_id", "score", "over25_result"]], on=["run_id", "fixture_id"], how="left")
    G["done"] = G.over25_result.isin(["Y", "N"]); G["over"] = G.over25_result == "Y"
    groups = [("A", "Official High", G.classification == "High"), ("B", "Official Medium (incl. report Weak)", G.classification == "Medium"),
              ("C", "Top 10 rejected by model score", G.top10_rejected.fillna("") != ""), ("D", "EXPERIMENTAL open-game category A", G.open_game == "A"),
              ("E", "All eligible fixtures (baseline)", pd.Series(True, index=G.index))]
    today = dt.date.today()
    L = [f"# Research groups review {today:%Y-%m-%d}", "", "Groups are fixed before kick-off in reports/research_groups/<run_id>.csv and never regenerated. Only completed fixtures with a stored "
         "FT / AET / PEN result count; postponed, abandoned and void games are left out as in the main review. A fixture can sit in more than one group: "
         "the overlap table shows how many, so groups are compared side by side, never added together. Group B includes the fixtures the report labels Weak "
         "(the bottom quarter of Medium); the prediction log stores them as Medium.", ""]
    def table(g):
        out = ["| group | fixtures evaluated | over 2.5 | under 2.5 | hit rate | 95% range | not yet played |", "|---|---|---|---|---|---|---|"]
        for code, name, mask in groups:
            s = g[mask.loc[g.index]]; d = s[s.done]; k = int(d.over.sum()); n = len(d)
            out.append(f"| {code}. {name} | {n} | {k} | {n - k} | {f'{k / n * 100:.0f}%' if n else '-'} | {_wilson(k, n)} | {int((~s.done).sum())} |")
        return out
    L += ["## All runs with groups", ""] + table(G)
    sel = G[G.classification.isin(["High", "Medium"]) & G.done]; ks, ns = int(sel.over.sum()), len(sel)
    L += ["", f"Official selections combined (A + B): {ks} of {ns} completed fixtures over 2.5. Groups C and D are research candidates, never selections; compare them with this line."]
    # overlaps on completed fixtures
    D = G[G.done]; codes = [c for c, _, _ in groups[:4]]; masks = {c: m.loc[D.index] for c, _, m in groups[:4]}
    L += ["", "## Overlap (completed fixtures in both groups)", "", "| | " + " | ".join(codes) + " |", "|---|" + "---|" * len(codes)]
    for a in codes: L.append(f"| {a} | " + " | ".join(str(int((masks[a] & masks[b]).sum())) for b in codes) + " |")
    both = D[masks["C"] & masks["D"]]
    L += ["", f"In both C and D: {len(both)} fixtures, {int(both.over.sum())} over 2.5. Overlap is not evidence of a higher chance until it is tested out of sample."]
    # open-game: who supplied the goals
    d = D[masks["D"] & D.over]
    if len(d):
        sc = d.score.str.split("-", expand=True).astype(int)
        L += ["", f"Open-game category A games that went over 2.5: {len(d)}. Both teams scored in {int(((sc[0] > 0) & (sc[1] > 0)).sum())}; "
              f"one team scored all the goals in {int(((sc[0] == 0) | (sc[1] == 0)).sum())}."]
    L += ["", "## By run", ""]
    for rid, g in G.groupby("run_id", sort=True): L += [f"### {rid}", ""] + table(g) + [""]
    L += ["## Group fixtures with results", "", "| run | group | fixture | V4.1 | score | result | ft |", "|---|---|---|---|---|---|---|"]
    for r in G[(G.top10_rejected.fillna("") != "") | (G.open_game == "A")].sort_values(["run_id", "model_score"], ascending=[True, False]).itertuples():
        grp = " + ".join(x for x, ok in (("C" + str(r.top10_rejected), str(r.top10_rejected) not in ("", "nan")), ("D", r.open_game == "A")) if ok)
        L.append(f"| {r.run_id} | {grp} | {r.home} v {r.away} | {r.classification} {float(r.model_score):.3f} | {r.score if isinstance(r.score, str) else '-'} | "
                 f"{'over' if r.over else ('under' if r.done else 'not played')} | {r.kickoff_uk} |")
    path = f"reports/performance/research_groups_{today:%Y-%m-%d}.md"; os.makedirs("reports/performance", exist_ok=True)
    open(path, "w", encoding="utf-8").write("\n".join(L)); print("\n".join(L[:20])); print("->", path)

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "build": build(sys.argv[2], force="--force" in sys.argv)
    elif len(sys.argv) >= 2 and sys.argv[1] == "review": review()
    else: print(__doc__)
