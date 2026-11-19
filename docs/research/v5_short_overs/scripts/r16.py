import pandas as pd, numpy as np, sqlite3
D=pd.read_pickle("D.pkl"); D=D[D.q_avg.notna()&D.b365_o.notna()].copy()
k=pd.to_datetime(D.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); D=D[k.dt.weekday>=4].copy(); k=k[D.index]
D["wk"]=(k-pd.to_timedelta(k.dt.weekday-4,unit="D")).dt.date
B={3:.05,5:.10,8:.20,10:.30}
PORT=[("treble",3,3,15.0,0.60,"value"),("5-fold",5,2,10.0,0.60,"value"),("8-fold",8,1,5.0,0.60,"shortest"),("10-fold",10,1,5.0,0.55,"shortest")]
def run(pricecol,qcol="q_avg"):
    pl=[]; 
    for wk,g in D[D[pricecol].notna()&D[qcol].notna()].groupby("wk"):
        st=ret=0
        for nm,n,cnt,stake,minp,rank in PORT:
            t=g[(g[qcol]>=minp)&(g[pricecol]>=1.10)]
            t=t.assign(v=t[qcol]*t[pricecol] if rank=="value" else t[qcol]).sort_values("v",ascending=False)
            for i in range(cnt):
                L=t.iloc[i*n:(i+1)*n]
                if len(L)<n: continue
                O=float(np.prod(L[pricecol])); st+=stake
                if L.y.all(): ret+=stake*(1+(O-1)*(1+B[n]))
        pl.append((int(g.season.iloc[0]),st,ret-st))
    P=pd.DataFrame(pl,columns=["s","st","pl"]); return {s:int(g.pl.sum()) for s,g in P.groupby("s")}, int(P.pl.sum()), int(P.st.sum())
D["worst_o"]=D[["b365_o","b365c_o"]].min(axis=1)
print("bet at Bet365 pre-match (Friday) price:", run("b365_o"))
print("bet at Bet365 closing price:           ", run("b365c_o"))
print("bet at the WORSE of the two:           ", run("worst_o"))
print("selector from closing consensus, closing price:", run("b365c_o","q_avgc"))
# live reproduction: API 8-bookmaker de-vig average vs football-data average, same fixtures
c=sqlite3.connect("/tmp/fdb.db"); o=pd.read_sql("select fixture_id,bookmaker,over25,under25 from fixture_odds where over25>1 and under25>1",c)
o["qo"]=(1/o.over25)/((1/o.over25)+(1/o.under25)); a=o.groupby("fixture_id").qo.mean().rename("q_api")
m=D.join(a,on="fixture_id"); m=m[m.q_api.notna()]
print("overlap fixtures",len(m),"corr q_api vs q_avg",round(m[["q_api","q_avg"]].corr().iloc[0,1],4),"mean abs diff",round((m.q_api-m.q_avg).abs().mean(),4))
print("agreement on q>=0.60:", int(((m.q_api>=.6)==(m.q_avg>=.6)).sum()),"of",len(m))
