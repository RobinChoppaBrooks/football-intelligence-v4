"""
btts_audit.py  -  independent BTTS assessment and contradiction flags for a completed V4 run. Version btts_audit_v1.

    python3 btts_audit.py <run_id> [--db football.db]

Reads the run's immutable inputs (runs/<run_id>/analysis_*.pkl, the committed predictions JSON, football.db, the BTTS model
cut points) and writes, without touching any existing file:

    reports/btts_audit/<date>/btts_audit_<date>_<mode>.csv       one row per fixture, every count, flag and explanation
    reports/btts_audit/<date>/btts_audit_<date>_<mode>.json      the same, machine readable
    reports/chatgpt_review/btts_audit_review_<date>_<mode>.md     the dedicated ChatGPT review output

Nothing here changes the production BTTS verdict, the Over 2.5 classifier, its thresholds or its features. The original
predictions stay exactly as published so both versions can be scored against results.

Flag tiers (validated on 2025-26, n = 15,263 league fixtures, and out of sample on 2026-27 to 28 Oct, n = 2,931):
    severe    BTTS NO while the BTTS model is in its High band. Historically 59% / 67% of these were BTTS.
    moderate  BTTS NO, model Medium, and strong card evidence (both sides BTTS in 4+ of 5, or evidence score 25+). 55% to 59% BTTS.
    mild      BTTS NO, model Medium, evidence score 23 or 24. 53% to 56% BTTS; the verdict is unsupported rather than contradicted.
    reverse   BTTS YES while the model is in its Low band. 42% BTTS on validation (n = 52), small sample.
    note      BTTS YES with one side having BTTS in 2 or fewer of 5. Informational only: 64% BTTS historically, no sign of error.
    data      an abandoned, awarded or cancelled match with a recorded score sits inside a side's last-five window.
"""
import sys, os, json, pickle, sqlite3, datetime as dt, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from btts_rules import prod_pattern, evidence_score, EV_CUT_LEAN, EV_CUT_STRONG

AUDIT_VERSION = "btts_audit_v1"
FIN = ("FT", "AET", "PEN")

def cn(rs, f): return sum(1 for x in rs if f(x))

def side_counts(rs, v):
    return dict(n=len(rs), s1=cn(rs, lambda x: x["gf"] >= 1), s2=cn(rs, lambda x: x["gf"] >= 2), c1=cn(rs, lambda x: x["ga"] >= 1), c2=cn(rs, lambda x: x["ga"] >= 2),
                btts=cn(rs, lambda x: x["gf"] > 0 and x["ga"] > 0), cs=cn(rs, lambda x: x["ga"] == 0), fts=cn(rs, lambda x: x["gf"] == 0), o25=cn(rs, lambda x: x["tot"] >= 3),
                vn=len(v), vbtts=cn(v, lambda x: x["gf"] > 0 and x["ga"] > 0), vfts=cn(v, lambda x: x["gf"] == 0), vcs=cn(v, lambda x: x["ga"] == 0),
                seq="; ".join(f"{x['gf']}-{x['ga']}" for x in rs), vseq="; ".join(f"{x['gf']}-{x['ga']}" for x in v))

def nonfinished_in_window(rs, fx_status):
    return [x["kickoff"].strftime("%d %b") for x in rs if fx_status.get(x.get("fid"), "FT") not in FIN]

def assess(row, cut_high, cut_medium):
    """Independent assessment from the model band plus the card evidence. Returns (assessment, reason)."""
    p, ev, minb = row["p_btts"], row["evidence_score"], min(row["h_btts"], row["a_btts"])
    if p >= cut_high:
        return "YES", f"BTTS model High band (p {p:.3f} at or above {cut_high:.3f}); validated 61% on 2025-26, 67% out of sample 2026-27"
    if p >= cut_medium and (ev >= EV_CUT_LEAN or minb >= 4):
        return "LEAN YES", f"BTTS model Medium band (p {p:.3f}) with supporting evidence (score {ev}, both sides BTTS at least {minb} of 5); 55% to 59% historically"
    if p < cut_medium:
        return "NO LEAN", f"BTTS model Low band (p {p:.3f} below {cut_medium:.3f}); 50% on 2025-26 but 56% out of sample, so no NO call is supportable"
    return "NO LEAN", f"BTTS model Medium band (p {p:.3f}) without strong card evidence (score {ev}); 55% historically, no lean either way"

