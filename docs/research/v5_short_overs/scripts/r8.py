import pandas as pd, numpy as np, re
D=pd.read_pickle("D2.pkl")
D["round_no"]=D.groupby(["fd_code","season","home_id"]).kickoff_utc.rank()  # approx home game number
k=pd.to_datetime(D.kickoff_utc,utc=True).dt.tz_convert("Europe/London"); D["month"]=k.dt.month; D["mid"]=k.dt.weekday.isin([1,2,3])
D["qa_band"]=pd.cut(D.q_avg,[0,.42,.46,.5,.54,.58,.62,.66,1])
D["h_ga2"]=np.rint(D.h_l5L_ga2*5); D["a_ga2"]=np.rint(D.a_l5L_ga2*5); D["h_gf2"]=np.rint(D.h_l5L_gf2*5); D["a_gf2"]=np.rint(D.a_l5L_gf2*5)
D["leaky"]=(D.h_ga2+D.a_ga2); D["attack"]=(D.h_gf2+D.a_gf2)
D["v41_sel"]=(D.p_v41>=0.5808)
D["early"]=D.month.isin([8,9]); D["late"]=D.month.isin([4,5])
segs={"league":"fd_code","market band":"qa_band","midweek":"mid","early season":"early","late season":"late","leaky sum (0-10)":"leaky","attack sum (0-10)":"attack","V4.1 selected":"v41_sel"}
rows=[]
for lab,col in segs.items():
    for v,g in D.groupby(col,observed=True):
        for side,price,y in (("Over","max_o",g.y),("Over","b365_o",g.y),("Under","max_u",1-g.y),("Under","b365_u",1-g.y)):
            pl=g[price]*y-1; per={s:pl[g.season==s].sum() for s in (2023,2024,2025,2026)}; n={s:int((g.season==s).sum()) for s in (2023,2024,2025,2026)}
            if min(n[2023],n[2024],n[2025])<60: continue
            cons=all(per[s]>0 for s in (2023,2024,2025))
            rows.append((lab,str(v),side,price,n[2023]+n[2024]+n[2025],round(per[2023],1),round(per[2024],1),round(per[2025],1),cons,n[2026],round(per[2026],1)))
R=pd.DataFrame(rows,columns=["segment","value","side","price","n 23-26","PL 23","PL 24","PL 25","positive all 3","n 26","PL 26 (hold-out)"])
print("segments tested:",len(R)); print(R[R["positive all 3"]].to_string(index=False))
R.to_csv("segments.csv",index=False)
