"""
render_email.py  -  V4.1 email body for a finished run, built from the run's own CSV so the email can never drift from the report.

    python3 render_email.py <run_id>        ->  reports/<mode>/<date>/email_<date>_<mode>.html  (and prints the subject line)

Layout (Rob's rules: counts only, no averages, no percentages, green = positive, amber = middle, red = danger, no em dashes, no sign-off):
    1. one line per monitored league in Rob's order, always, even when a league has nothing above the line
    2. the shortlist: every High, Medium and Weak fixture ranked by model score, with the two drivers for both sides, the 20-count,
       BTTS lean, trump card mark, and the why / risk note
    3. postponed and flagged fixtures, competitions with no fixtures, data warnings from the manifest
    4. links to the files on GitHub
"""
import sys, os, json, html, pandas as pd
from config import ROB_ORDER

GH = "https://github.com/RobinChoppaBrooks/football-intelligence-v4/blob/main/"
GREEN, AMBER, RED, MUTED = "#1a7f37", "#b26a00", "#b42318", "#374151"

def esc(s): return html.escape("" if s is None or (isinstance(s, float) and pd.isna(s)) else str(s))

def main():
    run_id = sys.argv[1]; mode = run_id.split("_")[0]; st = run_id.split("_")[1]; date = f"{st[:4]}-{st[4:6]}-{st[6:8]}"
    outdir = f"reports/{'range' if mode == 'range' else mode}/{date}"
    C = pd.read_csv(f"{outdir}/combined_{date}.csv")
    man = json.load(open(f"reports/manifests/{run_id}.json")) if os.path.exists(f"reports/manifests/{run_id}.json") else {}
    window = man.get("fixture_window", {}).get("text", "")
    if not window:
        rv = f"reports/chatgpt_review/chatgpt_review_{date}_{mode}.md"
        if os.path.exists(rv):
            for line in open(rv, encoding="utf-8"):
                if "Analysis window:" in line: window = line.split("Analysis window:")[1].split(".")[0].strip()
    flagged = []
    for s in ("english", "european"):
        p = f"runs/{run_id}/flagged_{s}.csv"
        if os.path.exists(p):
            f = pd.read_csv(p)
            flagged += [f"{r.comp}: {r.home} v {r.away} ({r.status})" for r in f.itertuples()]
    warnings = man.get("data_quality_warnings", [])
    conf_col = {"High": GREEN, "Medium": AMBER, "Weak": AMBER, "rejected": RED}
    C["model_confidence"] = C.model_confidence.fillna("rejected")
    sel = C[C.model_confidence.isin(["High", "Medium", "Weak"])].sort_values("model_score", ascending=False)
    nH, nM, nW, nR = [(C.model_confidence == k).sum() for k in ("High", "Medium", "Weak", "rejected")]
    nT = int(C.get("trump", pd.Series(dtype=int)).fillna(0).astype(int).sum()) if "trump" in C else 0

    # 1. league lines
    L = []
    for comp in ROB_ORDER:
        g = C[C.competition == comp]
        if not len(g):
            L.append(f'<tr><td style="padding:3px 8px"><b>{esc(comp)}</b></td><td style="padding:3px 8px;color:{MUTED}">no fixtures in the window</td></tr>'); continue
        h, m, w = [(g.model_confidence == k).sum() for k in ("High", "Medium", "Weak")]
        best = g.sort_values("model_score", ascending=False).iloc[0]
        if h + m + w == 0:
            txt = f'{len(g)} analysed, <span style="color:{RED}">none above the line</span>. Best: {esc(best.fixture)} at {best.model_score:.3f}'
        else:
            txt = f'{len(g)} analysed: <span style="color:{GREEN}"><b>High {h}</b></span>, <span style="color:{AMBER}">Medium {m}</span>, Weak {w}. Top: {esc(best.fixture)} at {best.model_score:.3f}'
        L.append(f'<tr><td style="padding:3px 8px;white-space:nowrap"><b>{esc(comp)}</b></td><td style="padding:3px 8px">{txt}</td></tr>')
    league_table = '<table cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px">' + "".join(L) + "</table>"

    # 2. shortlist
    rows = []
    for r in sel.itertuples():
        home, away = r.fixture.split(" v ", 1)
        trump = bool(getattr(r, "trump", 0))
        lean = getattr(r, "btts_lean", None) or r.model_btts
        lean_col = GREEN if str(lean).startswith("YES") else (AMBER if "lean" in str(lean) else MUTED)
        d20 = getattr(r, "drivers20", None)
        rows.append(
            f'<tr><td style="padding:8px 10px;border-bottom:1px solid #e5e7eb;font-size:13px;color:{MUTED}">'
            f'<div style="font-size:14px;color:#111"><b style="color:{conf_col[r.model_confidence]}">{esc(r.model_confidence.upper())}</b> &nbsp;<b>{esc(r.fixture)}</b>'
            f'{" &nbsp;<b style=\"color:" + GREEN + "\">TRUMP CARD</b>" if trump else ""} &nbsp;<span style="color:{MUTED}">{esc(r.competition)}, {esc(r.date)} UK, score {r.model_score:.3f}</span></div>'
            f'<div>{esc(home)}: Scored 2+ <b>{r.home_scored2} of 5</b>, Let in 2+ <b>{r.home_letin2} of 5</b> &nbsp;|&nbsp; {esc(away)}: Scored 2+ <b>{r.away_scored2} of 5</b>, Let in 2+ <b>{r.away_letin2} of 5</b>'
            f'{" &nbsp;|&nbsp; drivers <b>" + str(int(d20)) + " of 20</b>" if d20 is not None and not pd.isna(d20) else ""}'
            f' &nbsp;|&nbsp; BTTS <b style="color:{lean_col}">{esc(lean)}</b> (model {esc(r.model_btts_likelihood)})</div>'
            f'<div>Last five: {esc(home)} {esc(r.home_scores)} &nbsp;|&nbsp; {esc(away)} {esc(r.away_scores)}</div>'
            f'<div>Why: {esc(r.why)}</div><div style="color:{RED}">Risk: {esc(r.risk)}</div></td></tr>')
    shortlist = '<table width="100%" cellpadding="0" cellspacing="0">' + "".join(rows) + "</table>" if rows else f'<p style="color:{MUTED}">Nothing above the line this window.</p>'

    files = [("Combined PDF", f"{outdir}/combined_{date}.pdf"), ("English PDF", f"{outdir}/english_{date}.pdf"), ("European PDF", f"{outdir}/european_{date}.pdf"),
             ("Combined CSV", f"{outdir}/combined_{date}.csv"), ("Predictions JSON", f"{outdir}/predictions_{date}.json"),
             ("ChatGPT review", f"reports/chatgpt_review/chatgpt_review_{date}_{mode}.md"), ("BTTS audit review", f"reports/chatgpt_review/btts_audit_review_{date}_{mode}.md"),
             ("Manifest", f"reports/manifests/{run_id}.json")]
    links = "".join(f'<li><a href="{GH}{p}">{n}</a></li>' for n, p in files if os.path.exists(p))
    body = f"""<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#111;max-width:780px">
<h1 style="font-size:20px;margin:0 0 6px">Football Intelligence V4.1 {esc(mode)} report</h1>
<p style="margin:0 0 4px">Window: {esc(window)}. Run {esc(run_id)}, model v4.1 (selection model unchanged). {len(C)} fixtures across {C.competition.nunique()} of the 14 leagues.</p>
<p style="margin:0 0 10px"><b>{len(sel)} above the line</b>: <span style="color:{GREEN}"><b>High {nH}</b></span>, <span style="color:{AMBER}">Medium {nM}</span>, Weak {nW}, <span style="color:{RED}">rejected {nR}</span>. Trump cards: {nT}. BTTS YES: {int((C.model_btts == "YES").sum())}.</p>
<h2 style="font-size:16px;margin:16px 0 6px;border-bottom:2px solid #111;padding-bottom:3px">By league, in order</h2>
{league_table}
<h2 style="font-size:16px;margin:20px 0 6px;border-bottom:2px solid #111;padding-bottom:3px">Shortlist, ranked by model score</h2>
<p style="margin:0 0 6px;font-size:13px;color:{MUTED}">High is model score 0.630 or more, Medium 0.581 to 0.630, Weak the bottom quarter of Medium. The two drivers are Scored 2+ and Let in 2+ over each side's last five league games. BTTS YES is the BTTS model's High band, lean YES its Medium band. A trump card (both attacks 2+ in 4 or more of 5, both defences 2+ against in 1 or fewer) is in by Rob's rule.</p>
{shortlist}
<h2 style="font-size:16px;margin:20px 0 6px;border-bottom:2px solid #111;padding-bottom:3px">Postponed, flagged, warnings</h2>
<p style="margin:4px 0;font-size:13px">{esc("; ".join(flagged)) if flagged else "No postponed or other-status fixtures in the window."}</p>
<p style="margin:4px 0;font-size:13px">{esc("; ".join(warnings)) if warnings else "No data-quality warnings."}</p>
<h2 style="font-size:16px;margin:20px 0 6px;border-bottom:2px solid #111;padding-bottom:3px">Files</h2>
<ul style="margin:4px 0 0 18px;padding:0;font-size:13px">{links}</ul>
</div>"""
    path = f"{outdir}/email_{date}_{mode}.html"
    open(path, "w", encoding="utf-8").write(body)
    first = sel.date.iloc[0] if len(sel) else ""
    print(f"Football V4.1 {mode}: {window}")
    print(path)

if __name__ == "__main__":
    main()
