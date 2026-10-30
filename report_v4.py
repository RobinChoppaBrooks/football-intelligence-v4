"""
report_v4.py  -  PRODUCTION V4 report (locked 28 Oct 2026): the validated model is the unchanged selection engine.
Cards keep Scored 2+ and Let in 2+ as the prominent rows, with the model confidence (High / Medium / Weak / rejected),
division count, BTTS counts, clean sheets and failed-to-score counts, support and risk. No V2 / V3 alignment scores.

    python3 report_v4.py over25_analysis_YYYYMMDD.pkl football.db out.pdf out.csv "window" [--flagged f.csv] [--nofix "A,B"]

Derived from report_v2.py (kept as an experimental renderer). Original docstring follows.

report_v2.py  -  Over 2.5 model V2 report (Rob's brief, 28 Oct 2026): Scored 2+ and Let in 2+ as the dominant rows,
two-route alignment score and Primary / Secondary / Watchlist classification, Top 20, grouped shortlist, cards with
the five scorelines printed, rejected fixtures with reasons, coverage and methodology. Model verdict shown alongside.

    python3 report_v2.py over25_analysis_YYYYMMDD.pkl football.db out.pdf out.csv "window" [--flagged flagged.csv] [--nofix "Comp A,Comp B"]
"""
import os, sys, pickle, sqlite3, argparse, datetime as dt, math
import pandas as pd, numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable, KeepTogether, PageBreak
from reportlab.lib.styles import ParagraphStyle
from config import LEAGUES, CUPS, NONLEAGUE, ORDER
ALL = {**LEAGUES, **CUPS, **NONLEAGUE}

ap = argparse.ArgumentParser(); ap.add_argument("pkl"); ap.add_argument("db"); ap.add_argument("out"); ap.add_argument("csv"); ap.add_argument("window")
ap.add_argument("--flagged", default=None); ap.add_argument("--nofix", default="")
a = ap.parse_args()
rows = pickle.load(open(a.pkl, "rb")); c = sqlite3.connect(a.db)
teams = dict(c.execute("select team_id,name from teams"))

# ---------- alignment score (the brief's formula) ----------
n_ = lambda rs, f: sum(1 for x in rs if f(x))
def align(d):
    hr, ar, hv, av = d["hr"], d["ar"], d.get("hv5", d["hv"]), d.get("av5", d["av"])
    nh, na = len(hr), len(ar)
    hs2, hc2 = n_(hr, lambda x: x["gf"] >= 2), n_(hr, lambda x: x["ga"] >= 2)
    as2, ac2 = n_(ar, lambda x: x["gf"] >= 2), n_(ar, lambda x: x["ga"] >= 2)
    if nh < 3 or na < 3:
        return dict(hs2=hs2, hc2=hc2, as2=as2, ac2=ac2, nh=nh, na=na, rA=None, rB=None, score=None, cls="Insufficient data", strA="n/a", strB="n/a",
                    reason=f"only {nh} and {na} league games this season")
    fh, fa = hs2 / nh, as2 / na; dh, da = hc2 / nh, ac2 / na
    rA = math.sqrt(fh * da) * 100; rB = math.sqrt(fa * dh) * 100
    ven = ((n_(hv, lambda x: x["tot"] >= 3) / len(hv) if hv else 0) + (n_(av, lambda x: x["tot"] >= 3) / len(av) if av else 0)) / 2 * 100
    oth = (n_(hr, lambda x: x["tot"] >= 3) / nh + n_(ar, lambda x: x["tot"] >= 3) / na) / 2 * 100
    pen = 0.25 * abs(rA - rB)
    score = 0.4 * rA + 0.4 * rB + 0.1 * ven + 0.1 * oth - pen
    sa = hs2 >= 3 and ac2 >= 3; sb = as2 >= 3 and hc2 >= 3
    supA = hs2 >= 2 and ac2 >= 2; supB = as2 >= 2 and hc2 >= 2
    if sa and sb: cls = "Primary"
    elif (sa and supB) or (sb and supA): cls = "Secondary"
    elif sa or sb: cls = "Watchlist"
    else: cls = "Rejected"
    st = lambda s, sup: "Strong" if s else ("Some support" if sup else "Weak")
    if cls == "Rejected": reason = f"neither route reaches 3 of 5 both ways (home {hs2}/{nh} v away let in {ac2}/{na}; away {as2}/{na} v home let in {hc2}/{nh})"
    elif cls == "Watchlist": reason = "one credible route only"
    elif cls == "Secondary": reason = "one strong route with support on the other"
    else: reason = "both routes strong"
    return dict(hs2=hs2, hc2=hc2, as2=as2, ac2=ac2, nh=nh, na=na, rA=round(rA), rB=round(rB), ven=round(ven), oth=round(oth), pen=round(pen, 1),
                score=round(score), cls=cls, strA=st(sa, supA), strB=st(sb, supB), reason=reason)

