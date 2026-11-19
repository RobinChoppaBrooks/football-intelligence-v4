import sys, numpy as np, pandas as pd
sys.path.insert(0,"/home/claude/football-intelligence-v4"); import v5
D=pd.read_pickle("/home/claude/bt/D.pkl"); D=D[D.q_avg.notna()&D.b365_o.notna()].copy()
k=pd.to_datetime(D.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); D=D[k.dt.weekday>=4].copy(); k=k[D.index]
D["wk"]=(k-pd.to_timedelta(k.dt.weekday-4,unit="D")).dt.date
D=D.assign(fair=D.q_avg,price=D.b365_o)
rows=[]
for wk,g in D.groupby("wk"):
    for name,n,stake,legs in v5.build(g,1000):
        O=float(np.prod(legs.price)); won=bool(legs.y.all())
        rows.append(dict(wk=wk,season=int(g.season.iloc[0]),bet=name,n=n,stake=stake,odds=O,won=won,ret=stake*O if won else 0,ret_b=stake*(1+(O-1)*(1+v5.BOOST[n])) if won else 0))
R=pd.DataFrame(rows); R.to_csv("/home/claude/bt/v5_bets_backtest.csv",index=False)
for s,g in R.groupby("season"): print(s,"bets",len(g),"won",int(g.won.sum()),"staked",round(g.stake.sum()),"P/L",round(g.ret.sum()-g.stake.sum()),"with boost",round(g.ret_b.sum()-g.stake.sum()))
print("ALL bets",len(R),"won",int(R.won.sum()),"staked",round(R.stake.sum()),"P/L",round(R.ret.sum()-R.stake.sum()),"boost",round(R.ret_b.sum()-R.stake.sum()))
W=R.groupby("wk").apply(lambda g:(g.ret_b-g.stake).sum()); print("weekends",len(W),"mean P/L/wk",round(W.mean(),1),"sd",round(W.std(),1),"weekends needed for mean ~2 SE:",round((2*W.std()/W.mean())**2))
print(R.groupby("bet").apply(lambda g: pd.Series(dict(bets=len(g),won=int(g.won.sum()),pl=round(g.ret.sum()-g.stake.sum()),pl_b=round(g.ret_b.sum()-g.stake.sum())))))
