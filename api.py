"""
api.py  -  cached, logged API-Football client. Every call is written to football.db before it is parsed.

Key: put it in  apisports_key.txt  next to this file (one line). Or set APISPORTS_KEY in the environment.
"""
import os, sys, json, time, hashlib, sqlite3
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "football.db")
BASE_URL = "https://v3.football.api-sports.io"
DAILY_STOP = 7300          # stop the run when the day's remaining allowance drops below this many used
SLEEP = 0.25               # PRO plan allows 300 requests/min; 0.25 s keeps us at ~240

def _key():
    k = os.getenv("APISPORTS_KEY")
    p = os.path.join(HERE, "apisports_key.txt")
    if not k and os.path.exists(p):
        k = open(p, encoding="utf-8").read().strip()
    if not k:
        sys.exit("No API key. Create apisports_key.txt next to api.py with the key on one line.")
    return k

class Client:
    def __init__(self, db_path=DB_PATH):
        import requests
        self.s = requests.Session()
        self.s.headers["x-apisports-key"] = _key()
        self.db = sqlite3.connect(db_path)
        self.db.execute("PRAGMA journal_mode=WAL")
        from store import ensure_schema
        ensure_schema(self.db)
        self.calls_this_run = 0
        self.remaining = None      # daily allowance left, from response headers

    @staticmethod
    def _hash(endpoint, params):
        return hashlib.sha1((endpoint + "?" + json.dumps(params, sort_keys=True)).encode()).hexdigest()

    def get(self, endpoint, use_cache=True, **params):
        """Return the parsed 'response' list. Cached responses are returned without an API call."""
        h = self._hash(endpoint, params)
        if use_cache:
            row = self.db.execute("SELECT response FROM api_cache WHERE key=? AND result_count>0", (h,)).fetchone()
            if row:
                return json.loads(row[0])["response"]
        if self.remaining is not None and self.remaining < (7500 - DAILY_STOP):
            raise RuntimeError(f"Daily allowance nearly used ({self.remaining} left). Re-run tomorrow; the cache resumes where this stopped.")
        for attempt in range(4):
            try:
                r = self.s.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
            except Exception as e:
                print(f"  network error {e}; retry {attempt+1}"); time.sleep(5 * (attempt + 1)); continue
            self.calls_this_run += 1
            rem = r.headers.get("x-ratelimit-requests-remaining")
            self.remaining = int(rem) if rem is not None else self.remaining
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            try:
                d = r.json()
            except Exception:
                d = {"errors": {"json": r.text[:200]}, "response": []}
            errs = d.get("errors") or {}
            n = len(d.get("response") or []) if isinstance(d.get("response"), list) else (1 if d.get("response") else 0)
            self.db.execute("INSERT INTO api_log(ts,endpoint,params,http_status,result_count,remaining,error) VALUES(?,?,?,?,?,?,?)",
                            (now, endpoint, json.dumps(params, sort_keys=True), r.status_code, n, self.remaining, json.dumps(errs) if errs else None))
            if r.status_code == 429 or (isinstance(errs, dict) and "rateLimit" in errs):
                self.db.commit(); print("  rate limited, waiting 60 s"); time.sleep(60); continue
            if r.status_code >= 500:
                self.db.commit(); time.sleep(5 * (attempt + 1)); continue
            if errs:
                self.db.commit(); print(f"  API error {endpoint} {params}: {errs}")
                return []
            # only a populated response may overwrite an existing cache row
            if n > 0:
                self.db.execute("INSERT OR REPLACE INTO api_cache(key,endpoint,params,fetched_at,http_status,result_count,response) VALUES(?,?,?,?,?,?,?)",
                                (h, endpoint, json.dumps(params, sort_keys=True), now, r.status_code, n, json.dumps(d)))
            else:
                self.db.execute("INSERT OR IGNORE INTO api_cache(key,endpoint,params,fetched_at,http_status,result_count,response) VALUES(?,?,?,?,?,?,?)",
                                (h, endpoint, json.dumps(params, sort_keys=True), now, r.status_code, 0, json.dumps(d)))
            self.db.commit()
            time.sleep(SLEEP)
            return d.get("response") or []
        print(f"  gave up on {endpoint} {params}")
        return []

    def close(self):
        self.db.commit(); self.db.close()
