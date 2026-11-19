import pickle, numpy as np, pandas as pd
R={}
for f in ("h_res.pkl","h2_res.pkl","h3_res.pkl"):
    for k,v in pickle.load(open(f,"rb")).items():
        R[k if k not in R else k+" ("+f[:2]+")"]=v
X=pd.read_pickle("X_all.pkl")[["fixture_id","league_id"]]
def top(d,K,cap=None):
    d=d.merge(X,on="fixture_id").sort_values(["wk","s","fixture_id"],ascending=[True,False,True])
    if cap: d=d[d.groupby(["wk","league_id"]).cumcount()<cap]
    return d.groupby("wk").head(K)
base=top(R["V4.1 locked (as published)"],20); base=base[base.season>=2025]; bw=base.groupby("wk").y.sum()
rng=np.random.default_rng(9); rows=[]
for name,d in R.items():
    for cap in (None,4):
        t=top(d,20,cap); t=t[t.season>=2025]; w=t.groupby("wk").y.sum().reindex(bw.index).fillna(0); diff=w-bw
        bs=[diff.sample(len(diff),replace=True,random_state=int(rng.integers(1e9))).sum() for _ in range(2000)]
        rows.append((name+(" [max 4 a league]" if cap else ""),f"{int(t.y.sum())} of {len(t)}",int(t[t.season==2025].y.sum()),int(t[t.season==2026].y.sum()),int(diff.sum()),f"{np.percentile(bs,5):.0f} to {np.percentile(bs,95):.0f}",round(float(np.mean(np.array(bs)>0)),2)))
T=pd.DataFrame(rows,columns=["model","top 20 a weekend, 2025-26 + 2026-27","hits 25-26","hits 26-27","hits v V4.1","90% range","share of resamples better"]).sort_values("hits v V4.1",ascending=False)
pd.set_option("display.width",250); print("weekends",len(bw)); print(T.head(16).to_string(index=False)); print(T[T.model.str.contains("max 4")].head(3).to_string(index=False))
T.to_csv("clean_h2h.csv",index=False)
