"""
run_v4.py  -  Football Intelligence V4 orchestrator (production). The validated model is untouched: this script only builds
fixture lists, calls analyse_fixtures.py and report_v4.py, and writes the three reports, exports, review package and logs.

    python3 run_v4.py midweek            Monday..Thursday of the current week (fixtures not yet kicked off)
    python3 run_v4.py weekend            Friday..Sunday of the coming weekend
    python3 run_v4.py range 2026-11-03 2026-11-05 [--sets english|european|both]
    python3 run_v4.py review             fill results for played predictions, write the performance report
    python3 run_v4.py status             list schedules and last executions
    python3 run_v4.py export-review RUNID   rebuild the ChatGPT review file for a run

Assumes football.db is current (Rob's PC: py download.py --results). Bookmaker odds are never used for selection.
"""
import os, sys, json, pickle, sqlite3, subprocess, datetime as dt, uuid, math
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
from config import LEAGUES, CUPS, NONLEAGUE, ORDER
ALL = {**LEAGUES, **CUPS, **NONLEAGUE}; BYID = {v[0]: k for k, v in ALL.items()}
COMP = json.load(open("config/competitions.json"))
SETS = {"english": [c["name"] for c in COMP["english"]], "european": [c["name"] for c in COMP["european"]]}
LOGP = "data/predictions/predictions_log.csv"; RESP = "data/results/results_log.csv"; EXEC = "logs/execution/executions.csv"
MODEL_VERSION = "v4.1"
LONDON = "Europe/London"

def now_l(): return pd.Timestamp.now(tz=LONDON)
def log_exec(run_id, mode, status, start, msg=""):
    row = dict(run_id=run_id, mode=mode, status=status, start=start.strftime("%Y-%m-%d %H:%M:%S"), finish=now_l().strftime("%Y-%m-%d %H:%M:%S"), message=msg)
    df = pd.DataFrame([row]); df.to_csv(EXEC, mode="a", header=not os.path.exists(EXEC), index=False)

def window_for(mode, today=None):
    t = (today or now_l()).normalize()
    if mode == "midweek":
        mon = t - pd.Timedelta(days=t.weekday()); return max(now_l(), mon), mon + pd.Timedelta(days=4)            # Mon..Thu (end exclusive = Fri 00:00)
    if mode == "weekend":
        fri = t + pd.Timedelta(days=(4 - t.weekday()) % 7); return fri, fri + pd.Timedelta(days=3)                 # Fri..Sun
    raise ValueError(mode)

def build_lists(start, end, sets, run_id):
    c = sqlite3.connect("football.db"); teams = dict(pd.read_sql("select team_id,name from teams", c).values)
    s_utc, e_utc = pd.Timestamp(start).tz_convert("UTC").isoformat(), pd.Timestamp(end).tz_convert("UTC").isoformat()
    fx = pd.read_sql("select * from fixtures where kickoff_utc>=? and kickoff_utc<? and season=2026", c, params=(s_utc, e_utc))
    fx["comp"] = fx.league_id.map(BYID); fx = fx[fx.comp.notna()]
    out = {}
    for s in sets:
        g = fx[fx.comp.isin(SETS[s])]
        flagged = g[g.status != "NS"].assign(home=lambda d: d.home_id.map(teams), away=lambda d: d.away_id.map(teams))[["comp", "kickoff_utc", "home", "away", "status"]]
        ns = g[g.status == "NS"].assign(home=lambda d: d.home_id.map(teams), away=lambda d: d.away_id.map(teams), o=lambda d: d.comp.map(ORDER.index)).sort_values(["o", "kickoff_utc", "home"])
        path = f"runs/{run_id}/fixtures_{s}.txt"; os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for comp, gg in ns.groupby("comp", sort=False):
                f.write(comp + "\n"); [f.write(f"{r.home} v {r.away}\n") for r in gg.itertuples()]; f.write("\n")
        flagged.to_csv(f"runs/{run_id}/flagged_{s}.csv", index=False)
        nofix = [n for n in SETS[s] if n not in set(ns.comp)]
        out[s] = dict(list=path, n=len(ns), flagged=f"runs/{run_id}/flagged_{s}.csv", nflag=len(flagged), nofix=nofix)
    return out

def analyse(listpath, outbase):
    if os.path.getsize(listpath) == 0: return None
    r = subprocess.run([sys.executable, "analyse_fixtures.py", "football.db", listpath, "--out", outbase], capture_output=True, text=True)
    if not os.path.exists(outbase + ".pkl"): raise RuntimeError("analysis failed: " + r.stderr[-800:])
    return outbase + ".pkl"