def flag(row, cut_high, cut_medium):
    v, p, ev, minb = row["btts"], row["p_btts"], row["evidence_score"], min(row["h_btts"], row["a_btts"])
    lab = "High" if p >= cut_high else "Medium" if p >= cut_medium else "Low"
    h, a = row["home"], row["away"]
    ev_txt = (f"{h} scored in {row['h_s1']} of {row['h_n']}, conceded in {row['h_c1']} of {row['h_n']}, BTTS {row['h_btts']} of {row['h_n']}; "
              f"{a} scored in {row['a_s1']} of {row['a_n']}, conceded in {row['a_c1']} of {row['a_n']}, BTTS {row['a_btts']} of {row['a_n']}")
    if v == "NO" and lab == "High":
        return "severe", (f"Verdict NO comes from the goal pattern '{row['pattern']}', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. "
                          f"The BTTS model itself is in its High band (p {p:.3f}). {ev_txt}.")
    if v == "NO" and lab == "Medium" and (minb >= 4 or ev >= EV_CUT_STRONG):
        return "moderate", f"Verdict NO from pattern '{row['pattern']}' while the card shows both sides scoring and conceding regularly (evidence score {ev}). Model Medium (p {p:.3f}). {ev_txt}."
    if v == "NO" and lab == "Medium" and ev >= EV_CUT_LEAN:
        return "mild", f"Verdict NO from pattern '{row['pattern']}' with evidence score {ev} and model Medium (p {p:.3f}); the NO is unsupported rather than contradicted. {ev_txt}."
    if v == "YES" and lab == "Low":
        return "reverse", f"Verdict YES from pattern 'Both teams contribute' while the BTTS model is in its Low band (p {p:.3f}). {ev_txt}."
    if v == "YES" and minb <= 2:
        return "note", f"Verdict YES with one side having BTTS in only {minb} of 5; historically this group still went BTTS 64% of the time, so informational only. {ev_txt}."
    return "", ""

def main():
    run_id = sys.argv[1]; db = sys.argv[sys.argv.index("--db") + 1] if "--db" in sys.argv else "football.db"
    mode = run_id.split("_")[0]; date = f"{run_id.split('_')[1][:4]}-{run_id.split('_')[1][4:6]}-{run_id.split('_')[1][6:8]}"
    rows = []
    for s in ("english", "european"):
        p = f"runs/{run_id}/analysis_{s}.pkl"
        if os.path.exists(p): rows += pickle.load(open(p, "rb"))
    if not rows: sys.exit(f"no analysis pickles for {run_id}")
    bb = pickle.load(open("btts_model.pkl", "rb")); cut_high, cut_medium = bb["high"], bb["medium"]
    c = sqlite3.connect(db); status = dict(c.execute("select fixture_id, status from fixtures where ft_home is not null and status not in ('FT','AET','PEN')"))
    fxk = pd.read_sql("select fixture_id, kickoff_utc, home_id, away_id, season from fixtures", c)
    fxk["kickoff_utc"] = pd.to_datetime(fxk.kickoff_utc, utc=True)
    predj = f"reports/{'range' if mode == 'range' else mode}/{date}/predictions_{date}.json"
    pub = {d["fixture_id"]: d for d in json.load(open(predj))} if os.path.exists(predj) else {}
    recs = []
    for d in rows:
        pj = pub.get(d["fixture_id"], {})
        r = dict(audit_version=AUDIT_VERSION, run_id=run_id, fixture_id=d["fixture_id"], kickoff_uk=d["kickoff"], competition=d["comp"], fixture=d["fixture"], home=d["home"], away=d["away"],
                 over25_classification=pj.get("classification", {"GREEN": "High", "AMBER": "Medium", "RED": "rejected"}[d["light"]]), over25_model_score=d["p"],
                 btts=d["btts"], btts_likelihood=d["btts_lik"], p_btts=d["p_btts"], pattern=d["pattern"])
        hc, ac = side_counts(d["hr"], d["hv"]), side_counts(d["ar"], d["av"])
        for k, v in hc.items(): r[f"h_{k}"] = v
        for k, v in ac.items(): r[f"a_{k}"] = v
        recs.append(r)
    A = pd.DataFrame(recs)
    yes, pat = prod_pattern(A)
    A["rule_replicates"] = (yes == (A.btts == "YES")) & (pat == A.pattern)
    A["evidence_score"] = evidence_score(A)
    # data flags: a non-finished match with a score inside a last-five window (the card counts it, the model does not)
    fx_status = status
    data_flags = []
    for d in rows:
        bad = []
        for side, rs in (("home", d["hr"]), ("away", d["ar"])):
            # the card rows carry no fixture id, so match on kickoff and the pair of teams
            for x in rs:
                k = fxk[(fxk.kickoff_utc == x["kickoff"]) & (((fxk.home_id == x["opp"]) & (fxk.away_id != x["opp"])) | (fxk.away_id == x["opp"]))]
                k = k[(k.home_id == x["opp"]) | (k.away_id == x["opp"])]
                for fid in k.fixture_id:
                    if fid in fx_status: bad.append(f"{side} window includes {fx_status[fid]} match of {x['kickoff']:%d %b} ({x['gf']}-{x['ga']})")
        data_flags.append("; ".join(sorted(set(bad))))
    A["data_flag"] = data_flags
    out = []
    for _, r in A.iterrows():
        asmt, why = assess(r, cut_high, cut_medium)
        tier, expl = flag(r, cut_high, cut_medium)
        if r["data_flag"]:
            tier = tier or "data"; expl = (expl + " " if expl else "") + "Data: " + r["data_flag"] + "."
        status_ = {"severe": "needs review", "moderate": "needs review", "mild": "note", "reverse": "needs review", "note": "note", "data": "data check", "": "ok"}[tier]
        out.append(dict(audit_assessment=asmt, audit_reason=why, contradiction_flag=tier, contradiction_explanation=expl, review_status=status_))
    A = pd.concat([A, pd.DataFrame(out)], axis=1)
    A["agree"] = ((A.audit_assessment.isin(["YES", "LEAN YES"])) == (A.btts == "YES"))
    outdir = f"reports/btts_audit/{date}"; os.makedirs(outdir, exist_ok=True); os.makedirs("reports/chatgpt_review", exist_ok=True)
    base = f"{outdir}/btts_audit_{date}_{mode}"
    A.to_csv(base + ".csv", index=False)
    meta = dict(audit_version=AUDIT_VERSION, run_id=run_id, created_at=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), cut_high=cut_high, cut_medium=cut_medium,
                evidence_cut_lean=EV_CUT_LEAN, evidence_cut_strong=EV_CUT_STRONG, fixtures=len(A), flags=A.contradiction_flag.replace("", "none").value_counts().to_dict(),
                rule_replicates_all=bool(A.rule_replicates.all()), production_outputs_unchanged=True)
    json.dump(dict(meta=meta, fixtures=json.loads(A.to_json(orient="records"))), open(base + ".json", "w"), indent=1)
    write_review(A, meta, f"reports/chatgpt_review/btts_audit_review_{date}_{mode}.md")
    print(json.dumps(meta, indent=1))

