# football-model-discovery (research only)

Over 2.5 goals formula and model discovery lab, 20 Nov 2026. Production V4.1 is not touched; nothing here is imported by the live pipeline.
Read `report/FINAL_REPORT.md` first.

Run order (from this folder, after extracting `football.db` from branch `data`):
```
python3 scripts/01_v4_scores.py <football.db> .. data/v4_scores.parquet   # V4.1 scores rebuilt with production code
python3 scripts/02_features.py  <football.db> data/features.parquet         # point-in-time features + leakage test
python3 scripts/03_run_families.py      # 12 families, walk-forward 2024-25 and 2025-26
python3 scripts/04_search.py            # 510,223 formula evaluations on DEV + null search
python3 scripts/05_validate.py          # VAL scoring, freezes results/preregistered.json
python3 scripts/06_test.py              # one-shot TEST, accumulators, robustness
python3 scripts/07_v4_live.py           # against published V4.1 predictions
python3 scripts/08_summaries.py         # league tables, failure analysis, master workbook
python3 scripts/09_report.py            # report/FINAL_REPORT.md
```
Splits are fixed in `scripts/lab.py`: DEV 2023-24 + 2024-25, VAL 2025-26, TEST 2026-27 to 17 Nov 2026. Seed 20261120.
Experiment log: git history of this folder. Commit 541f8d8 froze the finalists before TEST was opened.
