import pandas as pd, numpy as np, itertools
D=pd.read_pickle("D.pkl"); D=D[D.q_avg.notna()&D.b365_o.notna()].copy()
k=pd.to_datetime(D.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); D=D[k.dt.weekday>=4].copy(); k=k[D.index]
D["wk"]=(k-pd.to_timedelta(k.dt.weekday-4,unit="D")).dt.date
B={1:0,2:.025,3:.05,4:.075,5:.10,6:.125,7:.15,8:.20,9:.25,10:.30}
G={s:list(g.groupby("wk")) for s,g in D.groupby("season")}
def sim(season,minp,maxp,rank,n,ng,boost):
    st=ret=0;wins=0;wks=0;pw=0
    for wk,g in G[season]:
        t=g[(g.q_avg>=minp)&(g.q_avg<maxp)&(g.b365_o>=1.10)]
        t=t.assign(v=t.q_avg*t.b365_o if rank=="value" else t.q_avg).sort_values("v",ascending=False)
        wp=0;ws=0
        for i in range(ng):
            L=t.iloc[i*n:(i+1)*n]
            if len(L)<n: continue
            O=float(np.prod(L.b365_o)); st+=1; ws+=1
            if L.y.all(): r=1+(O-1)*(1+(B[n] if boost else 0)); ret+=r; wins+=1; wp+=r
        if ws: wks+=1; pw+=int(wp>ws)
    return st,ret,wins,wks,pw
rows=[]
for minp,maxp,rank,n,ng in itertools.product((0.5,0.55,0.6,0.65,0.7),(0.75,1.0),("value","fair"),(1,2,3,4,5,6,8,10),(1,2,3,4)):
    if minp>=maxp: continue
    st,ret,w,wks,pw=sim(2025,minp,maxp,rank,n,ng,False)
    if st<40: continue
    rows.append((minp,maxp,rank,n,ng,st,w,round((ret-st)/st,3),wks,pw))
R=pd.DataFrame(rows,columns=["min","max","rank","n","per wk","bets","won","ROI 25-26 no boost","weekends","profit weekends"])
print("configs",len(R),"with ROI>=0.10 on 2025-26:",int((R["ROI 25-26 no boost"]>=0.10).sum()))
R.to_pickle("s1.pkl")
# out-of-sample check of ALL configs that cleared 10% on 2025-26
ok=R[R["ROI 25-26 no boost"]>=0.10].copy()
for s in (2023,2024,2026):
    ok[f"ROI {s}"]=[round((lambda r:(r[1]-r[0])/r[0] if r[0] else np.nan)(sim(s,a.min,a.max,a.rank,a.n,a["per wk"] if False else a[4],False)),3) for a in ok.itertuples(index=False)]
ok.to_pickle("s1_ok.pkl")
print("of those, positive in 2026-27 (unseen):",int((ok["ROI 2026"]>0).sum()),"; ROI>=0.10 in 2026-27:",int((ok["ROI 2026"]>=0.10).sum()),
      "; positive in all of 2023-24, 2024-25, 2026-27:",int(((ok[["ROI 2023","ROI 2024","ROI 2026"]]>0).all(axis=1)).sum()),
      "; >=10% in all three:",int(((ok[["ROI 2023","ROI 2024","ROI 2026"]]>=0.10).all(axis=1)).sum()))
print("median out-of-sample ROI of the selected configs:", {c:round(float(ok[c].median()),3) for c in ("ROI 2023","ROI 2024","ROI 2026")})
