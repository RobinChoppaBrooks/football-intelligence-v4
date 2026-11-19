import json, glob, difflib, sqlite3, pandas as pd, re, unicodedata
REPO="/home/claude/football-intelligence-v4"
comp=json.load(open(f"{REPO}/config/competitions.json"))
byname={c["name"]:c["league_id"] for c in comp["english"]+comp["european"]}
CODES={"E0":"Premier League","E1":"Championship","E2":"League One","E3":"League Two","EC":"National League","D1":"Bundesliga","N1":"Eredivisie","F1":"Ligue 1","T1":"Super Lig","SC0":"Scottish Premiership","SP1":"La Liga","P1":"Primeira Liga"}
PR={"b365_o":"B365>2.5","b365_u":"B365<2.5","pin_o":"P>2.5","pin_u":"P<2.5","max_o":"Max>2.5","max_u":"Max<2.5","avg_o":"Avg>2.5","avg_u":"Avg<2.5",
    "b365c_o":"B365C>2.5","b365c_u":"B365C<2.5","pinc_o":"PC>2.5","pinc_u":"PC<2.5","maxc_o":"MaxC>2.5","maxc_u":"MaxC<2.5","avgc_o":"AvgC>2.5","avgc_u":"AvgC<2.5"}
c=sqlite3.connect("/tmp/fdb.db")
fx=pd.read_sql("select f.fixture_id,f.league_id,f.season,f.kickoff_utc,f.ft_home,f.ft_away,h.name hn,a.name an from fixtures f join teams h on h.team_id=f.home_id join teams a on a.team_id=f.away_id",c)
fx["date"]=pd.to_datetime(fx.kickoff_utc,utc=True).dt.tz_convert("Europe/London").dt.date
def norm(s):
    s=unicodedata.normalize("NFKD",str(s)).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]","",re.sub(r"\b(fc|afc|sc|cf|ac|sv|fk|united|utd|town|city|club|the)\b"," ",s))
def sim(a,b):
    a,b=norm(a),norm(b)
    if not a or not b: return 0
    return 1.0 if (a in b or b in a) else difflib.SequenceMatcher(None,a,b).ratio()
rows=[]; stats=[]
for f in sorted(glob.glob(f"{REPO}/data/research_odds/*.csv")):
    s,code=f.split("/")[-1][:-4].split("_"); season=2000+int(s[:2]); lid=byname[CODES[code]]
    d=pd.read_csv(f,encoding="latin1"); d.columns=[x.replace("﻿","").replace("ï»¿","") for x in d.columns]
    d=d[d.HomeTeam.notna()&d.FTHG.notna()].copy(); d["date"]=pd.to_datetime(d.Date,dayfirst=True).dt.date
    g=fx[(fx.league_id==lid)&(fx.season==season)]; m=0; used=set()
    for r in d.to_dict("records"):
        dt=r["date"]; cand=g[g.date.isin([dt,dt+pd.Timedelta(days=1),dt-pd.Timedelta(days=1)])&(g.ft_home==r["FTHG"])&(g.ft_away==r["FTAG"])]
        cand=cand[~cand.fixture_id.isin(used)]
        if cand.empty: continue
        sc=cand.apply(lambda x: sim(x.hn,r["HomeTeam"])+sim(x.an,r["AwayTeam"]),axis=1); b=sc.idxmax()
        if sc[b]<1.0: continue
        used.add(int(cand.loc[b,"fixture_id"])); m+=1
        row=dict(fixture_id=int(cand.loc[b,"fixture_id"]),fd_code=code,fd_home=r["HomeTeam"],fd_away=r["AwayTeam"],db_home=cand.loc[b,"hn"],db_away=cand.loc[b,"an"],msc=round(float(sc[b]),2))
        for k,col in PR.items(): row[k]=pd.to_numeric(r.get(col),errors="coerce")
        rows.append(row)
    stats.append((s,code,len(d),len(g[g.ft_home.notna()]),m))
P=pd.DataFrame(rows); P.to_pickle("prices_hist.pkl")
S=pd.DataFrame(stats,columns=["season","code","fd_rows","db_finished","matched"]); print(S.to_string(index=False)); print("total matched",len(P),"of",S.fd_rows.sum())
print(P.sort_values("msc").head(12)[["fd_home","db_home","fd_away","db_away","msc"]])
