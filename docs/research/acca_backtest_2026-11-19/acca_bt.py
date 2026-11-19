import sys, os, json, pickle, numpy as np, pandas as pd
REPO="/home/claude/football-intelligence-v4"; sys.path.insert(0, REPO); os.chdir(REPO)
from features import build
from bands import predict as band_predict
comp=json.load(open("config/competitions.json"))
leagues=[c["league_id"] for c in comp["english"]+comp["european"] if not c.get("is_cup")]
X=build(sys.argv[1]); X=X[X.league_id.isin(leagues) & X.target_over25.notna()].copy()
bb=pickle.load(open("bands_model.pkl","rb")); X["p"]=band_predict(bb,X)
cnt=lambda c: np.rint(5*X[c])
full=(X.h_l5L_n>=5)&(X.a_l5L_n>=5)
trump=full&(cnt("h_l5L_gf2")>=4)&(cnt("a_l5L_gf2")>=4)&(cnt("h_l5L_ga2")<=1)&(cnt("a_l5L_ga2")<=1)
thin=(X.h_l5L_n.fillna(0)<3)|(X.a_l5L_n.fillna(0)<3)
X["sel"]=(~thin)&((X.p>=bb["amber"])|trump)
k=X.kickoff_utc.dt.tz_convert("Europe/London"); X["dow"]=k.dt.weekday
X=X[X.dow>=4]  # Fri, Sat, Sun
X["wk"]=(k - pd.to_timedelta(X.dow-4, unit="D")).dt.date  # Friday of that weekend
X=X[X.sel]
rng=np.random.default_rng(7); rows=[]
for (season,wk),g in X.groupby(["season","wk"]):
    g=g.sort_values("p",ascending=False); y=g.target_over25.values.astype(int); N=len(g); W=int(y.sum())
    r=dict(season=int(season),wk=str(wk),pool=N,landed=W)
    if N<20: r.update(bet=False); rows.append(r); continue
    r["bet"]=True
    t20=y[:20]; r["top20_all"]=int(t20.all())
    groups=[t20[[i for i in range(20) if (i//4)%2==0 and i%4==j or (i//4)%2==1 and i%4==3-j]] for j in range(4)]  # snake 4 groups of 5
    r["groups_landed"]=int(sum(gr.all() for gr in groups))
    wins=0
    for _ in range(100):
        idx=rng.choice(N,20,replace=False); wins+=int(y[idx].all())
    r["random_tickets_won"]=wins
    from math import comb
    r["p_ticket"]=comb(W,20)/comb(N,20) if W>=20 else 0.0
    rows.append(r)
R=pd.DataFrame(rows); R.to_csv("/home/claude/bt/acca_weeks.csv",index=False)
lab={2023:"2023-24",2024:"2024-25",2025:"2025-26",2026:"2026-27"}
for s,g in R.groupby("season"):
    b=g[g.bet]
    print(f"\n{lab[s]}: weekends {len(g)}, with 20+ selected {len(b)}; pool size {int(b.pool.min())} to {int(b.pool.max())}")
    print(f"  random 100 x 20-folds: weekends with >=1 winning ticket {int((b.random_tickets_won>0).sum())}, winning tickets total {int(b.random_tickets_won.sum())} of {100*len(b)}; expected weekends with a hit {round(float((1-(1-b.p_ticket)**100).sum()),2)}")
    print(f"  weekends where 20+ pool fixtures landed {int((b.landed>=20).sum())}")
    print(f"  top 20 as one 20-fold: landed {int(b.top20_all.sum())} of {len(b)}")
    vc=b.groups_landed.value_counts().sort_index().to_dict(); print(f"  4 groups of 5 (top 20): weekends by groups landed {vc}")
    top=b.copy(); 
    print("  top 20 legs landed per weekend, min/most common/max:", int(b.apply(lambda r:0,axis=1).sum()) if False else "")
