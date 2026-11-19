import json, re, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from sklearn.ensemble import HistGradientBoostingClassifier as HGB, RandomForestClassifier as RF
from sklearn.linear_model import LogisticRegression as LR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
R="/home/claude/football-intelligence-v4"
cfg=json.load(open(f"{R}/config/model_config.json")); F38=cfg["selection_engine"]["features"]
comp=json.load(open(f"{R}/config/competitions.json")); allc=comp["english"]+comp["european"]
LEAG=[c["league_id"] for c in allc if not c.get("is_cup")]; ALL=[c["league_id"] for c in allc]
X=pd.read_pickle("X_all.pkl"); X=X[X.league_id.isin(ALL)&X.target_over25.notna()].copy()
X=X[(X.h_l5L_n>=3)&(X.a_l5L_n>=3)].copy(); X["y"]=X.target_over25.astype(int); X["is_cup"]=X.is_cup.astype(float)
k=pd.to_datetime(X.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); X["dow"]=k.dt.weekday
X["wk"]=(k-pd.to_timedelta((X.dow-4)%7,unit="D")).dt.date
X["ev"]=X.league_id.isin(LEAG)&(X.dow>=4)
num=[c for c in X.columns if X[c].dtype.kind in "fi" and c not in ("y","target_over25","target_btts","ft_home","ft_away","ht_home","ht_away","fixture_id","home_id","away_id","h_team_id","a_team_id","p_v41","dow","season","league_id")]
CNT=("gf2","ga2","gf3","ga3","over25","btts","cs","fts","tot4","n")
def cols(prefixes,counts_only=False,extra=()):
    out=[c for c in num if re.match(r"^(h|a)_("+"|".join(prefixes)+r")_",c) and (not counts_only or c.rsplit("_",1)[-1] in CNT)]
    return out+[e for e in extra if e in num]
C_L5L=cols(["l5L","v3L"],True,("lg_o25","lg_btts","lg_n","is_cup"))
C_ALLW=cols(["l5L","v3L","l5","l10","l5_v","std_v"],True,("lg_o25","lg_btts","lg_n","is_cup"))
C_XG=F38+[c for c in num if c.startswith("m_")]+cols(["l5","l10"],False)[:0]+[c for c in num if re.match(r"^(h|a)_l5_(xg|shots)",c)]
C_L10=[c.replace("l5L","l10") for c in F38 if c.replace("l5L","l10") in num]+[c for c in F38 if not c.startswith(("h_l5L","a_l5L"))]
C_ALL=num
print("features: F38",len(F38),"count-only",len(C_L5L),"count all windows",len(C_ALLW),"xg",len(C_XG),"l10",len(C_L10),"all",len(C_ALL))
hgb=lambda d=3,lr=0.04,it=300,leaf=80: HGB(max_depth=d,learning_rate=lr,max_iter=it,min_samples_leaf=leaf,l2_regularization=1.0,random_state=0)
lr_=lambda: make_pipeline(StandardScaler(),LR(C=0.5,max_iter=3000))
def fitpred(model,cols_):
    def f(tr,te):
        m=model(); m.fit(tr[cols_].fillna(-1),tr.y); return m.predict_proba(te[cols_].fillna(-1))[:,1]
    return f
def rule(fn): return lambda tr,te: fn(te).values+1e-4*te.lg_o25.fillna(0).values
c5=lambda d,s,c: d[f"{s}_l5L_{c}"]
V={
 "V4.1 locked (as published)": lambda tr,te: te.p_v41.values,
 "V4.1 refit (same recipe)": fitpred(hgb,F38),
 "Rule: Scored2+ + Let in2+ (4 counts)": rule(lambda d: c5(d,"h","gf2")+c5(d,"h","ga2")+c5(d,"a","gf2")+c5(d,"a","ga2")),
 "Rule: two routes (min attack v defence)": rule(lambda d: np.minimum(c5(d,"h","gf2"),c5(d,"a","ga2"))+np.minimum(c5(d,"a","gf2"),c5(d,"h","ga2"))),
 "Rule: 3+ games both sides": rule(lambda d: c5(d,"h","over25")+c5(d,"a","over25")),
 "Rule: 3+ games + division rate": rule(lambda d: c5(d,"h","over25")+c5(d,"a","over25")+2*d.lg_o25),
 "Rule: 4 counts + 3+ games": rule(lambda d: c5(d,"h","gf2")+c5(d,"h","ga2")+c5(d,"a","gf2")+c5(d,"a","ga2")+c5(d,"h","over25")+c5(d,"a","over25")),
 "Rule: 3+ games last 10 + division": rule(lambda d: d.h_l10_over25+d.a_l10_over25+2*d.lg_o25),
 "HGB counts only (no averages)": fitpred(hgb,C_L5L),
 "Logistic counts only": fitpred(lr_,C_L5L),
 "Logistic V4.1 features": fitpred(lr_,F38),
 "HGB counts, all windows": fitpred(hgb,C_ALLW),
 "HGB V4.1 + xG and shots": fitpred(hgb,C_XG),
 "HGB V4.1 on last-10 window": fitpred(hgb,C_L10),
 "HGB all 300+ features": fitpred(lambda: hgb(3,0.03,400,100),C_ALL),
 "HGB depth 2": fitpred(lambda: hgb(2),F38),
 "HGB depth 5": fitpred(lambda: hgb(5,0.03,300,150),F38),
 "HGB slow 800 iters": fitpred(lambda: hgb(3,0.015,800,100),F38),
 "Random forest V4.1 features": fitpred(lambda: RF(400,min_samples_leaf=60,max_features=0.4,n_jobs=-1,random_state=0),F38),
 "Random forest counts all windows": fitpred(lambda: RF(400,min_samples_leaf=60,max_features=0.4,n_jobs=-1,random_state=0),C_ALLW),
}
def run(names=None):
    res={}
    for name,f in V.items():
        if names and name not in names: continue
        parts=[]
        for test in (2024,2025,2026):
            tr=X[X.season<test]; te=X[(X.season==test)&X.ev].copy()
            te["s"]=f(tr,te)
            # threshold mode: cut chosen on the last training season so it averaged >= 20 picks a weekend
            va=X[(X.season==test-1)&X.ev].copy(); trv=X[X.season<test-1]
            va["s"]=f(trv if len(trv) else tr, va) if name!="V4.1 locked (as published)" else va.p_v41.values
            cut=None
            for q in np.linspace(0.99,0.5,99):
                c=np.quantile(va.s,q)
                if (va.s>=c).groupby(va.wk).sum().mean()>=20: cut=c; break
            te["cut"]=cut; parts.append(te[["fixture_id","season","wk","y","s","cut"]])
        res[name]=pd.concat(parts)
    return res
if __name__=="__main__":
    import pickle; res=run(); pickle.dump(res,open("h_res.pkl","wb")); print("done",len(res))
