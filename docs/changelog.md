# Over 2.5 changelog

- 25 Sep 2026: v3 skill replaced by the backtested model project (PC data store, walk-forward validation).
- 7 Oct 2026: card format adopted; pattern search on 30,535 matches (division rate and both sides' recent 3+ counts the strongest signals).
- 19 Oct 2026: features fix (cup ties now carry league form), model refit; averages removed; cards redesigned (dot panel, no light); BTTS model, goal pattern, why/risk, prediction log, rules file v2; outlier catch removed after testing.
- 21 Oct 2026: four-week audit (audit_report_20261021.md); catches found not to predict failure; High cut briefly moved to 0.650 and reverted the same day; BTTS verdict tied to the goal pattern.
- 27 Oct 2026: DFB Pokal and Copa del Rey added; odds and injuries download step (--extras); midweek extras sheet (corners, cards, market, injuries) built then parked.
- 28 Oct 2026: V2 alignment report built and backtested (62%); V3 formulas backtested (62 to 66%); V4 LOCKED: validated model unchanged as the selection engine, report_v4.py as the production renderer, config / methodology / baseline / changelog saved.
- 28 Oct 2026 (later): Football Intelligence V4 operations: project structure (config/, data/, reports/, logs/, docs/), run_v4.py orchestrator (midweek / weekend / range / review / status), English, European and combined reports, JSON export, ChatGPT review package, results reconciliation, performance report, three scheduled tasks (Mon 09:54 review, Mon 13:52 midweek, Thu 09:52 weekend, Europe/London, bound to Rob's PC). Dry-run test on 28 to 30 Oct fixtures tagged in the prediction database as a test. Reproduction test of the 24 Oct report: 70 of 71 fixtures identical (one moved by 0.021 after Friday's results arrived).