import pickle as _pk
_b = _pk.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bands_model.pkl"), "rb"))
WEAK = _b["amber"] + (_b["green"] - _b["amber"]) / 4
def div_count(comp):
    lid = ALL[comp][0]
    g = pd.read_sql(f"select ft_home,ft_away from fixtures where league_id={lid} and season=2026 and status in ('FT','AET','PEN')", c)
    if len(g) < 10: return None
    tot = g.ft_home + g.ft_away; share = float((tot >= 3).mean())
    return f"{'hot' if share >= 0.65 else 'warm' if share >= 0.55 else 'cold'}, {int((tot >= 3).sum())} of {len(tot)} games had 3+"
for d in rows:
    d["al"] = align(d)
    d["conf"] = "High" if d["light"] == "GREEN" else ("Weak" if (d["light"] == "AMBER" and d["p"] < WEAK) else ("Medium" if d["light"] == "AMBER" else "rejected"))
    d["al"]["cls"] = {"High": "High", "Medium": "Medium", "Weak": "Weak", "rejected": "Rejected"}[d["conf"]]
    d["al"]["score"] = None if d["al"]["nh"] < 3 or d["al"]["na"] < 3 else d["al"]["score"]
    d["both3"] = d["al"]["hs2"] >= 3 and d["al"]["as2"] >= 3
    d["div"] = div_count(d["comp"])
    d["btts_v2"] = "YES" if (d["al"]["cls"] in ("Primary",) or (d["al"]["cls"] == "Secondary" and d["pattern"] == "Both teams contribute")) else ("NO" if d["al"]["cls"] in ("Rejected", "Watchlist", "Insufficient data") else d["btts"])
    d["risk_v2"] = d["risk"]
    if d["al"]["cls"] != "Insufficient data":
        hr, ar = d["hr"], d["ar"]
        if d["al"]["hc2"] >= 3 and d["al"]["hs2"] <= 1: d["risk_v2"] = f"{d['home']} let in 2+ in {d['al']['hc2']} of 5 but scored 2+ only {d['al']['hs2']} of 5: leaky, not scoring"
        elif d["al"]["ac2"] >= 3 and d["al"]["as2"] <= 1: d["risk_v2"] = f"{d['away']} let in 2+ in {d['al']['ac2']} of 5 but scored 2+ only {d['al']['as2']} of 5: leaky, not scoring"

CLS_ORDER = {"High": 0, "Medium": 1, "Weak": 2, "Rejected": 3, "Insufficient data": 4}
def kodate(d): return d["kickoff"][:10]
ranked = sorted([d for d in rows if d["conf"] != "rejected"], key=lambda d: (-d["p"], d["fixture"]))     # model score ranks within the selected set
top20 = ranked[:20]

# ---------- CSV ----------
def flat(d):
    al = d["al"]
    return dict(fixture_id=d["fixture_id"], date=d["kickoff"], competition=d["comp"], fixture=d["fixture"],
                home_scored2=al["hs2"], home_letin2=al["hc2"], away_scored2=al["as2"], away_letin2=al["ac2"], home_games=al["nh"], away_games=al["na"],
                route_home_attack=al["rA"], route_away_attack=al["rB"], venue_component=al.get("ven"), other_component=al.get("oth"), penalty=al.get("pen"),
                alignment_score=al["score"], classification=al["cls"], route_home_strength=al["strA"], route_away_strength=al["strB"],
                over25_v2=("Yes" if al["cls"] in ("Primary", "Secondary", "Watchlist") else "No"), btts_v2=d["btts_v2"],
                model_confidence=d["conf"], model_over25=("Yes" if d["light"] != "RED" else "No"), model_btts=d["btts"], model_btts_likelihood=d["btts_lik"], btts_lean=d.get("btts_lean"), btts_note=d.get("btts_note", ""), trump=int(bool(d.get("trump", False))), drivers20=d.get("drivers20"), model_score=d["p"],
                home_scores="; ".join(f"{x['gf']}-{x['ga']}" for x in d["hr"]), away_scores="; ".join(f"{x['gf']}-{x['ga']}" for x in d["ar"]),
                home_venue_scores="; ".join(f"{x['gf']}-{x['ga']}" for x in d.get("hv5", d["hv"])), away_venue_scores="; ".join(f"{x['gf']}-{x['ga']}" for x in d.get("av5", d["av"])),
                why=d["why"], risk=d["risk_v2"], rejection_reason=al["reason"] if al["cls"] in ("Rejected", "Insufficient data") else "")
