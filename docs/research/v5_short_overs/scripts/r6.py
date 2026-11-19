import pandas as pd, numpy as np
D=pd.read_pickle("D.pkl")
def rep(lab,m,price,y):
    pl=(D[price]*y-1)[m]; s=D.season[m]
    print(f"{lab:55s}", " | ".join(f"{yr}: {int((s==yr).sum())} {pl[s==yr].sum():+.1f}" for yr in (2023,2024,2025,2026)), f"|| all {int(m.sum())} {pl.sum():+.1f} ({pl.mean()*100 if m.sum() else 0:+.1f}/100)")
yo,yu=D.y,1-D.y
for th in (0.0,0.02,0.04,0.06):
    rep(f"Over: B365 price x Pinnacle fair >= {1+th}", D.b365_o.notna()&D.q_pin.notna()&(D.b365_o*D.q_pin>=1+th),"b365_o",yo)
    rep(f"Under: B365 price x Pinnacle fair >= {1+th}", D.b365_u.notna()&D.q_pin.notna()&(D.b365_u*(1-D.q_pin)>=1+th),"b365_u",yu)
for th in (0.0,0.02,0.04,0.06,0.08):
    rep(f"Over: B365 x market-average fair >= {1+th}", D.b365_o.notna()&D.q_avg.notna()&(D.b365_o*D.q_avg>=1+th),"b365_o",yo)
    rep(f"Under: B365 x market-average fair >= {1+th}", D.b365_u.notna()&D.q_avg.notna()&(D.b365_u*(1-D.q_avg)>=1+th),"b365_u",yu)
for th in (0.02,0.04,0.06,0.08,0.10):
    rep(f"Over: BEST price x market-average fair >= {1+th}", D.max_o.notna()&D.q_avg.notna()&(D.max_o*D.q_avg>=1+th),"max_o",yo)
    rep(f"Under: BEST price x market-average fair >= {1+th}", D.max_u.notna()&D.q_avg.notna()&(D.max_u*(1-D.q_avg)>=1+th),"max_u",yu)
# closing line value: does B365 pre-match beat B365 closing?
m=D.b365_o.notna()&D.b365c_o.notna(); print("\nB365 Over pre vs close: shortened",int((D.b365c_o<D.b365_o)[m].sum()),"drifted",int((D.b365c_o>D.b365_o)[m].sum()),"same",int((D.b365c_o==D.b365_o)[m].sum()))
for lab,mm in (("price shortened by close",m&(D.b365c_o<D.b365_o)),("drifted",m&(D.b365c_o>D.b365_o)),("same",m&(D.b365c_o==D.b365_o))):
    rep("Over at B365 pre-match, "+lab, mm,"b365_o",yo)
