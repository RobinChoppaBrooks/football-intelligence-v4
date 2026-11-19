import pandas as pd, numpy as np
D=pd.read_pickle("D.pkl"); D=D[D.q_avg.notna()&D.b365_o.notna()].copy()
k=pd.to_datetime(D.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); D=D[k.dt.weekday>=4].copy(); k=k[D.index]
D["wk"]=(k-pd.to_timedelta(k.dt.weekday-4,unit="D")).dt.date
B={3:.05,5:.10,8:.20,10:.30}
# pre-registered weekly portfolio (19 Nov 2026)
PORT=[("treble",3,3,15.0,0.60,"value"),("5-fold",5,2,10.0,0.60,"value"),("8-fold",8,1,5.0,0.60,"shortest"),("10-fold",10,1,5.0,0.55,"shortest")]
rows=[]
for wk,g in D.groupby("wk"):
    st=ret=retnb=0.0; nb=0; wins=[]
    for nm,n,cnt,stake,minp,rank in PORT:
        t=g[(g.q_avg>=minp)&(g.b365_o>=1.10)]
        t=t.assign(v=t.q_avg*t.b365_o if rank=="value" else t.q_avg).sort_values("v",ascending=False)
        for i in range(cnt):
            L=t.iloc[i*n:(i+1)*n]
            if len(L)<n: continue
            O=float(np.prod(L.b365_o)); st+=stake; nb+=1
            if L.y.all(): ret+=stake*(1+(O-1)*(1+B[n])); retnb+=stake*O; wins.append(nm)
    if nb: rows.append(dict(wk=wk,season=int(g.season.iloc[0]),bets=nb,staked=st,ret=ret,ret_nb=retnb,wins=",".join(wins)))
W=pd.DataFrame(rows); W["pl"]=W.ret-W.staked; W["pl_nb"]=W.ret_nb-W.staked
for s,g in W.groupby("season"):
    print(f"{s}-{(s+1)%100:02d}: weekends {len(g)} staked £{g.staked.sum():.0f} returned £{g.ret.sum():.0f} P/L £{g.pl.sum():+.0f} (no boost £{g.pl_nb.sum():+.0f}); weekends in profit {int((g.pl>0).sum())}")
c=W.pl.cumsum(); print(f"ALL: weekends {len(W)} staked £{W.staked.sum():.0f} P/L £{W.pl.sum():+.0f} (no boost £{W.pl_nb.sum():+.0f}); profit weekends {int((W.pl>0).sum())}; worst drawdown £{(c.cummax()-c).max():.0f}; best weekend £{W.pl.max():.0f}; avg stake/weekend £{W.staked.mean():.0f}")
print("wins by bet type:", pd.Series(",".join(W.wins).split(",")).value_counts().to_dict())
# resample weekends
rng=np.random.default_rng(11); bs=[W.pl.sample(len(W),replace=True,random_state=int(rng.integers(1e9))).sum() for _ in range(5000)]
print("bootstrap P/L over the same number of weekends: 10th pct £%.0f, median £%.0f, share >0 %.2f"%(np.percentile(bs,10),np.median(bs),np.mean(np.array(bs)>0)))
# excluding the single best weekend
print("P/L without best weekend £%.0f, without best 2 £%.0f"%(W.pl.sum()-W.pl.max(), W.pl.sum()-W.pl.nlargest(2).sum()))
W.to_csv("v5_portfolio_weeks.csv",index=False)
