# Proposed changes, not applied (need Rob's approval)

Each file here is a unified diff against main as of commit 31a3097 (29 Oct 2026). Nothing in this folder is active.

- football.yml.diff (full file: football.yml): DST-aware cron guard so the model runs at 08:30 / 12:30 / 08:30 Europe/London all year,
  manifest and commit steps run even when the model step fails, manifest step, optional BTTS audit step.
- analyse_fixtures_A_abandoned_matches.diff: last_n() ignores abandoned, awarded and cancelled matches that carry a score (features.py already does).
- analyse_fixtures_B_btts_verdict_from_model.diff: the BTTS verdict follows the BTTS model band (YES = High) instead of the Over 2.5 goal pattern.
  See docs/btts_audit_2026-10-29.md sections 6 and 9 for the backtest behind it.

Apply one with:   git apply docs/proposed/<name>.diff
After applying B, bump btts_engine.verdict_rule in config/model_config.json and record the change in over25_changelog.md.
Also update config/schedules.json and the three delivery task prompts to say 08:30 / 12:30 / 08:30 London and to check reports/manifests/latest_<mode>.json.
