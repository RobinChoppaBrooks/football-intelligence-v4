import pandas as pd, numpy as np
D=pd.read_pickle("D.pkl"); D=D[D.q_avg.notna()&D.b365_o.notna()&D.b365_u.notna()].copy()
k=pd.to_datetime(D.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); D=D[k.dt.weekday>=4].copy(); k=k[D.index]
D["wk"]=(k-pd.to_timedelta(k.dt.weekday-4,unit="D")).dt.date
B={5:.10,8:.20,10:.30,12:.40,14:.50,17:.70,20:1.0}
def pick(g,side,minp,n,rank):
    if side=="over": t=g.assign(pr=g.b365_o,pw=g.q_avg,win=g.y)
    else:
        o=g.q_avg>=0.5; t=g.assign(pr=np.where(o,g.b365_o,g.b365_u),pw=np.where(o,g.q_avg,1-g.q_avg),win=np.where(o,g.y,1-g.y))
    t=t[(t.pw>=minp)&(t.pr>=1.10)]
    key={"value":t.pw*t.pr,"shortest":t.pw,"v41":g.p_v41.reindex(t.index)}[rank]
    return t.assign(k=key).sort_values("k",ascending=False).head(n)
rows=[]
for side in ("over","either"):
  for rank in ("value","shortest","v41"):
    for minp in (0.55,0.6):
      for n in (10,14,20):
        L=[];W=0
        for wk,g in D.groupby("wk"):
            t=pick(g,side,minp,n,rank)
            if len(t)<n: continue
            L.append(t.assign(wk=wk))
        if not L: continue
        A=pd.concat(L); leg=(A.pr*A.win-1)
        per={s:round(float(leg[A.season==s].mean()+1),3) for s in sorted(A.season.unique())}
        ev=float(leg.mean()+1)
        rows.append((side,rank,minp,n,A.wk.nunique(),len(A),round(ev,3),per,round(ev**n*(1+B[n]),3)))
R=pd.DataFrame(rows,columns=["side","rank by","min p","n","weekends","legs","realised leg return per £1","by season","implied acca EV with boost"])
pd.set_option("display.width",250); print(R.to_string(index=False))
