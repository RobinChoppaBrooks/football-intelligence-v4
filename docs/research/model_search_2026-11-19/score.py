import pickle, numpy as np, pandas as pd, sys
res=pickle.load(open(sys.argv[1] if len(sys.argv)>1 else "h_res.pkl","rb"))
base=sys.argv[2] if len(sys.argv)>2 else "V4.1 refit (same recipe)"
def topk(d,K):
    return d.sort_values(["wk","s","fixture_id"],ascending=[True,False,True]).groupby("wk").head(K)
rows=[]; rng=np.random.default_rng(5)
B={K:topk(res[base],K).groupby("wk").y.sum() for K in (20,30)}
for name,d in res.items():
    r=dict(model=name)
    for K in (20,30,50):
        t=topk(d,K); r[f"top{K}"]=f"{int(t.y.sum())} of {len(t)}"; r[f"top{K}_rate"]=t.y.mean()
        for s in (2024,2025,2026): r[f"t{K}_{s}"]=round(t[t.season==s].y.mean()*100,1)
    th=d[d.s>=d.cut]; r["own cut"]=f"{int(th.y.sum())} of {len(th)}"; r["own cut picks/wk"]=round(th.groupby("wk").size().reindex(d.wk.unique(),fill_value=0).mean(),1); r["own_rate"]=th.y.mean()
    w=topk(d,20).groupby("wk").y.sum(); diff=(w-B[20]).reindex(B[20].index).fillna(0)
    bs=[diff.sample(len(diff),replace=True,random_state=int(rng.integers(1e9))).sum() for _ in range(2000)]
    r["top20 extra hits v base"]=int(diff.sum()); r["90% range"]=f"{np.percentile(bs,5):.0f} to {np.percentile(bs,95):.0f}"
    rows.append(r)
R=pd.DataFrame(rows).sort_values("top20_rate",ascending=False)
pd.set_option("display.width",320); pd.set_option("display.max_columns",30)
print(R[["model","top20","t20_2024","t20_2025","t20_2026","top30","top50","own cut","own cut picks/wk","top20 extra hits v base","90% range"]].to_string(index=False))
R.to_csv(sys.argv[1].replace(".pkl",".csv") if len(sys.argv)>1 else "h_res.csv",index=False)
