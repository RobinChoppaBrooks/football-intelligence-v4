import sqlite3, numpy as np, pandas as pd
from common import *
c=sqlite3.connect("/tmp/live.db")
F=pd.read_sql("select fixture_id,league_id,kickoff_utc,home_id,away_id,status from fixtures where status not in ('PST','CANC','ABD','TBD')",c)
F["ko"]=pd.to_datetime(F.kickoff_utc,utc=True)
EUR={2,3,848}
L=pd.concat([F.assign(team=F.home_id),F.assign(team=F.away_id)])[["fixture_id","team","ko","league_id"]].sort_values(["team","ko"])
L["eur"]=L.league_id.isin(EUR)
g=L.groupby("team")
L["prev_ko"]=g.ko.shift(1); L["next_ko"]=g.ko.shift(-1); L["prev_eur"]=g.eur.shift(1).fillna(False)
L["rest"]=(L.ko-L.prev_ko).dt.total_seconds()/86400; L["to_next"]=(L.next_ko-L.ko).dt.total_seconds()/86400
def last_n_days(df,days):
    out=np.zeros(len(df),int); ko=df.ko.values
    for t,idx in df.groupby("team").indices.items():
        k=ko[idx]; lo=np.searchsorted(k,k-np.timedelta64(days,"D"),side="left"); out[idx]=np.arange(len(idx))-lo
    return out
L=L.reset_index(drop=True); L["g14"]=last_n_days(L,14); L["g21"]=last_n_days(L,21)
L["eur_before"]=L.prev_eur&(L.rest<=4.5)
X=load()
for side,col in (("h","home_id"),("a","away_id")):
    m=L.rename(columns={c_:f"{side}_{c_}" for c_ in ["rest","to_next","g14","g21","eur_before"]})
    X=X.merge(m[["fixture_id","team"]+[f"{side}_{c_}" for c_ in ["rest","to_next","g14","g21","eur_before"]]],left_on=["fixture_id",col],right_on=["fixture_id","team"],how="left").drop(columns="team")
X["min_rest"]=X[["h_rest","a_rest"]].min(axis=1); X["max_rest"]=X[["h_rest","a_rest"]].max(axis=1)
X["rest_gap"]=(X.h_rest-X.a_rest); X["g14_sum"]=X.h_g14+X.a_g14; X["eur_any"]=(X.h_eur_before|X.a_eur_before)
X["after_break"]=(X.min_rest>=11)
X.to_pickle("/home/claude/bt/X_rest.pkl")
