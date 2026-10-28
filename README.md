# Football Intelligence V4

Rob's Over 2.5 (3+ goals) and BTTS fixture analysis, running unattended on GitHub Actions with the locked V4 model.

## What runs, and when (Europe/London)
| When | Mode | Output |
|---|---|---|
| Monday morning | review | results for last week's predictions, `reports/performance/` |
| Monday lunchtime | midweek | Mon to Thu fixtures, `reports/midweek/<date>/` |
| Thursday morning | weekend | Fri to Sun fixtures, `reports/weekend/<date>/` |

Each run pulls fixtures and results from API-Football (about 65 calls), runs `run_v4.py`, commits the reports,
`data/predictions/predictions_log.csv`, `data/results/results_log.csv` and `logs/execution/executions.csv` to `main`,
and pushes the slim database to the branch `data` (one commit, replaced every run).

## One-time setup
1. Settings -> Secrets and variables -> Actions -> New repository secret: name `APISPORTS_KEY`, value = your API-Sports key.
2. Actions tab -> "Football Intelligence V4" -> Run workflow -> mode `download-only` once. The branch `data` appears when it finishes.

## Run it by hand
Actions tab -> Run workflow -> mode `midweek`, `weekend` or `review`.

## Files
- `run_v4.py` orchestrator; `analyse_fixtures.py`, `report_v4.py` the production analysis and report.
- `bands_model.pkl`, `btts_model.pkl` the locked models (scikit-learn 1.8.0).
- `over25_model_v4_methodology.md`, `over25_model_v4_config.json`, `over25_backtest_baseline.md`, `over25_changelog.md` the method.
- `seed/football.db` the starting slim database (used only until branch `data` exists).

Bookmaker odds are never used for selection. The API key is never stored in this repository.
