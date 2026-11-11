"""
render_email.py  -  V4.2 email body for a finished run, built from the run's own CSV so the email can never drift from the report.

    python3 render_email.py <run_id>        ->  reports/<mode>/<date>/email_<date>_<mode>.html  (and prints the subject line)

Layout (Rob's rules: counts only, no averages, no percentages, green = positive, amber = middle, red = danger, no em dashes, no sign-off):
    1. one line per monitored league in Rob's order, always, even when a league has nothing above the line
    2. the shortlist: every High, Medium and Weak fixture ranked by model score, with the two drivers for both sides, the 20-count,
       each side's scoring counts (V4.2: no BTTS model), trump card mark, and the why / risk note
    3. research sections (added 2 Nov 2026; never selections, classifications unchanged), from reports/research_groups/<run_id>.csv:
       top 10 rejected fixtures to watch, the EXPERIMENTAL open-game watchlist (category A), and the complete ranking of every
       eligible fixture by model score
    4. postponed and flagged fixtures, competitions with no fixtures, data warnings from the manifest
    5. links to the files on GitHub
"""
import sys, os, json, html, pickle, pandas as pd
from config import ROB_ORDER
CUTS = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bands_model.pkl"), "rb"))   # the stored 3-decimal cut points
VER = CUTS.get("model_version", "v4.1").upper()

GH = "https://github.com/RobinChoppaBrooks/football-intelligence-v4/blob/main/"
GREEN, AMBER, RED, MUTED = "#1a7f37", "#b26a00", "#b42318", "#374151"

def esc(s): return html.escape("" if s is None or (isinstance(s, float) and pd.isna(s)) else str(s))

H2 = '<h2 style="font-size:16px;margin:20px 0 6px;border-bottom:2px solid #111;padding-bottom:3px">'
NOTE = f'<p style="margin:0 0 6px;font-size:13px;color:{MUTED}">'

def _i(v):
    try: return int(float(v))
    except Exception: return None