def render(pkl, pdf, csv, window, flagged, nofix):
    r = subprocess.run([sys.executable, "report_v4.py", pkl, "football.db", pdf, csv, window, "--flagged", flagged, "--nofix", ", ".join(nofix)], capture_output=True, text=True)
    if not os.path.exists(pdf): raise RuntimeError("report failed: " + r.stderr[-800:])

def chatgpt_review(rows, run_id, label, window, path, flagged_notes):
    n_ = lambda rs, f: sum(1 for x in rs if f(x))
    sel = [d for d in rows if d["light"] != "RED"]
    L = [f"# ChatGPT review package: {label}", "", f"Report date: {now_l():%Y-%m-%d %H:%M} UK. Analysis window: {window}. Model version: {MODEL_VERSION} (validated model, unchanged). Run id: {run_id}.",
         f"Fixtures analysed: {len(rows)}. Selected: {len(sel)} (High {sum(d['light']=='GREEN' for d in rows)}, Medium/Weak {sum(d['light']=='AMBER' for d in rows)}). Rejected: {len(rows)-len(sel)}.",
         "", "Classifications are model bands, not per-fixture probabilities (Rob's 14 leagues, out of sample 2026-27: High 65%, Medium 63%, rejected 50%). Counts are from stored final scores; the five results are listed oldest to newest. BTTS YES = BTTS model High band (67% out of sample); lean YES = Medium band; no lean = Low band. A trump card fixture (both attacks 2+ in 4+ of 5, both defences 2+ against in 1 or fewer) is High and BTTS YES by Rob's rule and is scored separately.",
         "", "Data-quality warnings: " + ("; ".join(flagged_notes) if flagged_notes else "none"), ""]
    for d in sorted(sel, key=lambda d: (d["light"] != "GREEN", d["comp"], d["kickoff"])):
        hr, ar, hv, av = d["hr"], d["ar"], d.get("hv5", d["hv"]), d.get("av5", d["av"])
        conf = "High" if d["light"] == "GREEN" else "Medium"
        L += [f"## {d['fixture']}  ({d['comp']}, {d['kickoff']} UK)  fixture_id {d['fixture_id']}",
              f"- Classification: {conf}{' (trump card)' if d.get('trump') else ''}. Over 2.5: YES. BTTS: {d.get('btts_lean', d['btts'])} (model {d['btts_lik']}){'; caution: ' + d['btts_note'] if d.get('btts_note') else ''}. Drivers: {d.get('drivers20')} of 20. Pattern: {d['pattern']}.",
              f"- {d['home']}: scored 2+ {n_(hr, lambda x: x['gf']>=2)}/{len(hr)}, let in 2+ {n_(hr, lambda x: x['ga']>=2)}/{len(hr)}, 3+ in {n_(hr, lambda x: x['tot']>=3)}/{len(hr)}, BTTS {n_(hr, lambda x: x['gf']>0 and x['ga']>0)}/{len(hr)}, clean sheets {n_(hr, lambda x: x['ga']==0)}/{len(hr)}, failed to score {n_(hr, lambda x: x['gf']==0)}/{len(hr)}. Last five: " + ", ".join(f"{x['gf']}-{x['ga']}" for x in hr) + f". Home last {len(hv)}: " + ", ".join(f"{x['gf']}-{x['ga']}" for x in hv),
              f"- {d['away']}: scored 2+ {n_(ar, lambda x: x['gf']>=2)}/{len(ar)}, let in 2+ {n_(ar, lambda x: x['ga']>=2)}/{len(ar)}, 3+ in {n_(ar, lambda x: x['tot']>=3)}/{len(ar)}, BTTS {n_(ar, lambda x: x['gf']>0 and x['ga']>0)}/{len(ar)}, clean sheets {n_(ar, lambda x: x['ga']==0)}/{len(ar)}, failed to score {n_(ar, lambda x: x['gf']==0)}/{len(ar)}. Last five: " + ", ".join(f"{x['gf']}-{x['ga']}" for x in ar) + f". Away last {len(av)}: " + ", ".join(f"{x['gf']}-{x['ga']}" for x in av),
              f"- Supporting: {d['why']}", f"- Concern: {d['risk']}", f"- Notes: {'; '.join(e for e in d['ev_against'] if 'average' not in e) or 'none'}", ""]
    L += ["## Rejected fixtures (model below the line)", ""] + [f"- {d['fixture']} ({d['comp']}, {d['kickoff']}) fixture_id {d['fixture_id']}" for d in rows if d["light"] == "RED"]
    open(path, "w", encoding="utf-8").write("\n".join(L))

