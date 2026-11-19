import pandas as pd, numpy as np
D=pd.read_pickle("D.pkl"); D=D[D.q_avg.notna()&D.b365_o.notna()&D.b365_u.notna()].copy()
k=pd.to_datetime(D.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); D=D[k.dt.weekday>=4].copy(); k=k[D.index]
D["wk"]=(k-pd.to_timedelta(k.dt.weekday-4,unit="D")).dt.date
BOOST={2:.025,3:.05,4:.075,5:.10,6:.125,7:.15,8:.20,9:.25,10:.30,11:.35,12:.40,13:.45,14:.50,15:.55,16:.60,17:.70,18:.80,19:.90,20:1.0}
D["v_o"]=D.q_avg*D.b365_o; D["v_u"]=(1-D.q_avg)*D.b365_u
def legs(g,mode):
    if mode=="over": t=g.assign(v=g.v_o,pr=g.b365_o,pw=g.q_avg,win=g.y)
    elif mode=="under": t=g.assign(v=g.v_u,pr=g.b365_u,pw=1-g.q_avg,win=1-g.y)
    else:
        o=g.v_o>=g.v_u; t=g.assign(v=np.where(o,g.v_o,g.v_u),pr=np.where(o,g.b365_o,g.b365_u),pw=np.where(o,g.q_avg,1-g.q_avg),win=np.where(o,g.y,1-g.y))
    return t[t.pr>=1.10].sort_values("v",ascending=False)
rows=[]
for mode in ("over","best side"):
  for n in (5,8,10,12,14,17,20):
    ev=[];won=0;real=0;cnt=0;vleg=[];pwin=[]
    for wk,g in D.groupby("wk"):
        t=legs(g,mode).head(n)
        if len(t)<n: continue
        O=float(np.prod(t.pr)); pw=float(np.prod(t.pw)); b=BOOST[n]
        ret=1+(O-1)*(1+b); ev.append(pw*ret); pwin.append(pw); vleg.append(float(t.v.mean())); cnt+=1
        if t.win.all(): won+=1; real+=ret
    rows.append((mode,n,cnt,round(np.mean(vleg),3),round(np.mean(ev),3),f"1 in {round(1/np.mean(pwin))}",won,round(real-cnt,1)))
R=pd.DataFrame(rows,columns=["legs from","n-fold","weekends","avg leg value (fair x Bet365)","EV per £1 with boost","chance per weekend","weekends won","realised P/L per £1 a weekend (units)"])
print(R.to_string(index=False))
