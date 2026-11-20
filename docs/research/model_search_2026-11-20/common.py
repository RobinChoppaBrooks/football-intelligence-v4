import json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
R="/home/claude/fi4"
cfg=json.load(open(f"{R}/config/model_config.json")); F38=cfg["selection_engine"]["features"]
comp=json.load(open(f"{R}/config/competitions.json")); allc=comp["english"]+comp["european"]
LEAG=[c["league_id"] for c in allc if not c.get("is_cup")]; ALL=[c["league_id"] for c in allc]
def load():
    X=pd.read_pickle("/home/claude/bt/X_all.pkl"); X=X[X.league_id.isin(ALL)&X.target_over25.notna()].copy()
    X=X[(X.h_l5L_n>=3)&(X.a_l5L_n>=3)].copy(); X["y"]=X.target_over25.astype(int)
    k=pd.to_datetime(X.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); X["dow"]=k.dt.weekday
    X["wk"]=(k-pd.to_timedelta((X.dow-4)%7,unit="D")).dt.date
    X["ev"]=X.league_id.isin(LEAG)&(X.dow>=4)
    return X
def topk(d,s,K=20):
    t=d.assign(s=s).sort_values(["wk","s","fixture_id"],ascending=[True,False,True]).groupby("wk").head(K); return t
def hits(d,s,K=20):
    t=topk(d,s,K); return int(t.y.sum()), len(t)
