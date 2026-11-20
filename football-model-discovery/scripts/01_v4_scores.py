"""01_v4_scores.py - score every historical fixture with the LOCKED V4.1 model (bands_model.pkl), exactly as production
builds its inputs (features.py). Read-only use of production code; nothing in production is changed.
Usage: python3 -I scripts/01_v4_scores.py <football.db> <repo_root> <out.parquet>"""
import sys, pickle
db, repo, out = sys.argv[1:4]
sys.path.insert(0, repo)
import features, bands
X = features.build(db)
b = pickle.load(open(f"{repo}/bands_model.pkl", "rb"))
X["v4_score"] = bands.predict(b, X)
keep = ["fixture_id", "league_id", "season", "kickoff_utc", "v4_score", "h_l5L_n", "a_l5L_n", "h_l5L_gf2", "a_l5L_gf2", "h_l5L_ga2", "a_l5L_ga2", "h_l5L_cs", "a_l5L_cs"]
X[keep].to_parquet(out)
print(len(X), "scored; cuts", b["green"], b["amber"])
