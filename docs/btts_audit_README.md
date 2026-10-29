# BTTS audit tooling (btts_audit_v1)

New files, all additive. The production model, thresholds, verdict rule and published predictions are unchanged.

| file | purpose |
|---|---|
| btts_rules.py | the production BTTS verdict rule re-stated from counts (replicates analyse_fixtures.pattern_text exactly), the evidence score, and the candidate rules under test |
| btts_audit.py | `python3 btts_audit.py <run_id>`: independent assessment, contradiction flags with explanations, ChatGPT review file. Writes only under reports/btts_audit/<date>/ and reports/chatgpt_review/btts_audit_review_*.md |
| backtest_btts.py | `python3 backtest_btts.py features_all.pkl`: chronological backtest, writes reports/btts_audit/backtest/ |
| write_manifest.py | `python3 write_manifest.py <run_id> [--commit sha]`: completion manifest, reports/manifests/<run_id>.json and latest_<mode>.json |
| reports/btts_audit/recompute.py | the independent recomputation of every last-five count from football.db used in the audit |
| docs/btts_audit_2026-10-29.md | the audit report |
| docs/proposed/ | diffs awaiting approval (workflow, two one-line fixes in analyse_fixtures.py) |

Scoring both versions after the weekend: join reports/btts_audit/2026-10-29/btts_audit_2026-10-29_weekend.csv to data/results/results_log.csv on run_id and fixture_id;
compare btts (production) and audit_assessment (YES, LEAN YES, NO LEAN) against btts_result.
