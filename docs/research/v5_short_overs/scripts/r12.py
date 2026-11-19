import pandas as pd, numpy as np
D=pd.read_pickle("D.pkl"); D=D[D.q_avg.notna()&D.b365_o.notna()].copy()
k=pd.to_datetime(D.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); D=D[k.dt.weekday>=4].copy(); k=k[D.index]
D["wk"]=(k-pd.to_timedelta(k.dt.weekday-4,unit="D")).dt.date
B={2:.025,3:.05,4:.075,5:.10,6:.125,7:.15,8:.20,9:.25,10:.30,11:.35,12:.40,13:.45,14:.50,15:.55,16:.60,17:.70,18:.80,19:.90,20:1.0}
PORT=[("5-fold A",5,10.0),("5-fold B",5,10.0),("5-fold C",5,10.0),("10-fold",10,4.0),("14-fold",14,2.0)]
def acca(t,stake,n,boost=True):
    O=float(np.prod(t.b365_o)); 
    return stake*(1+(O-1)*(1+(B[n] if boost else 0))) if t.y.all() else 0.0
out=[]
for wk,g in D.groupby("wk"):
    t=g[(g.q_avg>=0.60)&(g.b365_o>=1.10)].assign(v=lambda x:x.q_avg*x.b365_o).sort_values("v",ascending=False)
    if len(t)<15: continue
    r=dict(wk=wk,season=int(g.season.iloc[0]),legs=len(t))
    st=0;ret=0;retnb=0
    for i,(nm,n,s) in enumerate(PORT[:3]):
        leg=t.iloc[i*5:(i+1)*5]; st+=s; ret+=acca(leg,s,5); retnb+=acca(leg,s,5,False)
    for nm,n,s in PORT[3:]:
        if len(t)>=n: leg=t.head(n); st+=s; ret+=acca(leg,s,n); retnb+=acca(leg,s,n,False)
    r.update(staked=st,ret=ret,ret_noboost=retnb); out.append(r)
W=pd.DataFrame(out)
for s,g in W.groupby("season"):
    print(s,"weekends",len(g),"staked",round(g.staked.sum()),"returned",round(g.ret.sum()),"P/L",round(g.ret.sum()-g.staked.sum()),"| without boost P/L",round(g.ret_noboost.sum()-g.staked.sum()),"| winning weekends",int((g.ret>0).sum()))
print("ALL weekends",len(W),"staked",round(W.staked.sum()),"P/L",round(W.ret.sum()-W.staked.sum()),"no boost",round(W.ret_noboost.sum()-W.staked.sum()))
# drawdown
c=(W.ret-W.staked).cumsum(); print("worst run (max drawdown) £",round((c.cummax()-c).max()),"; biggest single weekend return £",round(W.ret.max()))
W.to_csv("portfolio_weeks.csv",index=False)
