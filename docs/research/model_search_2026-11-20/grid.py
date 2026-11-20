import itertools, numpy as np, pandas as pd, time
from common import *
X=load(); E=X[X.ev].reset_index(drop=True)
g=lambda c: (E[f"h_{c}"]+E[f"a_{c}"]).values.astype(float)
T={"scored2+":g("l5L_gf2"),"letin2+":g("l5L_ga2"),"3+games":g("l5L_over25"),"cleansheets(-)":-g("l5L_cs"),
   "failed2score(-)":-g("l5L_fts"),"btts":g("l5L_btts"),"venue3+":g("v3L_over25"),"division":10*E.lg_o25.fillna(E.lg_o25.mean()).values,
   "routes":(np.minimum(E.h_l5L_gf2,E.a_l5L_ga2)+np.minimum(E.a_l5L_gf2,E.h_l5L_ga2)).values.astype(float),
   "3+games_l10":g("l10_over25")}
names=list(T); M=np.vstack([np.nan_to_num(T[n]) for n in names]).T
tie=1e-4*np.nan_to_num(E.lg_o25.values)-1e-9*E.fixture_id.values
wk=pd.factorize(E.wk)[0]; y=E.y.values; season=E.season.values
trn=np.isin(season,[2023,2024]); tst=np.isin(season,[2025,2026])
order_wk=np.argsort(wk,kind="stable")
def top20_hits(score):
    o=np.lexsort((-(score+tie),wk)); w=wk[o]
    first=np.r_[0,np.flatnonzero(np.diff(w))+1]; rank=np.arange(len(o))-np.repeat(first,np.diff(np.r_[first,len(o)]))
    sel=o[rank<20]; return sel
W=[0,1,2]; rows=[]; t0=time.time()
for ws in itertools.product(W,repeat=len(names)):
    if sum(ws)==0: continue
    s=M@np.array(ws,float); sel=top20_hits(s)
    a=sel[trn[sel]]; b=sel[tst[sel]]
    rows.append((ws,y[a].sum(),len(a),y[b].sum(),len(b),y[sel[season[sel]==2025]].sum(),y[sel[season[sel]==2026]].sum()))
print("formulas",len(rows),"secs",round(time.time()-t0))
R=pd.DataFrame(rows,columns=["w","tr_hit","tr_n","te_hit","te_n","te25","te26"])
R["formula"]=R.w.apply(lambda ws:" + ".join((f"{v}x " if v>1 else "")+n for v,n in zip(ws,names) if v))
R.to_pickle("grid.pkl")
v=top20_hits(E.p_v41.values); print("V4.1 train",y[v[trn[v]]].sum(),"test",y[v[tst[v]]].sum(),"of",tst[v].sum())
R=R.sort_values("tr_hit",ascending=False)
pd.set_option("display.width",250); pd.set_option("display.max_colwidth",120)
print("TOP 15 BY TRAINING (2023-25), then their test (2025-27):"); print(R.head(15)[["formula","tr_hit","tr_n","te_hit","te_n","te25","te26"]].to_string(index=False))
print("test hits of top-100 train formulas: min/median/max",R.head(100).te_hit.min(),R.head(100).te_hit.median(),R.head(100).te_hit.max())
print("BEST IN HINDSIGHT ON TEST (overfit ceiling):"); print(R.sort_values("te_hit",ascending=False).head(5)[["formula","tr_hit","te_hit","te_n"]].to_string(index=False))
for n in names:
    one=R[R.w.apply(lambda ws: sum(ws)==1 and ws[names.index(n)]==1)]; print("single:",n,one.tr_hit.values,one.te_hit.values)
