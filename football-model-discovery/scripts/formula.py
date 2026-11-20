"""formula.py - turns a formula string from the search into a boolean selection on any fixture frame."""
import re, numpy as np
import importlib.util, os

_spec = importlib.util.spec_from_file_location("s04", os.path.join(os.path.dirname(__file__), "04_search.py"))


def variables(d):
    """same variable definitions the search used (copied from 04_search.frame to avoid re-running the search)."""
    import pandas as pd
    VARS = ["s1", "s2", "s3", "c1", "c2", "c3", "cs", "fts", "o25", "o35", "btts", "both2", "one3"]
    V = {}
    for v in VARS:
        h, a = d[f"h_S5_{v}"].values, d[f"a_S5_{v}"].values
        V[f"h.{v}"] = h; V[f"a.{v}"] = a; V[f"sum.{v}"] = h + a; V[f"min.{v}"] = np.minimum(h, a); V[f"max.{v}"] = np.maximum(h, a)
    for v in ("o25", "s2", "c2"):
        V[f"hv3.{v}"] = d[f"h_V3_{v}"].values; V[f"av3.{v}"] = d[f"a_V3_{v}"].values
        V[f"v3sum.{v}"] = d[f"h_V3_{v}"].values + d[f"a_V3_{v}"].values
    V["l10sum.o25"] = d.h_S10_o25.values + d.a_S10_o25.values
    V["goals5.sum"] = d.h_S5_g.values + d.a_S5_g.values
    V["route.s2c2"] = np.maximum(d.h_S5_s2 + d.a_S5_c2, d.a_S5_s2 + d.h_S5_c2).values
    V["route.s3c3"] = np.maximum(d.h_S5_s3 + d.a_S5_c3, d.a_S5_s3 + d.h_S5_c3).values
    V["route.min"] = np.maximum(np.minimum(d.h_S5_s2, d.a_S5_c2), np.minimum(d.a_S5_s2, d.h_S5_c2)).values
    V["drivers20"] = (d.h_S5_s2 + d.a_S5_s2 + d.h_S5_c2 + d.a_S5_c2).values
    lr = np.where(d.lg_n >= 30, d.lg_o25 / d.lg_n.replace(0, np.nan), d.pl_o / d.pl_n)
    V["lg.o25x10"] = np.round(np.nan_to_num(lr, nan=0.53) * 10)
    return {k: np.nan_to_num(np.asarray(v, float), nan=-99) for k, v in V.items()}


ATOM = re.compile(r"^\s*([\w.]+)\s*(>=|<=)\s*(-?[\d.]+)\s*$")


def mask(formula, V):
    f = formula.strip()
    if f.startswith("["):
        body, thr = f[1:].split("] >=")
        score = np.zeros(len(next(iter(V.values()))))
        for term in re.findall(r"([+-]?)\s*(\d*)\*?([a-z][\w.]+)", body):
            sign = -1 if term[0] == "-" else 1; w = int(term[1]) if term[1] else 1
            v = V[term[2]].copy(); v[v == -99] = 0; score = score + sign * w * v
        return score >= float(thr)
    m = np.ones(len(next(iter(V.values()))), bool)
    for part in f.split(" AND "):
        g = ATOM.match(part); name, op, k = g.group(1), g.group(2), float(g.group(3))
        v = V[name]
        m &= (v >= k) if op == ">=" else ((v <= k) & (v > -99))
    return m
