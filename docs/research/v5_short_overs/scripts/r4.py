import pandas as pd, numpy as np, json
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
D=pd.read_pickle("D.pkl"); cfg=json.load(open("/home/claude/football-intelligence-v4/config/model_config.json"))
F=[f for f in cfg["selection_engine"]["features"] if f in D.columns]
lg=lambda p: np.log(np.clip(p,1e-4,1-1e-4)/(1-np.clip(p,1e-4,1-1e-4)))
D=D[D.q_avg.notna()&(D.h_l5L_n>=3)&(D.a_l5L_n>=3)].copy(); D["mk"]=lg(D.q_avg)
D["lg_code"]=D.fd_code.astype("category").cat.codes
print(len(F),"features; rows",len(D))
out=[]
for test in (2024,2025,2026):
    tr=D[D.season<test]; te=D[D.season==test].copy()
    # A: logistic on market only (recalibration)
    a=LogisticRegression(C=1e6).fit(tr[["mk"]],tr.y); te["pA"]=a.predict_proba(te[["mk"]])[:,1]
    # B: GBM features + market + league
    cols=F+["mk","lg_code"]
    b=HistGradientBoostingClassifier(max_depth=3,learning_rate=0.03,max_iter=300,min_samples_leaf=100,l2_regularization=1.0,random_state=0).fit(tr[cols],tr.y)
    te["pB"]=b.predict_proba(te[cols])[:,1]
    # C: residual logistic: market + a few count features
    sm=["mk","h_l5L_gf2","h_l5L_ga2","a_l5L_gf2","a_l5L_ga2","h_l5L_over25","a_l5L_over25"]
    c=LogisticRegression(C=1.0,max_iter=2000).fit(tr[sm].fillna(0),tr.y); te["pC"]=c.predict_proba(te[sm].fillna(0))[:,1]
    print(test,len(te),"logloss market",round(log_loss(te.y,te.q_avg),5),"A",round(log_loss(te.y,te.pA),5),"B",round(log_loss(te.y,te.pB),5),"C",round(log_loss(te.y,te.pC),5))
    out.append(te)
T=pd.concat(out); T.to_pickle("T.pkl")
