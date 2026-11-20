import sqlite3, numpy as np, pandas as pd, itertools
from common import *
c=sqlite3.connect("/tmp/live.db")
comp=pd.read_sql("select league_id,is_cup from competitions",c); LG=set(comp[comp.is_cup==0].league_id)
F=pd.read_sql("select fixture_id,league_id,season,kickoff_utc,home_id,away_id,status,ft_home,ft_away from fixtures",c)
F=F[F.league_id.isin(LG)].copy(); F["ko"]=pd.to_datetime(F.kickoff_utc,utc=True)
done=F.status.isin(["FT","AET","PEN"])&F.ft_home.notna()
H=F.assign(team=F.home_id,venue="h",gf=F.ft_home,ga=F.ft_away); A=F.assign(team=F.away_id,venue="a",gf=F.ft_away,ga=F.ft_home)
L=pd.concat([H,A])[["fixture_id","season","team","venue","ko","gf","ga","status"]].sort_values(["team","ko","fixture_id"]).reset_index(drop=True)
L["fin"]=L.status.isin(["FT","AET","PEN"])&L.gf.notna()
L["cs"]=(L.ga==0).astype(float); L["fts"]=(L.gf==0).astype(float); L["o3"]=((L.gf+L.ga)>=3).astype(float)
for m in ("gf","ga","cs","fts","o3"): L[m]=L[m].where(L.fin)
def roll(df,keys,N,tag):
    out={}
    G=df[df.fin].groupby(keys)
    for m in ("gf","ga","cs","fts","o3"):
        out[f"{tag}{N}_{m}"]=G[m].transform(lambda s: s.shift(1).rolling(N,min_periods=1).sum())
    return pd.DataFrame(out,index=df[df.fin].index)
feats=[]
for N in (3,4,5,6,8,10):
    feats.append(roll(L,["team","season"],N,"all"))
    feats.append(pd.concat([roll(L[L.venue==v],["team","season","venue"],N,"ven") for v in ("h","a")]))
R=pd.concat([L[["fixture_id","team","venue"]]]+[f.reindex(L.index) for f in feats],axis=1)
# need features for upcoming too? eval uses finished fixtures only, so finished rows suffice
X=load(); E=X[X.ev].copy()
for side,col in (("h","home_id"),("a","away_id")):
    r=R[R.venue==side].drop(columns="venue"); r.columns=["fixture_id","team"]+[f"{side}_{c_}" for c_ in r.columns[2:]]
    E=E.merge(r,left_on=["fixture_id",col],right_on=["fixture_id","team"],how="left").drop(columns="team")
E.to_pickle("/home/claude/bt/E_last5.pkl"); print(E.shape, E["h_all5_gf"].isna().sum())
