import pandas as pd, numpy as np, json
from sklearn.linear_model import LogisticRegression
D=pd.read_pickle("D.pkl")
print("pin coverage by season", D.groupby("season").q_pin.apply(lambda s: int(s.notna().sum())).to_dict(), "avg", D.groupby("season").q_avg.apply(lambda s:int(s.notna().sum())).to_dict())
lg=lambda p: np.log(np.clip(p,1e-4,1-1e-4)/(1-np.clip(p,1e-4,1-1e-4)))
for s in (2025,2026):
    g=D[(D.season==s)&D.q_avg.notna()&D.p_v41.notna()&(D.h_l5L_n>=3)&(D.a_l5L_n>=3)]
    A=np.c_[lg(g.q_avg),lg(g.p_v41)]
    m=LogisticRegression(C=1e6).fit(A,g.y); m1=LogisticRegression(C=1e6).fit(A[:,:1],g.y)
    from sklearn.metrics import log_loss
    print(s,len(g),"coef market, v41:",m.coef_.round(3),"logloss market-only",round(log_loss(g.y,m1.predict_proba(A[:,:1])[:,1]),5),"with v41",round(log_loss(g.y,m.predict_proba(A)[:,1]),5),
          "| raw market",round(log_loss(g.y,g.q_avg),5),"v41",round(log_loss(g.y,g.p_v41),5))
# correlation
g=D[D.season>=2025]; print("corr q_avg vs p_v41", round(g[["q_avg","p_v41"]].corr().iloc[0,1],3))
