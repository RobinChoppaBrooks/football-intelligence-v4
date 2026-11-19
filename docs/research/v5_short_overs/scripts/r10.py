import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
D=pd.read_pickle("D.pkl"); D=D[D.q_avg.notna()&D.b365_o.notna()&D.b365_u.notna()].copy()
lg=lambda p: np.log(p/(1-p))
k=pd.to_datetime(D.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); D=D[k.dt.weekday>=4].copy(); k=k[D.index]
D["wk"]=(k-pd.to_timedelta(k.dt.weekday-4,unit="D")).dt.date
# recalibrated prob: fit on seasons before each season (2023 uses itself only for illustration -> exclude 2023 from results)
D["pc"]=np.nan
for s in (2024,2025,2026):
    tr=D[D.season<s]; m=LogisticRegression(C=1e6).fit(lg(tr[["q_avg"]]),tr.y); D.loc[D.season==s,"pc"]=m.predict_proba(lg(D.loc[D.season==s,["q_avg"]]))[:,1]
D=D[D.season>=2024]
BOOST={5:.10,8:.20,10:.30,12:.40,14:.50,17:.70,20:1.0}
def run(prob,minp,n,side):
    rows=[]
    for wk,g in D.groupby("wk"):
        if side=="over": t=g.assign(pr=g.b365_o,pw=g[prob],win=g.y)
        else:
            o=g[prob]>=0.5; t=g.assign(pr=np.where(o,g.b365_o,g.b365_u),pw=np.where(o,g[prob],1-g[prob]),win=np.where(o,g.y,1-g.y))
        t=t[(t.pw>=minp)&(t.pr>=1.10)].assign(v=lambda x:x.pw*x.pr).sort_values("v",ascending=False).head(n)
        if len(t)<n: continue
        O=float(np.prod(t.pr)); pw=float(np.prod(t.pw)); ret=1+(O-1)*(1+BOOST[n])
        rows.append((pw*ret,pw,int(t.win.all())*ret,float(t.v.mean()),int(t.win.sum())))
    if not rows: return None
    r=np.array(rows); return len(r),round(r[:,3].mean(),3),round(r[:,0].mean(),3),round(1/r[:,1].mean()),int((r[:,2]>0).sum()),round(r[:,2].sum()-len(r),1),round(r[:,4].mean(),1)
print("prob   side   min p  n  | weekends, avg leg value, EV/£1 with boost, 1-in chance, weekends won, realised net units, avg legs landed")
for prob in ("q_avg","pc"):
  for side in ("over","either"):
    for minp in (0.55,0.6,0.65):
      for n in (5,8,10,12,14,17,20):
        r=run(prob,minp,n,side)
        if r: print(prob,side,minp,n,"|",r)
