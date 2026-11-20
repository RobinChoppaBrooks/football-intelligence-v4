import numpy as np, pandas as pd
E=pd.read_pickle("/home/claude/bt/E_last5.pkl").reset_index(drop=True)
y=E.y.values; wk=pd.factorize(E.wk)[0]; season=E.season.values
trn=np.isin(season,[2023,2024]); tst=np.isin(season,[2025,2026])
div=np.nan_to_num(E.lg_o25.values); tie=1e-6*div
def top(score,K=20,mask=None):
    s=np.where(mask if mask is not None else True, score, -1e9)+tie
    o=np.lexsort((E.fixture_id.values,-s,wk)); w=wk[o]
    first=np.r_[0,np.flatnonzero(np.diff(w))+1]; rank=np.arange(len(o))-np.repeat(first,np.diff(np.r_[first,len(o)]))
    sel=o[rank<K]; 
    if mask is not None: sel=sel[mask[sel]]
    return sel
def res(sel): a=sel[trn[sel]]; b=sel[tst[sel]]; return int(y[a].sum()),len(a),int(y[b].sum()),len(b)
g=lambda s,t,m: np.nan_to_num(E[f"{s}_{t}_{m}"].values)
rows=[]
for N in (3,4,5,6,8,10):
  for V in ("all","ven"):
    t=f"{V}{N}"; hg,ha,ag,aa=g("h",t,"gf"),g("h",t,"ga"),g("a",t,"gf"),g("a",t,"ga")
    cs=g("h",t,"cs")+g("a",t,"cs"); fts=g("h",t,"fts")+g("a",t,"fts"); o3=g("h",t,"o3")+g("a",t,"o3")
    goals=hg+ha+ag+aa; route=np.minimum(hg+aa,ag+ha)
    S={"goals in both sides' games":goals,"weaker attack-v-defence route":route,"goals scored only":hg+ag,"goals conceded only":ha+aa,
       "fewest clean sheets":-cs+0.01*goals,"3+ games":o3+0.01*goals,"route then goals":route+0.1*goals}
    for k in (1,2,3): S[f"goals minus {k}x clean sheets"]=goals-k*cs; S[f"goals minus {k}x clean sheets and failed to score"]=goals-k*(cs+fts)
    for k in (1,2): S[f"route minus {k}x clean sheets"]=route-k*cs
    for name,s in S.items():
        rows.append((t,name)+res(top(s)))
R=pd.DataFrame(rows,columns=["window","formula","tr_hit","tr_n","te_hit","te_n"])
v=top(E.p_v41.values); print("V4.1:",res(v)); dv=top(div); print("division only:",res(dv))
R=R.sort_values("tr_hit",ascending=False); R.to_csv("last5_grid.csv",index=False)
pd.set_option("display.width",200)
print("formulas tested",len(R)); print("TOP 12 ON TRAINING, then test:"); print(R.head(12).to_string(index=False))
print("\nBest per formula family on the last-5 all-games window:"); print(R[R.window=="all5"].sort_values("te_hit",ascending=False).to_string(index=False))
print("\nBest window for 'goals in both sides games':"); print(R[R.formula=="goals in both sides' games"].sort_values("tr_hit",ascending=False).to_string(index=False))
# clean-sheet gates (last 5 league, all games), compared with V4.1 picking the SAME number each weekend
print("\nCLEAN-SHEET GATES (last 5), pool size per weekend chosen by the rule, V4.1 given the same count:")
t="all5"; hcs,acs=g("h",t,"cs"),g("a",t,"cs"); goals=g("h",t,"gf")+g("h",t,"ga")+g("a",t,"gf")+g("a",t,"ga")
gates={"neither side kept a clean sheet":(hcs==0)&(acs==0),"each side 1 or fewer":(hcs<=1)&(acs<=1),"1 or fewer between them":(hcs+acs)<=1,"2 or fewer between them":(hcs+acs)<=2,
       "each side 1 or fewer + both failed to score 1 or fewer":(hcs<=1)&(acs<=1)&(g("h",t,"fts")<=1)&(g("a",t,"fts")<=1)}
base=E.ev.values
for name,m in gates.items():
    for per,msk in (("test",tst),):
        sel=np.flatnonzero(m&msk); n_wk=pd.Series(wk[sel]).value_counts()
        # V4.1 same count per weekend
        vs=[]
        for w_,cnt in n_wk.items():
            idx=np.flatnonzero((wk==w_)&msk); idx=idx[np.argsort(-E.p_v41.values[idx])][:cnt]; vs.extend(idx)
        vs=np.array(vs)
        print(f"{name:55s} test picks {len(sel):5d} ({len(sel)/len(np.unique(wk[msk])):.0f} a weekend) landed {y[sel].sum():5d} | V4.1 same count landed {y[vs].sum()}")
    # gate then top 20 by goals
    s=top(goals,20,m); a,b,c_,d=res(s); print(f"   ...gate then top 20 by goals: test {c_} of {d}")