pd.DataFrame([flat(d) for d in rows]).drop(columns=["alignment_score", "classification", "route_home_strength", "route_away_strength", "over25_v2", "btts_v2", "route_home_attack", "route_away_attack", "venue_component", "other_component", "penalty"]).to_csv(a.csv, index=False)

# ---------- PDF ----------
_fd = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts"), "/usr/share/fonts/truetype/dejavu"]
_f = next(p for p in _fd if os.path.exists(os.path.join(p, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DV", os.path.join(_f, "DejaVuSans.ttf"))); pdfmetrics.registerFont(TTFont("DVB", os.path.join(_f, "DejaVuSans-Bold.ttf")))
BG, CARD, LINE, TXT, MUTED, EMPTY = (colors.HexColor("#0F1117"), colors.HexColor("#1A1D26"), colors.HexColor("#2A2E3A"), colors.HexColor("#E6E8EF"), colors.HexColor("#8B90A0"), colors.HexColor("#3A3F4C"))
GREEN, AMBER, RED = colors.HexColor("#3DDC97"), colors.HexColor("#F5B942"), colors.HexColor("#FF6B6B")
CC = {"High": GREEN, "Medium": AMBER, "Weak": AMBER, "Rejected": RED, "Insufficient data": RED}
W, H = A4
st = {k: ParagraphStyle(k, fontName=f, fontSize=s, textColor=cl, leading=s * 1.3) for k, f, s, cl in
      (("h1", "DVB", 17, TXT), ("h2", "DVB", 12, TXT), ("h3", "DVB", 9.5, TXT), ("body", "DV", 8.5, TXT), ("mut", "DV", 7.8, MUTED), ("sm", "DV", 7, TXT), ("smm", "DV", 7, MUTED), ("smb", "DVB", 7, TXT))}
def P(t, s="body"): return Paragraph(str(t).replace("&", "&amp;"), st[s])
def wrap(txt, font, size, width):
    line, lines = "", []
    for wd in txt.split():
        if pdfmetrics.stringWidth((line + " " + wd).strip(), font, size) > width: lines.append(line); line = wd
        else: line = (line + " " + wd).strip()
    return lines + [line]
CW = W - 24 * mm; CH = 124 * mm

class Card(Flowable):
    def __init__(s, d): super().__init__(); s.d = d; s.width, s.height = CW, CH
    def dots(s, x, y, rs, f, big=False):
        r = 2.8 * mm if big else 2.2 * mm; step = 7.2 * mm if big else 6 * mm
        for i in range(5):
            cx = x + i * step
            if i < len(rs):
                on = f(rs[i]); s.canv.setFillColor(GREEN if on else EMPTY); s.canv.setStrokeColor(GREEN if on else LINE); s.canv.circle(cx, y, r, fill=1, stroke=1)
    def draw(s):
        cv, d, al = s.canv, s.d, s.d["al"]
        cv.setFillColor(CARD); cv.setStrokeColor(CC[al["cls"]]); cv.setLineWidth(1.2); cv.roundRect(0, 0, s.width, s.height, 3 * mm, fill=1, stroke=1)
        top = s.height
        cv.setFillColor(TXT); cv.setFont("DVB", 12.5); cv.drawString(6 * mm, top - 9 * mm, d["fixture"])
        cv.setFillColor(MUTED); cv.setFont("DV", 8); cv.drawRightString(s.width - 6 * mm, top - 9 * mm, f"{d['comp']} · {d['kickoff']} UK")
        y = top - 16 * mm
        cv.setFillColor(CC[al["cls"]]); cv.setFont("DVB", 9); cv.drawString(6 * mm, y, f"OVER 2.5 {'YES' if d['light'] != 'RED' else 'NO'}  ·  confidence {d['conf'].upper()}")
        cv.setFillColor(MUTED); cv.setFont("DV", 8); cv.drawString(84 * mm, y, f"BTTS {d.get('btts_lean', d['btts'])} (model {d['btts_lik']}) · drivers {d.get('drivers20', '-')} of 20{' · TRUMP CARD' if d.get('trump') else ''}")
        cv.setFillColor(GREEN if d["both3"] else MUTED); cv.setFont("DVB" if d["both3"] else "DV", 8); cv.drawRightString(s.width - 6 * mm, y - 4.5 * mm, "both attacks 3 of 5+" if d["both3"] else "")
        y -= 4.5 * mm; cv.setFillColor(MUTED); cv.setFont("DV", 7.5); cv.drawString(6 * mm, y, f"Division: {d['div'] or 'too few games yet'}")
        y -= 5 * mm; cv.setStrokeColor(LINE); cv.setLineWidth(0.6); cv.line(6 * mm, y, s.width - 6 * mm, y)
        # team panels
        y -= 6 * mm
        for k, (name, ven, rs, vs, vlab) in enumerate(((d["home"], "home", d["hr"], d.get("hv5", d["hv"]), "At home, 3+"), (d["away"], "away", d["ar"], d.get("av5", d["av"]), "Away, 3+"))):
            px = 6 * mm + k * (s.width / 2)
            cv.setFillColor(TXT); cv.setFont("DVB", 9); cv.drawString(px, y, f"{name.upper()}  {ven}")
            cv.setFillColor(MUTED); cv.setFont("DV", 6.5); cv.drawRightString(px + 88 * mm, y, "oldest → newest")
            cv.setFillColor(MUTED); cv.setFont("DV", 6.8); cv.drawString(px, y - 4 * mm, "scores: " + ", ".join(f"{x['gf']}-{x['ga']}" for x in rs) if rs else "no league games this season")
            yy = y - 11 * mm
            for lab, f, rr, big in (("SCORED 2+", lambda r: r["gf"] >= 2, rs, True), ("LET IN 2+", lambda r: r["ga"] >= 2, rs, True),
                                    ("Game had 3+", lambda r: r["tot"] >= 3, rs, False), ("Both scored", lambda r: r["gf"] > 0 and r["ga"] > 0, rs, False), (vlab, lambda r: r["tot"] >= 3, vs, False)):
                cv.setFillColor(TXT if big else MUTED); cv.setFont("DVB" if big else "DV", 9 if big else 8); cv.drawString(px, yy - 1 * mm, lab)
                s.dots(px + 34 * mm, yy, rr, f, big)
                cnt = n_(rr, f); cv.setFillColor(TXT if big else MUTED); cv.setFont("DVB" if big else "DV", 9 if big else 8); cv.drawString(px + 72 * mm, yy - 1 * mm, f"{cnt}/{len(rr)}")
                yy -= 7.5 * mm if big else 6 * mm
            if k == 0: cv.setStrokeColor(LINE); cv.line(s.width / 2 - 2 * mm, y + 3 * mm, s.width / 2 - 2 * mm, yy + 2 * mm)
        # match-up section
        ym = yy - 3 * mm; cv.setStrokeColor(LINE); cv.line(6 * mm, ym + 2 * mm, s.width - 6 * mm, ym + 2 * mm)
        if al["score"] is not None:
            for k, (ttl, a1, b1, stv, rt) in enumerate(((f"HOME ATTACK → AWAY DEFENCE", f"{d['home']} scored 2+: {al['hs2']}/{al['nh']}", f"{d['away']} let in 2+: {al['ac2']}/{al['na']}", al["strA"], al["rA"]),
                                                       (f"AWAY ATTACK → HOME DEFENCE", f"{d['away']} scored 2+: {al['as2']}/{al['na']}", f"{d['home']} let in 2+: {al['hc2']}/{al['nh']}", al["strB"], al["rB"]))):
                px = 6 * mm + k * (s.width / 2)
                cv.setFillColor(MUTED); cv.setFont("DVB", 7.5); cv.drawString(px, ym - 3 * mm, ttl)
                cv.setFillColor(TXT); cv.setFont("DV", 8); cv.drawString(px, ym - 7.5 * mm, a1); cv.drawString(px, ym - 11.5 * mm, b1)
                colr = GREEN if stv == "Strong" else (AMBER if stv == "Some support" else RED)
                cv.setFillColor(colr); cv.setFont("DVB", 8); cv.drawString(px, ym - 16 * mm, f"Route: {stv}")
            yw = ym - 21 * mm
            cs = lambda rs: (n_(rs, lambda x: x["ga"] == 0), n_(rs, lambda x: x["gf"] == 0), n_(rs, lambda x: x["gf"] > 0 and x["ga"] > 0))
            hc, ac = cs(d["hr"]), cs(d["ar"])
            cv.setFillColor(RED if (hc[0] >= 2 or hc[1] >= 2 or ac[0] >= 2 or ac[1] >= 2) else MUTED); cv.setFont("DV", 7.5)
            cv.setFont("DV", 7)
            cv.drawString(6 * mm, yw, f"{d['home'][:22]}: clean sheets {hc[0]}/{al['nh']}, failed to score {hc[1]}/{al['nh']}, both scored {hc[2]}/{al['nh']}")
            cv.drawString(s.width / 2 + 4 * mm, yw, f"{d['away'][:22]}: clean sheets {ac[0]}/{al['na']}, failed to score {ac[1]}/{al['na']}, both scored {ac[2]}/{al['na']}")
            yw -= 4.5 * mm
            cv.setFillColor(MUTED); cv.setFont("DVB", 7.5); cv.drawString(6 * mm, yw, "Why:"); cv.setFont("DV", 7.5)
            for ln in wrap(d["why"], "DV", 7.5, s.width - 24 * mm)[:2]: cv.drawString(17 * mm, yw, ln); yw -= 3.6 * mm
            cv.setFillColor(RED); cv.setFont("DVB", 7.5); cv.drawString(6 * mm, yw, "Risk:"); cv.setFont("DV", 7.5)
            for ln in wrap(d["risk_v2"], "DV", 7.5, s.width - 24 * mm)[:2]: cv.drawString(17 * mm, yw, ln); yw -= 3.6 * mm
        else:
            cv.setFillColor(RED); cv.setFont("DVB", 8.5); cv.drawString(6 * mm, ym - 4 * mm, f"INSUFFICIENT DATA: {al['reason']}")

def on_page(cv, doc):
    cv.setFillColor(BG); cv.rect(0, 0, W, H, fill=1, stroke=0); cv.setFillColor(MUTED); cv.setFont("DV", 7)
    cv.drawString(12 * mm, 8 * mm, f"Over 2.5 model V4  |  {a.window}  |  generated {dt.date.today():%d %b %Y}"); cv.drawRightString(W - 12 * mm, 8 * mm, f"Page {doc.page}")

def tstyle(extra=()):
    return TableStyle([("FONT", (0, 0), (-1, 0), "DVB", 7), ("FONT", (0, 1), (-1, -1), "DV", 6.8), ("TEXTCOLOR", (0, 0), (-1, -1), TXT), ("BACKGROUND", (0, 0), (-1, 0), CARD),
                       ("LINEBELOW", (0, 0), (-1, -1), 0.3, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2), *extra])

ncls = {k: sum(1 for d in rows if d["conf"] == k) for k in ("High", "Medium", "Weak", "rejected")}
nboth = sum(1 for d in rows if d["conf"] != "rejected" and d["both3"])
S = [P("Over 2.5 goals: V4 report", "h1"), Spacer(1, 2 * mm), P(a.window + ". All times UK.", "body"), Spacer(1, 3 * mm),
     P("Executive summary", "h2"), Spacer(1, 1.5 * mm),
     P(f"{len(rows)} fixtures analysed: High {ncls['High']}, Medium {ncls['Medium']}, Weak {ncls['Weak']}, rejected {ncls['rejected']}. Selected fixtures with both attacks scoring 2+ in 3 of 5 or better: {nboth}."),
     Spacer(1, 1.5 * mm),
     P("Selection engine: the validated model (V4 lock, unchanged since 19 Oct 2026). Out of sample it hit 69% in High (729 fixtures), 64% across all selected (2,518), 54% rejected (5,017). "
       "Those are band rates, not the chance of any one fixture. Scored 2+ and Let in 2+ counts are shown on every card as supporting evidence; both attacks at 3 of 5+ adds about three points inside the bands and is highlighted, not required.", "mut"), Spacer(1, 4 * mm)]
# Top 20
S += [P("Selected fixtures ranked by model score (up to 20)", "h2"), Spacer(1, 1.5 * mm)]
hdr = [P(h, "smb") for h in ["#", "Kick-off (UK)", "Competition", "Fixture", "Home sc2+ / let2+", "Away sc2+ / let2+", "Both 3/5+", "BTTS", "Confidence", "Division", "Main risk (Over 2.5 = Yes for every row)"]]
data = [hdr]
for i, d in enumerate(top20, 1):
    al = d["al"]
    data.append([P(str(i), "sm"), P(d["kickoff"], "sm"), P(d["comp"], "sm"), P(d["fixture"], "sm"), P(f"{al['hs2']}/{al['nh']}  ·  {al['hc2']}/{al['nh']}", "sm"), P(f"{al['as2']}/{al['na']}  ·  {al['ac2']}/{al['na']}", "sm"),
                 P("<font color='#3DDC97'><b>yes</b></font>" if d["both3"] else "", "sm"), P(f"{d['btts']} ({d['btts_lik'][:3]})", "sm"),
                 P(f"<font color='{ {'High':'#3DDC97','Medium':'#F5B942','Weak':'#F5B942'}[d['conf']] }'><b>{d['conf']}</b></font>", "sm"), P((d["div"] or "").split(",")[0], "sm"), P(d["risk_v2"], "smm")])
cwid = [5 * mm, 17 * mm, 18 * mm, 34 * mm, 15 * mm, 15 * mm, 10 * mm, 14 * mm, 14 * mm, 11 * mm]
t = Table(data, colWidths=cwid + [CW - sum(cwid)], repeatRows=1)
ts = []
t.setStyle(tstyle(ts)); S += [t, PageBreak()]
# grouped shortlist
S += [P("Grouped shortlist (date, competition, confidence, model score)", "h2"), Spacer(1, 1.5 * mm)]
short = [d for d in rows if d["conf"] != "rejected"]
short.sort(key=lambda d: (kodate(d), d["comp"], CLS_ORDER[d["al"]["cls"]], -d["p"]))
cur = None
for d in short:
    key = (kodate(d), d["comp"])
    if key != cur:
        cur = key; S += [Spacer(1, 2 * mm), P(f"{d['kickoff'][:10]}  ·  {d['comp']}", "h3"), Spacer(1, 1 * mm)]
    al = d["al"]
    S.append(Table([[P(f"<font color='{ {'High':'#3DDC97','Medium':'#F5B942','Weak':'#F5B942'}[d['conf']] }'><b>{d['conf']}</b></font>", "sm"), P(f"<b>{d['fixture']}</b> {d['kickoff'][-5:]}", "sm"),
                     P(f"H scored 2+ {al['hs2']}/{al['nh']} · H let in 2+ {al['hc2']}/{al['nh']} · A scored 2+ {al['as2']}/{al['na']} · A let in 2+ {al['ac2']}/{al['na']}" + (" · <font color='#3DDC97'>both 3/5+</font>" if d["both3"] else ""), "sm"),
                     P(f"BTTS {d['btts']} ({d['btts_lik']})", "smm")]], colWidths=[18 * mm, 52 * mm, 86 * mm, 30 * mm], style=tstyle([("BACKGROUND", (0, 0), (-1, -1), CARD)])))
S.append(PageBreak())
# cards
S += [P("Fixture cards", "h2"), Spacer(1, 2 * mm)]
order = {n: i for i, n in enumerate(ORDER)}
cards = sorted([d for d in rows if d["conf"] != "rejected"], key=lambda d: (order.get(d["comp"], 99), d["kickoff"], d["home"]))
cur = None
for d in cards:
    if d["comp"] != cur: cur = d["comp"]; S += [KeepTogether([P(cur, "h3"), Spacer(1, 1.5 * mm), Card(d)]), Spacer(1, 3 * mm)]
    else: S += [Card(d), Spacer(1, 3 * mm)]
S.append(PageBreak())
# rejected
S += [P("Rejected fixtures, with the model's reason", "h2"), Spacer(1, 1.5 * mm)]
rej = sorted([d for d in rows if d["conf"] == "rejected"], key=lambda d: (order.get(d["comp"], 99), d["kickoff"]))
for d in rej: d["al"]["reason"] = ("fewer than 3 league games for one side" if (d["al"]["nh"] < 3 or d["al"]["na"] < 3) else ("match-up contradicts the headline numbers" if any("contradicts" in e for e in d["ev_against"]) else "model score below the selection line") + (f"; attacks {d['al']['hs2']}/{d['al']['nh']} and {d['al']['as2']}/{d['al']['na']}" if d["al"]["nh"] >= 3 and d["al"]["na"] >= 3 else ""))
data = [["Kick-off (UK)", "Competition", "Fixture", "H sc2+", "H let2+", "A sc2+", "A let2+", "Model", "Reason"]]
for d in rej:
    al = d["al"]; data.append([d["kickoff"], d["comp"], d["fixture"], f"{al['hs2']}/{al['nh']}", f"{al['hc2']}/{al['nh']}", f"{al['as2']}/{al['na']}", f"{al['ac2']}/{al['na']}", "rejected", P(al["reason"], "smm")])
S += [Table(data, colWidths=[20 * mm, 24 * mm, 46 * mm, 9 * mm, 9 * mm, 9 * mm, 9 * mm, 13 * mm, 47 * mm], repeatRows=1, style=tstyle()), Spacer(1, 4 * mm)]
# coverage
S += [P("Data coverage and limitations", "h2"), Spacer(1, 1.5 * mm)]
cov = [f"Fixtures analysed: {len(rows)}. Every count is taken from the stored final score of each match (fixture ID, teams, score); the five scorelines are printed on each card.",
       "Form sample: each side's last five completed league games this season, cup ties excluded; venue rows use the last five league games at that venue, sample size shown when fewer.",
       "Not covered by API Sports for 2026-27: Northern Premier, Isthmian and Southern League Division One. 'England V2' is not an API Sports competition and was not included.",
       "Scored first / conceded after leading: needs match event timelines, not pulled (one call per match, no history). Not shown. First-half goals: available from half-time scores, not yet on the card.",
       "Injuries and suspensions: the API returned lists for a minority of fixtures this week; nothing is inferred where it returned none. Squad rotation in cup ties is not assessed.",
       "Opposition strength: each side's opponents' scoring versus the division is held in the analysis file (oq columns) but is not part of the alignment score."]
if a.nofix: cov.append(f"Competitions in scope with no fixtures in the window: {a.nofix}.")
if a.flagged and os.path.exists(a.flagged):
    fl = pd.read_csv(a.flagged)
    if len(fl): cov.append(f"Flagged, not analysed ({len(fl)}): " + "; ".join(f"{r.home} v {r.away} ({r.comp}, {r.status})" for r in fl.itertuples()))
for ln in cov: S += [P("• " + ln, "mut"), Spacer(1, 1 * mm)]
S += [Spacer(1, 3 * mm), P("Methodology (V4 lock)", "h2"), Spacer(1, 1.5 * mm)]
meth = ["Selection: gradient-boosted model on each side's last-5 league counts (goals, 3+, 2+ scored, 2+ conceded, clean sheets, failed to score, BTTS), last-3 venue counts and the division's 3+ share. Trained on 2023-24 and 2024-25, validated on 2025-26; cut points from validation deciles. High = top decile; Medium = next two; Weak = bottom quarter of Medium; rejected below.",
        "Out of sample (Jan to Jun 2026 and Aug to Oct 2026, 7,535 fixtures): High 69% (729), Selected 64% (2,518), rejected 54% (5,017). Band rates, not per-fixture probabilities.",
        "Scored 2+ and Let in 2+ are shown for both sides as evidence. Both attacks 3 of 5+ is highlighted (Selected with it 66%, High 71%) but never required: High fixtures failing a 2-of-5 attacking rule hit 73% on 222 fixtures.",
        "BTTS: YES when the pattern is 'both teams contribute' (two scoring routes, each side scoring in 4 of 5 and conceding in 3 of 5); likelihood from a second validated model (High 61%, Medium 55%, Low 50%). A lean, not a pick.",
        "V2 and V3 alignment scores were tested (62 to 66% at comparable sizes) and are not used for selection. Full tables in over25_backtest_baseline.md.",
        "No averages anywhere. Nothing inferred for missing data. Every count comes from stored final scores; the five scorelines are printed on each card."]
for ln in meth: S += [P("• " + ln, "mut"), Spacer(1, 1 * mm)]
SimpleDocTemplate(a.out, pagesize=A4, leftMargin=12 * mm, rightMargin=12 * mm, topMargin=12 * mm, bottomMargin=14 * mm).build(S, onFirstPage=on_page, onLaterPages=on_page)
print(f"wrote {a.out}: {len(rows)} fixtures; {ncls}; both attacks 3/5+ among selected: {nboth}")
