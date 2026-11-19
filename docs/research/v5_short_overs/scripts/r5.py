import pandas as pd, numpy as np
T=pd.read_pickle("T.pkl")
def run(pcol,price,side,th):
    p=T[pcol] if side=="o" else 1-T[pcol]; pr=T[price]; y=T.y if side=="o" else 1-T.y
    m=pr.notna()&(p*pr>=1+th); pl=(pr*y-1)[m]
    return {s:(int((T.season[m]==s).sum()),round(float(pl[T.season[m]==s].sum()),1)) for s in (2024,2025,2026)}
for pcol in ("pA","pB","pC"):
    for side in ("o","u"):
        for price in (("b365_o","max_o") if side=="o" else ("b365_u","max_u")):
            for th in (0.0,0.02,0.04,0.06):
                r=run(pcol,price,side,th); print(pcol,side,price,th,r)
