import pandas as pd, numpy as np
D=pd.read_pickle("D.pkl")
def res(m,col="max_o",side="o"):
    g=D[m & D[col].notna()]; y=g.y if side=="o" else 1-g.y; pl=g[col]*y-1
    out=[]
    for s in (2023,2024,2025,2026):
        ps=pl[g.season==s]; out.append(f"{len(ps)}:{ps.sum():+.0f}")
    return " | ".join(out)+f" || all {len(pl)}: {pl.sum():+.1f} ({pl.mean()*100:+.1f}/100)"
print("Over by Pinnacle implied band, at MAX price  (season n:PL units)")
for lo,hi in ((0,.45),(.45,.5),(.5,.55),(.55,.6),(.6,.65),(.65,.7),(.7,1),(.6,1),(.62,1),(.65,1)):
    print(f" q {lo}-{hi}: ", res((D.q_pin>=lo)&(D.q_pin<hi)))
print("\nsame at B365 price")
for lo,hi in ((.6,1),(.65,1)):
    print(f" q {lo}-{hi}: ", res((D.q_pin>=lo)&(D.q_pin<hi),"b365_o"))
print("\nsame at Pinnacle price")
for lo,hi in ((.6,1),(.65,1)):
    print(f" q {lo}-{hi}: ", res((D.q_pin>=lo)&(D.q_pin<hi),"pin_o"))
print("\nUnder by band at max")
for lo,hi in ((0,.4),(0,.45),(.45,.5)):
    print(f" q {lo}-{hi}: ", res((D.q_pin>=lo)&(D.q_pin<hi),"max_u","u"))
print("\nOver q>=0.6 at max, by league")
for code,g in D[D.q_pin>=.6].groupby("fd_code"):
    pl=g.max_o*g.y-1; print(f" {code}: n {len(g)} PL {pl.sum():+.1f}  by season", {s:round(float(pl[g.season==s].sum()),1) for s in (2023,2024,2025,2026)})