def write_review(A, meta, path):
    L = [f"# BTTS audit review: {meta['run_id']}", "",
         f"Audit version {meta['audit_version']}, created {meta['created_at']}. Production outputs for this run are unchanged; this file is a second, independent reading of the same evidence.",
         f"Fixtures: {meta['fixtures']}. Flags: " + ", ".join(f"{k} {v}" for k, v in meta["flags"].items()) + ".", "",
         "How to read: the production BTTS verdict is a hand rule (YES exactly when the goal pattern is 'Both teams contribute', which needs an Over 2.5 route for each side).",
         "The audit assessment uses the trained BTTS model band plus the card counts. Neither is overridden; both are listed so each can be scored against the result.",
         f"Model bands: High p >= {meta['cut_high']:.3f}, Medium p >= {meta['cut_medium']:.3f}. Evidence score 0 to 30 = each side's scored-in + conceded-in + BTTS counts of 5, with venue adjustments.", ""]
    order = {"severe": 0, "moderate": 1, "reverse": 2, "mild": 3, "note": 4, "data": 5, "": 6}
    for tier in ("severe", "moderate", "reverse", "mild", "note", "data"):
        g = A[A.contradiction_flag == tier]
        if not len(g): continue
        L += [f"## {tier.title()} ({len(g)})", ""]
        for r in g.sort_values(["competition", "kickoff_uk"]).itertuples():
            L += [f"### {r.fixture}  ({r.competition}, {r.kickoff_uk} UK)  fixture_id {r.fixture_id}",
                  f"- Over 2.5: {r.over25_classification} (model score {r.over25_model_score}). Production BTTS: {r.btts} ({r.btts_likelihood}, p {r.p_btts:.3f}). Pattern: {r.pattern}.",
                  f"- Audit assessment: {r.audit_assessment}. {r.audit_reason}.",
                  f"- {r.home}: scored in {r.h_s1}/{r.h_n}, 2+ in {r.h_s2}/{r.h_n}, conceded in {r.h_c1}/{r.h_n}, 2+ against in {r.h_c2}/{r.h_n}, BTTS {r.h_btts}/{r.h_n}, clean sheets {r.h_cs}/{r.h_n}, failed to score {r.h_fts}/{r.h_n}. Last five: {r.h_seq}. Home last {r.h_vn}: {r.h_vseq} (BTTS {r.h_vbtts}/{r.h_vn}).",
                  f"- {r.away}: scored in {r.a_s1}/{r.a_n}, 2+ in {r.a_s2}/{r.a_n}, conceded in {r.a_c1}/{r.a_n}, 2+ against in {r.a_c2}/{r.a_n}, BTTS {r.a_btts}/{r.a_n}, clean sheets {r.a_cs}/{r.a_n}, failed to score {r.a_fts}/{r.a_n}. Last five: {r.a_seq}. Away last {r.a_vn}: {r.a_vseq} (BTTS {r.a_vbtts}/{r.a_vn}).",
                  f"- Evidence score: {r.evidence_score}. Flag: {r.contradiction_flag}. Review status: {r.review_status}.",
                  f"- Why flagged: {r.contradiction_explanation}", ""]
    L += ["## All fixtures", "", "| fixture_id | kickoff UK | competition | fixture | Over 2.5 | BTTS (prod) | p | audit | evidence | flag | status |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in A.sort_values(["competition", "kickoff_uk"]).itertuples():
        L.append(f"| {r.fixture_id} | {r.kickoff_uk} | {r.competition} | {r.fixture} | {r.over25_classification} | {r.btts} ({r.btts_likelihood}) | {r.p_btts:.3f} | {r.audit_assessment} | {r.evidence_score} | {r.contradiction_flag or '-'} | {r.review_status} |")
    open(path, "w", encoding="utf-8").write("\n".join(L))

if __name__ == "__main__":
    main()