def run_analysis(mode, start=None, end=None, sets=("english", "european")):
    t0 = now_l(); run_id = f"{mode}_{t0:%Y%m%d_%H%M}"
    if mode in ("midweek", "weekend"): start, end = window_for(mode)
    else: start, end = pd.Timestamp(start, tz=LONDON), pd.Timestamp(end, tz=LONDON) + pd.Timedelta(days=1)
    window = f"{start:%a %d %b %Y} to {(end - pd.Timedelta(seconds=1)):%a %d %b %Y}"
    outdir = f"reports/{'range' if mode == 'range' else mode}/{t0:%Y-%m-%d}"; os.makedirs(outdir, exist_ok=True)
    try:
        lists = build_lists(start, end, sets, run_id); allrows = []; summary = {}
        for s in sets:
            info = lists[s]
            if info["n"] == 0: summary[s] = "no fixtures"; continue
            pkl = analyse(info["list"], f"runs/{run_id}/analysis_{s}")
            rows = pickle.load(open(pkl, "rb")); allrows += rows
            render(pkl, f"{outdir}/{s}_{t0:%Y-%m-%d}.pdf", f"{outdir}/{s}_{t0:%Y-%m-%d}.csv", f"{window} ({s})", info["flagged"], info["nofix"])
            summary[s] = f"{len(rows)} analysed, {sum(d['light']!='RED' for d in rows)} selected, {info['nflag']} flagged"
        # combined: all selected, grouped by date then league, original classifications
        comb = [d for d in allrows if d["light"] != "RED"]
        pickle.dump(allrows, open(f"runs/{run_id}/analysis_combined.pkl", "wb"))
        render(f"runs/{run_id}/analysis_combined.pkl", f"{outdir}/combined_{t0:%Y-%m-%d}.pdf", f"{outdir}/combined_{t0:%Y-%m-%d}.csv", f"{window} (combined)", lists[sets[0]]["flagged"], [])
        # JSON export for review
        n_ = lambda rs, f: sum(1 for x in rs if f(x))
        js = [dict(run_id=run_id, fixture_id=d["fixture_id"], competition=d["comp"], league_id=ALL[d["comp"]][0], kickoff_uk=d["kickoff"], home=d["home"], away=d["away"],
                   model_version=MODEL_VERSION, classification=("High" if d["light"] == "GREEN" else "Medium" if d["light"] == "AMBER" else "rejected"), over25=("Yes" if d["light"] != "RED" else "No"),
                   btts=d["btts"], btts_likelihood=d["btts_lik"], btts_lean=d.get("btts_lean"), btts_note=d.get("btts_note", ""), trump=bool(d.get("trump", False)), drivers20=d.get("drivers20"), pattern=d["pattern"], model_score=d["p"],
                   home_scored2=n_(d["hr"], lambda x: x["gf"] >= 2), home_letin2=n_(d["hr"], lambda x: x["ga"] >= 2), away_scored2=n_(d["ar"], lambda x: x["gf"] >= 2), away_letin2=n_(d["ar"], lambda x: x["ga"] >= 2),
                   home_last5=[f"{x['gf']}-{x['ga']}" for x in d["hr"]], away_last5=[f"{x['gf']}-{x['ga']}" for x in d["ar"]], why=d["why"], risk=d["risk"]) for d in allrows]
        json.dump(js, open(f"{outdir}/predictions_{t0:%Y-%m-%d}.json", "w"), indent=1)
        notes = []
        for s in sets:
            if lists[s]["nflag"]: notes.append(f"{lists[s]['nflag']} {s} fixtures postponed/other status, not analysed (see flagged_{s}.csv)")
            if lists[s]["nofix"]: notes.append(f"{s} competitions with no fixtures: " + ", ".join(lists[s]["nofix"]))
        thin = [d["fixture"] for d in allrows if len(d["hr"]) < 5 or len(d["ar"]) < 5]
        if thin: notes.append(f"{len(thin)} fixtures with fewer than five league games for a side")
        chatgpt_review(allrows, run_id, f"{mode} {t0:%Y-%m-%d}", window, f"reports/chatgpt_review/chatgpt_review_{t0:%Y-%m-%d}_{mode}.md", notes)
        # prediction database: append snapshot rows tagged with run_id, never edit earlier rows
        _db_append(allrows, run_id)
        log_exec(run_id, mode, "ok", t0, json.dumps(summary))
        print(json.dumps(dict(run_id=run_id, window=window, outdir=outdir, summary=summary, combined_selected=len(comb)), indent=1))
    except Exception as e:
        log_exec(run_id, mode, "error", t0, str(e)[:500]); raise

