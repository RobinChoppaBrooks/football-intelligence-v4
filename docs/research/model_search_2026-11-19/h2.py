import pickle, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,"/home/claude/bt")
import h
from h import X, F38, C_ALL, C_L10, hgb, lr_, fitpred, num
from sklearn.ensemble import HistGradientBoostingRegressor as HGBR
from scipy.stats import poisson
import json
full=pd.read_pickle("X_all.pkl"); full=full[full.target_over25.notna()&(full.h_l5L_n>=3)&(full.a_l5L_n>=3)].copy()
full["y"]=full.target_over25.astype(int); full["is_cup"]=full.is_cup.astype(float); full["goals"]=full.ft_home+full.ft_away
X["goals"]=X.ft_home+X.ft_away
X["lgcat"]=X.league_id.astype("category").cat.codes
def poisson_model(cols):
    def f(tr,te):
        m=HGBR(loss="poisson",max_depth=3,learning_rate=0.04,max_iter=300,min_samples_leaf=80,random_state=0).fit(tr[cols].fillna(-1),tr.goals)
        lam=m.predict(te[cols].fillna(-1)); return 1-poisson.cdf(2,lam)
    return f
def more_data(cols):
    def f(tr,te):
        T=full[full.season<int(te.season.iloc[0])]
        if len(T)==0: T=full[full.season<=int(te.season.iloc[0])]
        m=hgb(); m.fit(T[cols].fillna(-1),T.y); return m.predict_proba(te[cols].fillna(-1))[:,1]
    return f
def recency(cols,w=2.0):
    def f(tr,te):
        sw=np.where(tr.season==tr.season.max(),w,1.0); m=hgb(); m.fit(tr[cols].fillna(-1),tr.y,sample_weight=sw); return m.predict_proba(te[cols].fillna(-1))[:,1]
    return f
def league_cat(cols):
    def f(tr,te):
        from sklearn.ensemble import HistGradientBoostingClassifier as HGB
        cc=cols+["lgcat"]; m=HGB(max_depth=3,learning_rate=0.04,max_iter=300,min_samples_leaf=80,l2_regularization=1.0,categorical_features=[len(cc)-1],random_state=0)
        m.fit(tr[cc].fillna(-1),tr.y); return m.predict_proba(te[cc].fillna(-1))[:,1]
    return f
def ens(fns):
    def f(tr,te):
        P=[pd.Series(fn(tr,te)).rank(pct=True).values for fn in fns]; return np.mean(P,axis=0)
    return f
A=fitpred(lambda: hgb(3,0.03,400,100),C_ALL); Lg=fitpred(lr_,F38); L10=fitpred(hgb,C_L10); Rf=fitpred(hgb,F38)
h.V={
 "V4.1 refit (same recipe)": Rf,
 "Goals-count model (Poisson), V4.1 features": poisson_model(F38),
 "Goals-count model (Poisson), all features": poisson_model(C_ALL),
 "V4.1 recipe trained on ALL leagues in database": more_data(F38),
 "All features trained on ALL leagues": more_data(C_ALL),
 "V4.1 recipe, last season weighted x2": recency(F38,2.0),
 "V4.1 recipe + league identity": league_cat(F38),
 "Ensemble: all-features + logistic + last-10": ens([A,Lg,L10]),
 "Ensemble: all-features + logistic + last-10 + V4.1 refit": ens([A,Lg,L10,Rf]),
}
res=h.run(); pickle.dump(res,open("h2_res.pkl","wb")); print("done")
