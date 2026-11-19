import pandas as pd, numpy as np
D=pd.read_pickle("D.pkl"); D=D[D.q_avg.notna()&D.b365_o.notna()].copy()
k=pd.to_datetime(D.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); D=D[k.dt.weekday>=4].copy(); k=k[D.index]
D["wk"]=(k-pd.to_timedelta(k.dt.weekday-4,unit="D")).dt.date
for lo in (0.55,0.6,0.65):
    s=D[D.q_avg>=lo]; pl=s.b365_o*s.y-1
    print(f"singles q>={lo}: n {len(s)} hits {int(s.y.sum())} expected by market {s.q_avg.sum():.0f}  return per £1 {pl.mean():+.3f}  by season", {y:round(float(pl[s.season==y].mean()),3) for y in (2023,2024,2025,2026)})
# correlation: within-weekend hit rate dispersion vs binomial
s=D[D.q_avg>=0.6]; g=s.groupby("wk").agg(n=("y","size"),h=("y","sum"),e=("q_avg","sum"))
g=g[g.n>=10]; z=(g.h-g.e); var_bin=(s.groupby("wk").apply(lambda x:(x.q_avg*(1-x.q_avg)).sum())).reindex(g.index)
print("weekends",len(g),"observed variance of weekend hits minus expected",round(float(z.var()),2),"binomial variance",round(float(var_bin.mean()),2),"ratio",round(float(z.var()/var_bin.mean()),2))
# 5-fold: observed win freq vs product of q and vs product of leg-level calibrated hit (bucket)
rows=[]
for wk,g2 in s.groupby("wk"):
    t=g2.sort_values("q_avg",ascending=False)
    for i in range(0,len(t)-4,5):
        L=t.iloc[i:i+5]; rows.append((float(np.prod(L.q_avg)),int(L.y.all()),float(L.y.mean())))
R=pd.DataFrame(rows,columns=["pq","win","legrate"])
print("5-folds",len(R),"won",int(R.win.sum()),"expected (market, independent)",round(R.pq.sum(),1),"expected using actual leg hit rate, independent",round(len(R)*R.legrate.mean()**5,1))
