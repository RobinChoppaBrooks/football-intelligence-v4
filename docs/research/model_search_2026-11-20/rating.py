# Dynamic attack/defence goal ratings (online Poisson, time-decayed via learning rate). Prediction made BEFORE each match updates the ratings.
import sqlite3, numpy as np, pandas as pd
from scipy.stats import poisson
from common import *
c=sqlite3.connect("/tmp/live.db")
F=pd.read_sql("select fixture_id,league_id,season,kickoff_utc,home_id,away_id,status,ft_home,ft_away from fixtures",c)
F=F[F.league_id.isin(LEAG)].copy(); F["ko"]=pd.to_datetime(F.kickoff_utc,utc=True); F=F.sort_values(["ko","fixture_id"])
FIN=F.status.isin(["FT","AET","PEN"])&F.ft_home.notna()
def run(lr=0.05, carry=0.7, homeadv=True, lr_mu=0.005):
    out={}
    for lg,G in F.groupby("league_id"):
        att={}; de={}; mu=np.log(1.35); ha=0.2 if homeadv else 0.0; last={}
        for r in G.itertuples():
            h,a=r.home_id,r.away_id
            for t in (h,a):
                if t not in att: att[t]=0.0; de[t]=0.0; last[t]=r.season
                if last[t]!=r.season: att[t]*=carry; de[t]*=carry; last[t]=r.season
            lh=np.exp(mu+ha+att[h]+de[a]); la=np.exp(mu+att[a]+de[h])
            out[r.fixture_id]=(lh,la)
            if not (r.status in ("FT","AET","PEN") and r.ft_home==r.ft_home): continue
            eh=r.ft_home-lh; ea=r.ft_away-la
            att[h]+=lr*eh; de[a]+=lr*eh; att[a]+=lr*ea; de[h]+=lr*ea
            mu+=lr_mu*(eh+ea)/2
            if homeadv: ha+=lr_mu*(eh-ea)/2
    P=pd.DataFrame.from_dict(out,orient="index",columns=["lh","la"]); P["p3"]=1-poisson.cdf(2,P.lh+P.la)
    P["pmin"]=np.minimum(P.lh,P.la); return P
if __name__=="__main__":
    X=load(); E=X[X.ev].set_index("fixture_id")
    rows=[]
    for lr in (0.02,0.035,0.05,0.08,0.12):
        for carry in (0.5,0.8,1.0):
            P=run(lr,carry); d=E.join(P,how="inner").reset_index()
            r=dict(lr=lr,carry=carry)
            for s in (2023,2024,2025,2026):
                q=d[d.season==s]; r[s]=hits(q,q.p3.values)[0]
            rows.append(r); print(r,flush=True)
    pd.DataFrame(rows).to_csv("rating_grid.csv",index=False)
