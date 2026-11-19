import sys, os, json, pickle, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
REPO="/home/claude/football-intelligence-v4"; sys.path.insert(0, REPO); os.chdir(REPO)
from features import build
from bands import predict as band_predict
X=build("/tmp/fdb.db"); X=X[X.target_over25.notna()].copy()
bb=pickle.load(open("bands_model.pkl","rb")); X["p_v41"]=band_predict(bb,X)
X=X.copy(); X.to_pickle("/home/claude/bt/X_all.pkl"); print(X.shape)
