"""
write_manifest.py  -  machine-readable completion manifest for a V4 run, so a reviewer (ChatGPT, Claude, Rob) can confirm
it is looking at the right run and that the run completed before reports were delivered.

    python3 write_manifest.py <run_id> [--commit <sha>]

Reads logs/execution/executions.csv, the run folder, the report folder and football.db. Writes
    reports/manifests/<run_id>.json           the manifest
    reports/manifests/latest_<mode>.json      a copy, so 'the latest weekend run' is one fixed path
Runs after run_v4.py and never changes any report. Safe to re-run: it only describes what exists.
"""
import sys, os, json, hashlib, sqlite3, datetime as dt, pandas as pd

MODEL_VERSION = "v4"

def sha(path, n=16):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()[:n]

def describe(path):
    return dict(path=path, bytes=os.path.getsize(path), sha256_16=sha(path)) if os.path.exists(path) else dict(path=path, missing=True)

def main():
    run_id = sys.argv[1]; commit = sys.argv[sys.argv.index("--commit") + 1] if "--commit" in sys.argv else os.environ.get("GITHUB_SHA", "")
    mode = run_id.split("_")[0]; stamp = run_id.split("_")[1]; date = f"{stamp[:4]}-{stamp[4:6]}-{stamp[6:8]}"
    ex = pd.read_csv("logs/execution/executions.csv", dtype=str)
    row = ex[ex.run_id == run_id]
    status = dict(status="missing from executions.csv") if row.empty else row.iloc[-1].to_dict()
    db = {}
    if os.path.exists("football.db") and os.path.getsize("football.db") > 0:
        c = sqlite3.connect("football.db")
        db = dict(max_finished_kickoff_utc=c.execute("select max(kickoff_utc) from fixtures where status in ('FT','AET','PEN')").fetchone()[0],
                  finished_matches=c.execute("select count(*) from fixtures where status in ('FT','AET','PEN')").fetchone()[0],
                  scheduled_matches=c.execute("select count(*) from fixtures where status='NS'").fetchone()[0],
                  scored_but_not_finished=c.execute("select count(*) from fixtures where ft_home is not null and status not in ('FT','AET','PEN')").fetchone()[0])
    files, warnings, window, counts = [], [], {}, {}
    if mode in ("midweek", "weekend", "range"):
        outdir = f"reports/{mode}/{date}"
        for s in ("english", "european", "combined"):
            files += [describe(f"{outdir}/{s}_{date}.pdf"), describe(f"{outdir}/{s}_{date}.csv")]
        files += [describe(f"{outdir}/predictions_{date}.json"), describe(f"reports/chatgpt_review/chatgpt_review_{date}_{mode}.md")]
        for s in ("english", "european"):
            fl = f"runs/{run_id}/flagged_{s}.csv"
            if os.path.exists(fl):
                n = len(pd.read_csv(fl))
                if n: warnings.append(f"{n} {s} fixtures postponed/other status, not analysed (see {fl})")
        rv = f"reports/chatgpt_review/chatgpt_review_{date}_{mode}.md"
        if os.path.exists(rv):
            for line in open(rv, encoding="utf-8"):
                if line.startswith("Data-quality warnings:"):
                    txt = line.split(":", 1)[1].strip()
                    if txt and txt != "none": warnings = [w.strip() for w in txt.split(";")]
                if line.startswith("Report date:") and "Analysis window:" in line:
                    window["text"] = line.split("Analysis window:")[1].split(".")[0].strip()
        pj = f"{outdir}/predictions_{date}.json"
        if os.path.exists(pj):
            P = pd.DataFrame(json.load(open(pj)))
            counts = dict(fixtures=len(P), by_classification=P.classification.value_counts().to_dict(), btts_yes=int((P.btts == "YES").sum()),
                          competitions=int(P.competition.nunique()))
        for extra in (f"reports/btts_audit/{date}/btts_audit_{date}_{mode}.csv", f"reports/btts_audit/{date}/btts_audit_{date}_{mode}.json", f"reports/chatgpt_review/btts_audit_review_{date}_{mode}.md"):
            if os.path.exists(extra): files.append(describe(extra) | {"audit": True})
    elif mode == "review":
        files += [describe(f"reports/performance/performance_{date}.md"), describe("data/results/results_log.csv"), describe("data/predictions/predictions_log.csv")]
    if db.get("scored_but_not_finished"): warnings.append(f"{db['scored_but_not_finished']} matches in the database carry a score but are not FT/AET/PEN (abandoned, awarded or cancelled); neither the card nor the model counts them as results since 29 Oct")
    now = dt.datetime.now(dt.timezone.utc)
    man = dict(manifest_version=1, run_id=run_id, mode=mode, model_version=MODEL_VERSION, created_at_utc=now.strftime("%Y-%m-%d %H:%M:%S"),
               created_at_london=pd.Timestamp(now).tz_convert("Europe/London").strftime("%Y-%m-%d %H:%M:%S %Z"), git_commit=commit,
               fixture_window=window, completion=dict(status=status.get("status"), start_london=status.get("start"), finish_london=status.get("finish"), message=status.get("message")),
               model_files=dict(bands_model_pkl=sha("bands_model.pkl") if os.path.exists("bands_model.pkl") else None, btts_model_pkl=sha("btts_model.pkl") if os.path.exists("btts_model.pkl") else None),
               database=db, counts=counts, report_files=files, missing_files=[f["path"] for f in files if f.get("missing")], data_quality_warnings=warnings,
               complete=bool(status.get("status") == "ok" and not any(f.get("missing") for f in files)))
    os.makedirs("reports/manifests", exist_ok=True)
    json.dump(man, open(f"reports/manifests/{run_id}.json", "w"), indent=1)
    json.dump(man, open(f"reports/manifests/latest_{mode}.json", "w"), indent=1)
    print(json.dumps(dict(run_id=run_id, complete=man["complete"], missing=man["missing_files"], warnings=warnings), indent=1))

if __name__ == "__main__":
    main()
