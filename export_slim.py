"""export_slim.py  -  football.db -> football_slim.db without the raw API cache and logs (what the cloud needs: fixtures,
results, teams, competitions, coverage, match statistics, goals odds).    python3 export_slim.py football.db football_slim.db"""
import sys, sqlite3, os
src, dst = sys.argv[1], sys.argv[2]
if os.path.exists(dst): os.remove(dst)
c = sqlite3.connect(src); c.execute("ATTACH DATABASE ? AS slim", (dst,))
from store import SCHEMA
for stmt in SCHEMA.split(";"):
    s = stmt.strip()
    if s.upper().startswith("CREATE TABLE"): c.execute(s.replace("CREATE TABLE IF NOT EXISTS ", "CREATE TABLE IF NOT EXISTS slim."))
    elif s.upper().startswith("CREATE INDEX"): c.execute(s.replace("CREATE INDEX IF NOT EXISTS ", "CREATE INDEX IF NOT EXISTS slim."))
for t in ("competitions", "coverage", "teams", "fixtures", "fixture_stats", "fixture_odds", "predictions_log"):
    c.execute(f"INSERT OR REPLACE INTO slim.{t} SELECT * FROM main.{t}")
c.commit(); c.execute("DETACH DATABASE slim"); c.close()
d = sqlite3.connect(dst); d.execute("VACUUM"); d.close()
print(f"{dst}: {os.path.getsize(dst)/1e6:.1f} MB")
