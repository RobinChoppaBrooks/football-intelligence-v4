import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier as HGB
from common import *
from rating import run
X=load(); P=run(0.05,0.5); X=X.merge(P[["lh","la","p3"]].rename(columns={"p3":"r_p3"}),left_on="fixture_id",right_index=True,how="left")
hgb=lambda: HGB(max_depth=3,learning_rate=0.04,max_iter=300,min_samples_leaf=80,l2_regularization=1.0,random_state=0)
rk=lambda d,c: d.groupby("wk")[c].rank(pct=True)
res={}
for test in (2025,2026):
    tr=X[X.season<test]; te=X[(X.season==test)&X.ev].copy()
    m=hgb().fit(tr[F38].fillna(-1),tr.y); te["refit"]=m.predict_proba(te[F38].fillna(-1))[:,1]
    C2=F38+["lh","la","r_p3"]; m=hgb().fit(tr[C2].fillna(-1),tr.y); te["refit+rating"]=m.predict_proba(te[C2].fillna(-1))[:,1]
    te["perleague"]=np.nan
    for lg,g in te.groupby("league_id"):
        t=tr[tr.league_id==lg]; m=hgb().fit(t[F38].fillna(-1),t.y); te.loc[g.index,"perleague"]=m.predict_proba(g[F38].fillna(-1))[:,1]
    te["div"]=te.lg_o25.fillna(0)
    te["rating"]=te.r_p3.fillna(0)
    te["V4.1+rating"]=rk(te,"p_v41")+rk(te,"rating")
    te["V4.1+division"]=rk(te,"p_v41")+rk(te,"div")
    te["V4.1 2x + rating + perleague"]=2*rk(te,"p_v41")+rk(te,"rating")+rk(te,"perleague")
    res[test]=te
cols=["p_v41","refit","refit+rating","perleague","rating","div","V4.1+rating","V4.1+division","V4.1 2x + rating + perleague"]
rng=np.random.default_rng(1); D=pd.concat(res.values())
base=topk(D,D.p_v41.values).groupby("wk").y.sum()
for c in cols:
    t=topk(D,D[c].values); w=t.groupby("wk").y.sum(); diff=(w-base).reindex(base.index).fillna(0)
    bs=[diff.sample(len(diff),replace=True,random_state=int(rng.integers(1e9))).sum() for _ in range(2000)]
    print(f"{c:32s} {int(t.y.sum())} of {len(t)}  25-26 {int(t[t.season==2025].y.sum())}  26-27 {int(t[t.season==2026].y.sum())}  v V4.1 {int(diff.sum()):+d}  90% {np.percentile(bs,5):.0f} to {np.percentile(bs,95):.0f}  leagues used {t.league_id.nunique()} top-league share {t.league_id.value_counts(normalize=True).iloc[0]:.2f}")
D.to_pickle("c_res.pkl")
