import pandas as pd, numpy as np, itertools
D=pd.read_pickle("D.pkl"); D=D[D.q_avg.notna()&D.b365_o.notna()].copy()
k=pd.to_datetime(D.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); D=D[k.dt.weekday>=4].copy(); k=k[D.index]
D["wk"]=(k-pd.to_timedelta(k.dt.weekday-4,unit="D")).dt.date
B={2:.025,3:.05,4:.075,5:.10,6:.125,7:.15,8:.20,9:.25,10:.30,11:.35,12:.40,13:.45,14:.50,15:.55,16:.60,17:.70,18:.80,19:.90,20:1.0}
G={wk:g for wk,g in D.groupby("wk")}
def sim(minp,rank,n,ngroups,boost=True):
    res=[]
    for wk,g in G.items():
        t=g[(g.q_avg>=minp)&(g.b365_o>=1.10)]
        t=t.assign(v=t.q_avg*t.b365_o if rank=="value" else t.q_avg).sort_values("v",ascending=False)
        if len(t)<n*ngroups: continue
        st=0;ret=0
        for i in range(ngroups):
            leg=t.iloc[i*n:(i+1)*n]; O=float(np.prod(leg.b365_o)); st+=1
            if leg.y.all(): ret+=1+(O-1)*(1+(B[n] if boost else 0))
        res.append((int(g.season.iloc[0]),st,ret))
    return pd.DataFrame(res,columns=["season","st","ret"])
rows=[]; rng=np.random.default_rng(3)
for minp,rank,n,ng in itertools.product((0.55,0.6,0.65),("value","shortest"),(3,5,8,10,14),(1,2,3)):
    W=sim(minp,rank,n,ng)
    if len(W)<30: continue
    pl=W.ret-W.st; per={s:round(float(pl[W.season==s].sum()/max(1,W.st[W.season==s].sum())),2) for s in (2023,2024,2025,2026)}
    bs=[pl.sample(len(pl),replace=True,random_state=int(rng.integers(1e9))).sum()/W.st.sum() for _ in range(500)]
    nb=sim(minp,rank,n,ng,False); plnb=(nb.ret-nb.st).sum()/nb.st.sum()
    rows.append((minp,rank,n,ng,len(W),int(W.st.sum()),round(pl.sum()/W.st.sum(),3),round(plnb,3),per,round(np.percentile(bs,10),2),round(np.percentile(bs,50),2),round(np.mean(np.array(bs)>0),2)))
R=pd.DataFrame(rows,columns=["min fair p","rank","n-fold","accas/wk","weekends","bets","return per £1 net (boost)","net no boost","by season (net per £1)","10th pct","median","share of resamples >0"])
pd.set_option("display.width",300); print(R.sort_values("share of resamples >0",ascending=False).to_string(index=False))
R.to_csv("grid.csv",index=False)
print("configs",len(R),"positive overall",int((R["return per £1 net (boost)"]>0).sum()),"positive without boost",int((R["net no boost"]>0).sum()))
