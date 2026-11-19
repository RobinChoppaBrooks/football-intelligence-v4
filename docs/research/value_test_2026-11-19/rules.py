import pandas as pd, numpy as np
X=pd.read_pickle("x2026.pkl"); y=X.target_over25.astype(int)
X["edge"]=X.p*X.b365
rng=np.random.default_rng(1)
def row(name,m,price="b365"):
    s=X[m]; n=len(s)
    if n==0: return (name,0,0,0,0,"")
    ret=(s[price]*s.target_over25).values; pl=ret-1
    bs=[rng.choice(pl,n).sum() for _ in range(2000)]
    return (name,n,int(s.target_over25.sum()),round(s[price].median(),2),round(pl.sum(),1),f"{round(np.percentile(bs,5),1)} to {round(np.percentile(bs,95),1)}")
L=X.league
R=[row("all fixtures",L), row("selected (High+Medium)",L&(X.band!="rejected")), row("High",L&(X.band=="High")),
   row("Medium",L&(X.band=="Medium")), row("rejected",L&(X.band=="rejected")),
   row("value p x price >= 1.00",L&(X.edge>=1.0)&(X.band!="rejected")|L&(X.edge>=1.0)&(X.band=="rejected")),
   row("value >= 1.05",L&(X.edge>=1.05)), row("value >= 1.10",L&(X.edge>=1.10)),
   row("selected and price >= 1.51",L&(X.band!="rejected")&(X.b365>=1.51)),
   row("selected and value >= 1.00",L&(X.band!="rejected")&(X.edge>=1.0)),
   row("selected and value >= 1.05",L&(X.band!="rejected")&(X.edge>=1.05)),
   row("selected at BEST price",L&(X.band!="rejected"),"best"),
   row("selected, value>=1.05 at best price",L&(X.band!="rejected")&(X.p*X.best>=1.05),"best")]
print(pd.DataFrame(R,columns=["rule","bets","hits","median price","P/L per £1 units","90% range"]).to_string(index=False))
# market vs model accuracy
s=X[L&X.pin.notna()]; imp=1/s.pin
# normalise pinnacle approx: over+under not available here; use raw
print("Brier model",round(((s.p-s.target_over25)**2).mean(),4),"Brier Pinnacle raw implied",round(((imp-s.target_over25)**2).mean(),4), "n",len(s))
s=X[L]; print("Brier model",round(((s.p-s.target_over25)**2).mean(),4),"Brier Bet365 implied",round(((1/s.b365-s.target_over25)**2).mean(),4))
print("selected: mean model p",round(X[L&(X.band!='rejected')].p.mean(),3),"mean Bet365 implied",round((1/X[L&(X.band!='rejected')].b365).mean(),3),"actual",round(X[L&(X.band!='rejected')].target_over25.mean(),3))
