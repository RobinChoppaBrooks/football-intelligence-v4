#!/usr/bin/env bash
# ci/run.sh  -  the whole GitHub Actions job for Football Intelligence V4.1. The workflow file only calls this script,
# so every change to the pipeline is an ordinary file upload; .github/workflows/football.yml never needs editing again.
#
# Inputs (environment, set by the workflow):
#   GH_EVENT      github.event_name          schedule | workflow_dispatch
#   GH_SCHEDULE   github.event.schedule      the cron string that fired, when scheduled
#   MODE_INPUT    github.event.inputs.mode   review | midweek | weekend | range | download-only, when run by hand
#   APISPORTS_KEY secret for download.py
#   GITHUB_TOKEN, GITHUB_REPOSITORY, GITHUB_SHA  provided by Actions
#
# Schedule slots (Europe/London targets): Monday 08:30 review, Monday 12:30 midweek, Friday 07:00 weekend.
# GitHub cron is UTC only, so each slot has a GMT entry and a BST entry in the workflow; this script runs the one that
# matches today's London clock and skips the other.
set -u
cd "$(dirname "$0")/.."

CLOCK=$(TZ=Europe/London date +%Z)
MODE=""
case "${GH_EVENT:-}:${GH_SCHEDULE:-}:$CLOCK" in
  schedule:"30 8 * * 1":GMT  | schedule:"30 7 * * 1":BST)  MODE=review ;;
  schedule:"30 12 * * 1":GMT | schedule:"30 11 * * 1":BST) MODE=midweek ;;
  schedule:"0 7 * * 5":GMT   | schedule:"0 6 * * 5":BST)   MODE=weekend ;;
  schedule:*) echo "Cron '${GH_SCHEDULE:-}' is the wrong DST variant for a $CLOCK clock; nothing to do."; exit 0 ;;
  *) MODE="${MODE_INPUT:-download-only}" ;;
esac
echo "London clock $CLOCK, mode $MODE"

# 1. current database: branch data, else the seed
if git ls-remote --exit-code --heads origin data >/dev/null 2>&1; then
  git fetch --depth 1 origin data
  git show origin/data:football.db > football.db
else
  cp seed/football.db football.db
fi
ls -la football.db

# 2. fixtures and results from API-Football (the only API step)
python download.py --results

# 3. the model. A failure here is recorded (manifest, logs) and committed, then the job exits non-zero at the end.
MODEL_STATUS=0
if [ "$MODE" != "download-only" ]; then
  python run_v4.py "$MODE" || MODEL_STATUS=$?
  RUN_ID=$(tail -n 1 logs/execution/executions.csv | cut -d, -f1)
  echo "run id $RUN_ID, model exit $MODEL_STATUS"
  case "$MODE" in
    midweek|weekend|range)
      python btts_audit.py "$RUN_ID" || echo "audit skipped: $?"
      ;;
  esac
  python write_manifest.py "$RUN_ID" --commit "$GITHUB_SHA" || echo "manifest skipped: $?"
  case "$MODE" in
    midweek|weekend|range)
      python render_email.py "$RUN_ID" || echo "email render skipped: $?"
      ;;
  esac
fi

# 4. slim database for branch data
python export_slim.py football.db football_slim.db

# 5. commit reports and logs to main
git config user.name "football-v4-bot"
git config user.email "football-v4-bot@users.noreply.github.com"
git add -A reports data logs runs predictions_log.csv
git commit -m "V4.1 $MODE run $(date -u +'%Y-%m-%d %H:%M') UTC" || echo "nothing to commit"
git push

# 6. slim database to branch data (single commit, replaced each run)
WS=$(pwd)
rm -rf /tmp/data && mkdir -p /tmp/data && cd /tmp/data
git init -q -b data
git config user.name "football-v4-bot"
git config user.email "football-v4-bot@users.noreply.github.com"
cp "$WS/football_slim.db" football.db
echo "Slim football.db written $(date -u +'%Y-%m-%d %H:%M') UTC by the $MODE run." > README.md
git add football.db README.md
git commit -q -m "football.db $(date -u +'%Y-%m-%d %H:%M') UTC"
git push --force "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}" data

if [ "$MODEL_STATUS" -ne 0 ]; then
  echo "model step failed with exit $MODEL_STATUS (recorded in logs and manifest)"; exit "$MODEL_STATUS"
fi
echo "done"