def _db_append(rows, run_id):
    n_ = lambda rs, f: sum(1 for x in rs if f(x))
    recs = [dict(run_id=run_id, generated_at=now_l().strftime("%Y-%m-%d %H:%M"), model_version=MODEL_VERSION, fixture_id=d["fixture_id"], league_id=ALL[d["comp"]][0], competition=d["comp"],
                 kickoff_uk=d["kickoff"], home=d["home"], away=d["away"], classification=("High" if d["light"] == "GREEN" else "Medium" if d["light"] == "AMBER" else "rejected"),
                 over25=("Yes" if d["light"] != "RED" else "No"), btts=d["btts"], btts_likelihood=d["btts_lik"], btts_lean=d.get("btts_lean"), btts_note=d.get("btts_note", ""), trump=int(bool(d.get("trump", False))), drivers20=d.get("drivers20"), model_score=d["p"], p_btts=d["p_btts"], pattern=d["pattern"],
                 h_s2=n_(d["hr"], lambda x: x["gf"] >= 2), h_c2=n_(d["hr"], lambda x: x["ga"] >= 2), a_s2=n_(d["ar"], lambda x: x["gf"] >= 2), a_c2=n_(d["ar"], lambda x: x["ga"] >= 2),
                 h_over=n_(d["hr"], lambda x: x["tot"] >= 3), a_over=n_(d["ar"], lambda x: x["tot"] >= 3), h_btts=n_(d["hr"], lambda x: x["gf"] > 0 and x["ga"] > 0), a_btts=n_(d["ar"], lambda x: x["gf"] > 0 and x["ga"] > 0),
                 h_cs=n_(d["hr"], lambda x: x["ga"] == 0), a_cs=n_(d["ar"], lambda x: x["ga"] == 0), h_fts=n_(d["hr"], lambda x: x["gf"] == 0), a_fts=n_(d["ar"], lambda x: x["gf"] == 0), h_n=len(d["hr"]), a_n=len(d["ar"]),
                 home_last5="; ".join(f"{x['gf']}-{x['ga']}" for x in d["hr"]), away_last5="; ".join(f"{x['gf']}-{x['ga']}" for x in d["ar"]), why=d["why"], risk=d["risk"], notes="; ".join(d["ev_against"]),
                 published=1) for d in rows]
    df = pd.DataFrame(recs)
    if os.path.exists(LOGP):
        old = pd.read_csv(LOGP, dtype=str)
        # a fixture analysed again in a later run keeps its earlier rows; the first published snapshot stays published=1, later ones are marked 0
        seen = set(old.fixture_id.astype(str)); df["published"] = [0 if str(f) in seen else 1 for f in df.fixture_id]
        df = pd.concat([old, df.astype(str)])
    df.to_csv(LOGP, index=False)

