import pandas as pd, numpy as np, json
from sklearn.ensemble import HistGradientBoostingClassifier
D=pd.read_pickle("D.pkl"); cfg=json.load(open("/home/claude/football-intelligence-v4/config/model_config.json"))
F=[f for f in cfg["selection_engine"]["features"] if f in D.columns]
D=D[D.b365_o.notna()&D.b365c_o.notna()&D.avg_o.notna()&D.q_avg.notna()].copy()
D["short"]=(D.b365c_o<D.b365_o).astype(int)
D["d_b365_avg"]=D.b365_o/D.avg_o; D["d_max_avg"]=D.max_o/D.avg_o; D["d_b365_max"]=D.b365_o/D.max_o
D["d_q"]=D.q_b365-D.q_avg; D["v41_gap"]=D.p_v41-D.q_avg; D["lgc"]=D.fd_code.astype("category").cat.codes
D["dow"]=pd.to_datetime(D.kickoff_utc).dt.weekday
mk=["b365_o","b365_u","avg_o","avg_u","max_o","max_u","q_avg","q_b365","q_b365_margin","d_b365_avg","d_max_avg","d_b365_max","d_q","v41_gap","p_v41","lgc","dow"]
sets={"market only":mk,"market+form":mk+F}
res=[]
for name,cols in sets.items():
    for test in (2024,2025,2026):
        tr=D[D.season<test]; te=D[D.season==test].copy()
        m=HistGradientBoostingClassifier(max_depth=3,learning_rate=0.03,max_iter=300,min_samples_leaf=100,random_state=0).fit(tr[cols],tr.short)
        te["ps"]=m.predict_proba(te[cols])[:,1]
        from sklearn.metrics import roc_auc_score
        auc=roc_auc_score(te.short,te.ps)
        for q in (0.5,0.6,0.7,0.8,0.9):
            cut=np.quantile(te.ps,q) if False else np.quantile(tr.assign(ps=m.predict_proba(tr[cols])[:,1]).ps,q)
            s=te[te.ps>=cut]; pl=s.b365_o*s.y-1
            res.append((name,test,round(auc,3),q,len(s),int(s.y.sum()),round(pl.sum(),1),round(pl.mean()*100,1)))
R=pd.DataFrame(res,columns=["features","test season","AUC shorten","top share cut (train quantile)","bets","hits","PL units","per 100"])
print(R.to_string(index=False))
D.to_pickle("D2.pkl")
