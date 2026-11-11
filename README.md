# Football Intelligence V4.2

Rob's Over 2.5 (3+ goals) fixture analysis, running unattended on GitHub Actions. V4.2 (11 Nov 2026): counts-only model, whale trump card, FT-only results, no BTTS model.

## What runs, and when (Europe/London)
| When | Mode | Output |
|---|---|---|
| Monday 08:30 | review | results for last week's predictions, `reports/performance/` |
| Monday 12:30 | midweek | Monday to Friday fixtures not yet kicked off, `reports/midweek/<date>/` |
| Friday 07:00 | weekend | Saturday and Sunday fixtures, `reports/weekend/<date>/` |

Each run pulls fixtures and results from API-Football (about 65 calls), runs `run_v4.py`, commits the reports,
`data/predictions/predictions_log.csv`, `data/results/results_log.csv` and `logs/execution/executions.csv` to `main`,
and pushes the slim database to the branch `data` (one commit, replaced every run).

## One-time setup
1. Settings -> Secrets and variables -> Actions -> New repository secret: name `APISPORTS_KEY`, value = your API-Sports key.
2. Actions tab -> "Football Intelligence V4" -> Run workflow -> mode `download-only` once. The branch `data` appears when it finishes.

## Run it by hand
Actions tab -> Run workflow -> mode `midweek`, `weekend` or `review`.

## Files
- `run_v4.py` orchestrator (midweek, weekend, range, review); `analyse_fixtures.py`, `report_v4.py` the production analysis and report.
- `bands_model.pkl` the selection model (scikit-learn 1.8.0), fitted by `bands.py` from `features.py`.
- `config/model_config.json` the exact current model (V4.2); `config/competitions.json` Rob's 14 leagues; `config/schedules.json` the schedule.
- `config/benchmarks.json` the one benchmark every report quotes, written by `benchmarks.py` each Monday review.
- `docs/methodology.md` the method, `docs/backtest_baseline.md` the backtest tables, `docs/changelog.md` the history, `docs/research/` research records, `docs/research_policy.md` the rules for any change.
- `data/predictions/predictions_log.csv` the only pre-match prediction record; `data/results/results_log.csv` the scored results.
- `seed/football.db` a starting database, used only if branch `data` is ever missing.

Bookmaker odds are never used for selection or shown. The API key is never stored in this repository.
