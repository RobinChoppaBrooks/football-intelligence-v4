import sys; sys.path.insert(0,"/home/claude/bt")
import pickle, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
import h
from h import X, F38, C_ALL, C_L10, hgb, lr_
full=pd.read_pickle("X_all.pkl"); full=full[full.target_over25.notna()&(full.h_l5L_n>=3)&(full.a_l5L_n>=3)].copy()
full["y"]=full.target_over25.astype(int); full["is_cup"]=full.is_cup.astype(float)
def md(model,cols):
    def f(tr,te):
        s=int(te.season.iloc[0]); T=full[full.season<s]
        if len(T)==0: T=full[full.season<=s]
        m=model(); m.fit(T[cols].fillna(-1),T.y); return m.predict_proba(te[cols].fillna(-1))[:,1]
    return f
def ens(fns):
    def f(tr,te): return np.mean([pd.Series(fn(tr,te)).rank(pct=True).values for fn in fns],axis=0)
    return f
A=md(lambda: hgb(3,0.03,400,100),C_ALL); Lg=md(lr_,F38); L10=md(hgb,C_L10); Rf=md(hgb,F38)
h.V={"V4.1 locked (as published)": lambda tr,te: te.p_v41.values,
     "V4.1 refit (same recipe)": h.fitpred(hgb,F38),
     "Blend of 4, trained on ALL leagues": ens([A,Lg,L10,Rf]),
     "Blend of 3 (no V4.1 refit), ALL leagues": ens([A,Lg,L10])}
res=h.run(); pickle.dump(res,open("h3_res.pkl","wb")); print("done")
