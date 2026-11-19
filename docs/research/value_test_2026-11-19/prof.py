import sys, os, json, pickle, sqlite3, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
REPO="/home/claude/football-intelligence-v4"; sys.path.insert(0, REPO); os.chdir(REPO)
from features import build
from bands import predict as band_predict
comp=json.load(open("config/competitions.json"))
leagues=[c["league_id"] for c in comp["english"]+comp["european"] if not c.get("is_cup")]
X=build("/tmp/fdb.db"); X=X[(X.season==2026)&X.target_over25.notna()].copy()
bb=pickle.load(open("bands_model.pkl","rb")); X["p"]=band_predict(bb,X)
thin=(X.h_l5L_n.fillna(0)<3)|(X.a_l5L_n.fillna(0)<3)
X["band"]=np.where(thin,"rejected",np.where(X.p>=bb["green"],"High",np.where(X.p>=bb["amber"],"Medium","rejected")))
c=sqlite3.connect("/tmp/fdb.db")
o=pd.read_sql("select fixture_id,bookmaker,over25,fetched_at from fixture_odds",c)
b365=o[o.bookmaker=="Bet365"].groupby("fixture_id").over25.last().rename("b365")
pin=o[o.bookmaker=="Pinnacle"].groupby("fixture_id").over25.last().rename("pin")
best=o.groupby("fixture_id").over25.max().rename("best")
X=X.join(b365,on="fixture_id").join(pin,on="fixture_id").join(best,on="fixture_id")
X=X[X.b365.notna()].copy(); X["league"]=X.league_id.isin(leagues)
X[["fixture_id","league_id","league","kickoff_utc","p","band","target_over25","b365","pin","best"]+[c for c in X.columns if c.startswith(("h_l5L","a_l5L"))]].to_pickle("/home/claude/bt/x2026.pkl")
print(len(X), X.league.sum(), X.kickoff_utc.min(), X.kickoff_utc.max())