def research_sections(run_id, C):
    """Top 10 rejected, open-game watchlist and the complete ranking. Read-only: every label and score is the run's own."""
    p = f"reports/research_groups/{run_id}.csv"
    if not os.path.exists(p):
        return H2 + "Research sections</h2>" + NOTE + "No research groups file for this run (reports/research_groups/), so the watchlists are not shown.</p>"
    G = pd.read_csv(p, dtype={"fixture_id": str, "top10_rejected": str, "open_game": str}).fillna("")
    G["model_score"] = G.model_score.astype(float)
    lab = {r.fixture_id: (r.report_label or r.classification) for r in G.itertuples()}
    col = {"High": GREEN, "Medium": AMBER, "Weak": AMBER, "rejected": RED}
    out = []
    # top 10 rejected
    T = G[G.top10_rejected != ""].copy(); T["k"] = T.top10_rejected.astype(int); T = T.sort_values("k")
    rows = []
    for r in T.itertuples():
        gap = CUTS["amber"] - r.model_score
        why = f"Score {r.model_score:.3f}, {gap:.3f} below the selection line; rank {r.rank_all} of {len(G)} fixtures overall."
        if r.rejection_reason: why += f" Rejected because: {esc(r.rejection_reason)}."
        rows.append(f'<tr><td style="padding:6px 10px;border-bottom:1px solid #e5e7eb;font-size:13px;color:{MUTED}"><div style="font-size:14px;color:#111"><b>{r.k}.</b> <b>{esc(r.home)} v {esc(r.away)}</b> '
                    f'&nbsp;<span style="color:{MUTED}">{esc(r.competition)}, {esc(r.kickoff_uk)} UK</span> &nbsp;<b style="color:{RED}">REJECTED</b> {r.model_score:.3f}'
                    f'{" &nbsp;<b>open-game " + esc(r.open_game) + "</b>" if r.open_game else ""}</div>'
                    f'<div>{esc(r.home)}: Scored 2+ <b>{_i(r.h_s2)} of 5</b>, Let in 2+ <b>{_i(r.h_c2)} of 5</b>, clean sheets {_i(r.h_cs)}, failed to score {_i(r.h_fts)} &nbsp;|&nbsp; '
                    f'{esc(r.away)}: Scored 2+ <b>{_i(r.a_s2)} of 5</b>, Let in 2+ <b>{_i(r.a_c2)} of 5</b>, clean sheets {_i(r.a_cs)}, failed to score {_i(r.a_fts)}</div>'
                    f'<div>Last five: {esc(r.home)} {esc(r.home_scores)} &nbsp;|&nbsp; {esc(r.away)} {esc(r.away_scores)}</div><div>{why}</div></td></tr>')
    out.append(H2 + f"Top 10 rejected fixtures to watch</h2>" + NOTE + f"The highest {VER} model scores among fixtures {VER} rejected, nothing else applied. Research candidates, not selections; "
               "their classification stays rejected.</p>" + ('<table width="100%" cellpadding="0" cellspacing="0">' + "".join(rows) + "</table>" if rows else NOTE + "No rejected fixtures in this run.</p>"))
    # open-game watchlist
    A = G[G.open_game == "A"].sort_values("model_score", ascending=False); rows = []
    for r in A.itertuples():
        try: d = json.loads(r.open_game_detail)
        except Exception: d = {}
        h5, a5 = d.get("home5", {}), d.get("away5", {})
        def side(name, s, flags, shut, pers):
            return (f'{esc(name)}: scored in <b>{s.get("scored")} of 5</b>, conceded in <b>{s.get("conceded")} of 5</b>, conceded 2+ in <b>{s.get("conceded2")}</b>, clean sheets {s.get("cs")}; '
                    f'second-half goals {s.get("sh_gf")} for, {s.get("sh_ga")} against; after 75\' {s.get("g75_gf")} for, {s.get("g75_ga")} against'
                    f'{"; weakness holds over ten games" if pers else ""}')
        gaps = []
        for name, s in ((r.home, h5), (r.away, a5)):
            if s.get("scored", 5) <= 2: gaps.append(f"{name} scored in only {s.get('scored')} of 5")
            if s.get("scored2", 0) == 0: gaps.append(f"{name} scored 2+ in none of 5")
            if s.get("conceded2", 0) <= 1: gaps.append(f"{name} conceded 2+ only {s.get('conceded2')} time(s)")
        rows.append(f'<tr><td style="padding:6px 10px;border-bottom:1px solid #e5e7eb;font-size:13px;color:{MUTED}"><div style="font-size:14px;color:#111"><b>{esc(r.home)} v {esc(r.away)}</b> '
                    f'&nbsp;<span style="color:{MUTED}">{esc(r.competition)}, {esc(r.kickoff_uk)} UK</span> &nbsp;{VER} <b style="color:{col.get(lab.get(r.fixture_id), MUTED)}">{esc(lab.get(r.fixture_id, "").upper())}</b> {r.model_score:.3f} &nbsp;open-game <b>A</b></div>'
                    f'<div>{side(r.home, h5, d.get("flags_home"), d.get("shuts_home"), d.get("persistent_home"))}</div>'
                    f'<div>{side(r.away, a5, d.get("flags_away"), d.get("shuts_away"), d.get("persistent_away"))}</div>'
                    f'<div style="color:{RED}">Weaknesses: {esc("; ".join(gaps) if gaps else "none flagged by the counts")}</div></td></tr>')
    labelled = int((G.open_game != "").sum())
    out.append(H2 + "EXPERIMENTAL: open-game watchlist</h2>" + NOTE + f"Category A of the 2 Nov open-game filter (both sides concede often, both contribute goals, their games stay open after the break). "
               f"Not validated: on 639 earlier fixtures A went 130 of 208 over 2.5 and B 138 of 225, and the filter has not shown value beyond the model score. Never a selection. "
               f"{labelled} of {len(G)} fixtures had enough goal-event data to be labelled.</p>" + ('<table width="100%" cellpadding="0" cellspacing="0">' + "".join(rows) + "</table>" if rows else NOTE + "No category A fixtures in this run.</p>"))
    # complete ranking
    rows = []
    for r in G.sort_values("rank_all").itertuples():
        l = lab.get(r.fixture_id, r.classification)
        tags = " ".join(x for x in (f"top-10 rejected #{r.top10_rejected}" if r.top10_rejected else "", f"open-game {r.open_game}" if r.open_game else "") if x)
        rows.append(f'<tr><td style="padding:2px 6px">{r.rank_all}</td><td style="padding:2px 6px">{r.model_score:.3f}</td><td style="padding:2px 6px;color:{col.get(l, MUTED)}"><b>{esc(l)}</b></td>'
                    f'<td style="padding:2px 6px">{esc(r.home)} v {esc(r.away)}</td><td style="padding:2px 6px;color:{MUTED}">{esc(r.competition)}, {esc(r.kickoff_uk)}</td><td style="padding:2px 6px;color:{MUTED}">{esc(tags)}</td></tr>')
    out.append(H2 + f"Complete eligible fixture rankings ({len(G)})</h2>" + NOTE + f"Every fixture the run analysed, by {VER} model score, with its official label. Same run, same scores as above.</p>"
               '<table cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:12px"><tr style="color:#111"><td style="padding:2px 6px"><b>#</b></td><td style="padding:2px 6px"><b>score</b></td>'
               f'<td style="padding:2px 6px"><b>{VER}</b></td><td style="padding:2px 6px"><b>fixture</b></td><td style="padding:2px 6px"><b>league, UK kick-off</b></td><td style="padding:2px 6px"><b>research tags</b></td></tr>' + "".join(rows) + "</table>")
    return "\n".join(out)

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
        scoring = getattr(r, "scoring", "")
        whale = getattr(r, "whale_side", "")
        whale = "" if whale is None or (isinstance(whale, float) and pd.isna(whale)) else str(whale)
        d20 = getattr(r, "drivers20", None)
        rows.append(
            f'<tr><td style="padding:8px 10px;border-bottom:1px solid #e5e7eb;font-size:13px;color:{MUTED}">'
            f'<div style="font-size:14px;color:#111"><b style="color:{conf_col[r.model_confidence]}">{esc(r.model_confidence.upper())}</b> &nbsp;<b>{esc(r.fixture)}</b>'
            f'{" &nbsp;<b style=\"color:" + GREEN + "\">TRUMP CARD (" + esc(whale) + ")</b>" if trump else ""} &nbsp;<span style="color:{MUTED}">{esc(r.competition)}, {esc(r.date)} UK, score {r.model_score:.3f}</span></div>'
            f'<div>{esc(home)}: Scored 2+ <b>{r.home_scored2} of 5</b>, Let in 2+ <b>{r.home_letin2} of 5</b> &nbsp;|&nbsp; {esc(away)}: Scored 2+ <b>{r.away_scored2} of 5</b>, Let in 2+ <b>{r.away_letin2} of 5</b>'
            f'{" &nbsp;|&nbsp; drivers <b>" + str(int(d20)) + " of 20</b>" if d20 is not None and not pd.isna(d20) else ""}'
            f'</div><div>Scoring: {esc(scoring)}</div>'
            f'<div>Last five: {esc(home)} {esc(r.home_scores)} &nbsp;|&nbsp; {esc(away)} {esc(r.away_scores)}</div>'
            f'<div>Why: {esc(r.why)}</div><div style="color:{RED}">Risk: {esc(r.risk)}</div></td></tr>')
    shortlist = '<table width="100%" cellpadding="0" cellspacing="0">' + "".join(rows) + "</table>" if rows else f'<p style="color:{MUTED}">Nothing above the line this window.</p>'

    research = research_sections(run_id, C)

    files = [("Combined PDF", f"{outdir}/combined_{date}.pdf"), ("English PDF", f"{outdir}/english_{date}.pdf"), ("European PDF", f"{outdir}/european_{date}.pdf"),
             ("Combined CSV", f"{outdir}/combined_{date}.csv"), ("Predictions JSON", f"{outdir}/predictions_{date}.json"),
             ("ChatGPT review", f"reports/chatgpt_review/chatgpt_review_{date}_{mode}.md"),
             ("Research groups CSV", f"reports/research_groups/{run_id}.csv"), ("Manifest", f"reports/manifests/{run_id}.json")]
    links = "".join(f'<li><a href="{GH}{p}">{n}</a></li>' for n, p in files if os.path.exists(p))
    body = f"""<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#111;max-width:780px">
<h1 style="font-size:20px;margin:0 0 6px">Football Intelligence {VER} {esc(mode)} report</h1>
<p style="margin:0 0 4px">Window: {esc(window)}. Run {esc(run_id)}, model {VER} (counts only, no averages). {len(C)} fixtures across {C.competition.nunique()} competitions.</p>
<p style="margin:0 0 10px"><b>{len(sel)} above the line</b>: <span style="color:{GREEN}"><b>High {nH}</b></span>, <span style="color:{AMBER}">Medium {nM}</span>, Weak {nW}, <span style="color:{RED}">rejected {nR}</span>. Trump cards: {nT}.</p>
<h2 style="font-size:16px;margin:16px 0 6px;border-bottom:2px solid #111;padding-bottom:3px">By league, in order</h2>
{league_table}
<h2 style="font-size:16px;margin:20px 0 6px;border-bottom:2px solid #111;padding-bottom:3px">Shortlist, ranked by model score</h2>
<p style="margin:0 0 6px;font-size:13px;color:{MUTED}">High is model score {CUTS["green"]:.3f} or more, Medium {CUTS["weak"]:.3f} to {CUTS["green"] - 0.001:.3f}, Weak {CUTS["amber"]:.3f} to {CUTS["weak"] - 0.001:.3f}. The two drivers are Scored 2+ and Let in 2+ over each side's last five league games. There is no BTTS verdict: the Scoring line shows how often each side scored, failed to score and saw both teams score in its last five. A trump card (a side that scored 16+ goals in its last five league games, against an opponent that kept fewer than 2 clean sheets) is in by Rob's rule.</p>
{shortlist}
{research}
<h2 style="font-size:16px;margin:20px 0 6px;border-bottom:2px solid #111;padding-bottom:3px">Postponed, flagged, warnings</h2>
<p style="margin:4px 0;font-size:13px">{esc("; ".join(flagged)) if flagged else "No postponed or other-status fixtures in the window."}</p>
<p style="margin:4px 0;font-size:13px">{esc("; ".join(warnings)) if warnings else "No data-quality warnings."}</p>
<h2 style="font-size:16px;margin:20px 0 6px;border-bottom:2px solid #111;padding-bottom:3px">Files</h2>
<ul style="margin:4px 0 0 18px;padding:0;font-size:13px">{links}</ul>
</div>"""
    path = f"{outdir}/email_{date}_{mode}.html"
    open(path, "w", encoding="utf-8").write(body)
    first = sel.date.iloc[0] if len(sel) else ""
    print(f"Football {VER} {mode}: {window}")
    print(path)

if __name__ == "__main__":
    main()
