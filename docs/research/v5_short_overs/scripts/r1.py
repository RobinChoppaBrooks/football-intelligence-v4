import pandas as pd, numpy as np
X=pd.read_pickle("X_all.pkl"); P=pd.read_pickle("prices_hist.pkl")
D=X.merge(P,on="fixture_id",how="inner"); D["y"]=D.target_over25.astype(int)
# de-vig Pinnacle (opening-ish) and closing
for a,b,n in (("pin_o","pin_u","q_pin"),("pinc_o","pinc_u","q_pinc"),("b365_o","b365_u","q_b365"),("avg_o","avg_u","q_avg")):
    io,iu=1/D[a],1/D[b]; D[n]=io/(io+iu); D[n+"_margin"]=io+iu-1
D.to_pickle("D.pkl"); print(len(D), D.season.value_counts().sort_index().to_dict())
print("margins b365", round(D.q_b365_margin.median(),3), "pin", round(D.q_pin_margin.median(),3), "avg", round(D.q_avg_margin.median(),3))
def pl(price,y): return (price*y-1)
rows=[]
for s,g in D.groupby("season"):
    for side,col,yy in (("Over b365","b365_o",g.y),("Over max","max_o",g.y),("Over closing b365","b365c_o",g.y),("Under b365","b365_u",1-g.y),("Under max","max_u",1-g.y)):
        m=g[col].notna(); rows.append((s,side,int(m.sum()),round(float(pl(g.loc[m,col],yy[m]).sum()),1),round(float(pl(g.loc[m,col],yy[m]).mean())*100,1)))
print(pd.DataFrame(rows,columns=["season","bet","n","PL units","PL per 100"]).to_string(index=False))
# calibration of de-vigged pinnacle
D["b"]=pd.cut(D.q_pin,[0,.4,.45,.5,.55,.6,.65,.7,.75,1])
print(D.groupby("b",observed=True).agg(n=("y","size"),q=("q_pin","mean"),hit=("y","mean")).round(3))