def review():
    t0 = now_l(); run_id = f"review_{t0:%Y%m%d_%H%M}"
    c = sqlite3.connect("football.db"); fx = pd.read_sql("select fixture_id,status,ft_home,ft_away from fixtures", c).set_index("fixture_id")
    played = fx[fx.status.isin(["FT", "AET", "PEN"])]
    log = pd.read_csv(LOGP, dtype=str); res = pd.read_csv(RESP, dtype=str) if os.path.exists(RESP) else pd.DataFrame(columns=["run_id", "fixture_id"])
    done = set(zip(res.run_id, res.fixture_id)) if len(res) else set()
    new = []
    for r in log.itertuples():
        fid = int(r.fixture_id)
        if (r.run_id, r.fixture_id) in done or fid not in played.index: continue
        h, a = int(played.ft_home[fid]), int(played.ft_away[fid]); tot = h + a
        new.append(dict(run_id=r.run_id, fixture_id=r.fixture_id, score=f"{h}-{a}", total_goals=tot, over25_result=("Y" if tot >= 3 else "N"), btts_result=("Y" if h > 0 and a > 0 else "N"),
                        over25_correct=int((tot >= 3) == (r.over25 == "Yes")), btts_correct=int(((h > 0 and a > 0) == (r.btts == "YES"))), verified_at=t0.strftime("%Y-%m-%d %H:%M")))
    if new: res = pd.concat([res, pd.DataFrame(new).astype(str)]); res.to_csv(RESP, index=False)
    m = log.merge(res, on=["run_id", "fixture_id"]); m = m[m.published == "1"]
    m["o"] = (m.over25_result == "Y").astype(int); m["b"] = (m.btts_result == "Y").astype(int); m["bc"] = m.btts_correct.astype(int)
    for col in ("h_s2", "a_s2", "h_c2", "a_c2"): m[col] = m[col].astype(int)
    def w(k, n):
        if n == 0: return "-"
        p = k / n; z = 1.96; d = 1 + z * z / n; cc = p + z * z / (2 * n); s = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return f"{(cc - s) / d * 100:.0f} to {(cc + s) / d * 100:.0f}%"
    def line(lab, g): k = int(g.o.sum()); n = len(g); return f"| {lab} | {k} of {n} | {k / n * 100:.0f}% | {w(k, n)} |" if n else f"| {lab} | 0 | - | - |"
    sel = m[m.over25 == "Yes"]; L = [f"# Performance report {t0:%Y-%m-%d}", "", f"Predictions with results: {len(m)} of {len(log[log.published == '1'])} published. New results added this run: {len(new)}.", "",
                                     "Benchmarks (out of sample): High 69%, selected 64%, rejected 54%; BTTS High 61%, Medium 55%, Low 50%.", "", "| | hit 3+ | rate | 95% range |", "|---|---|---|---|",
                                     line("Selected (all)", sel), line("High", m[m.classification == "High"]), line("Medium", m[m.classification == "Medium"]), line("Rejected", m[m.classification == "rejected"])]
    L += ["", f"BTTS: YES predictions correct {int(m[m.btts == 'YES'].bc.sum())} of {int((m.btts == 'YES').sum())}; NO predictions correct {int(m[m.btts == 'NO'].bc.sum())} of {int((m.btts == 'NO').sum())}.", "", "## By competition (selected)", "", "| competition | hit | n | rate |", "|---|---|---|---|"]
    for cp, g in sel.groupby("competition"): L.append(f"| {cp} | {int(g.o.sum())} | {len(g)} | {g.o.mean() * 100:.0f}% |")
    both = sel[(sel.h_s2 >= 3) & (sel.a_s2 >= 3)]; one = sel[((sel.h_s2 >= 3) | (sel.a_s2 >= 3)) & ~((sel.h_s2 >= 3) & (sel.a_s2 >= 3))]; nei = sel[(sel.h_s2 < 3) & (sel.a_s2 < 3)]
    L += ["", "## Patterns (selected)", "", "| | hit 3+ | rate | 95% range |", "|---|---|---|---|", line("both attacks 3 of 5+", both), line("one attack 3 of 5+", one), line("neither", nei)]
    for lab, col in (("home scored 2+", "h_s2"), ("away scored 2+", "a_s2"), ("home let in 2+", "h_c2"), ("away let in 2+", "a_c2")):
        L += ["", f"By {lab}:", ""] + [line(f"  {v} of 5", sel[sel[col] == v]) for v in range(6)]
    L += ["", "## Over time (selected, by run)", "", "| run | hit | n |", "|---|---|---|"] + [f"| {rid} | {int(g.o.sum())} | {len(g)} |" for rid, g in sel.groupby("run_id")]
    L += ["", "## Outstanding (published, no result yet)", ""] + [f"- {r.fixture} ({r.competition}, {r.kickoff_uk}) fixture_id {r.fixture_id}" if "fixture" in log.columns else f"- {r.home} v {r.away} ({r.competition}, {r.kickoff_uk}) fixture_id {r.fixture_id}" for r in log[(log.published == "1") & ~log.set_index(["run_id", "fixture_id"]).index.isin(list(zip(res.run_id, res.fixture_id)))].itertuples()][:60]
    path = f"reports/performance/performance_{t0:%Y-%m-%d}.md"; open(path, "w", encoding="utf-8").write("\n".join(L))
    log_exec(run_id, "review", "ok", t0, f"{len(new)} results added"); print("\n".join(L[:14])); print("->", path)

def status():
    print(json.dumps(json.load(open("config/schedules.json")), indent=1))
    if os.path.exists(EXEC): print(pd.read_csv(EXEC).tail(10).to_string(index=False))

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode in ("midweek", "weekend"): run_analysis(mode)
    elif mode == "range":
        sets = ("english", "european")
        if "--sets" in sys.argv:
            v = sys.argv[sys.argv.index("--sets") + 1]; sets = ("english", "european") if v == "both" else (v,)
        run_analysis("range", sys.argv[2], sys.argv[3], sets)
    elif mode == "review": review()
    elif mode == "status": status()
    else: print(__doc__)
