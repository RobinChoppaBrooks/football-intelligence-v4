# Accumulator structure backtest (19 Nov 2026, research only, no model change)

Question (Rob): over past seasons, how often would £1,000 split across 20-fold accumulators have landed each weekend?

Method: every finished league fixture in Rob's 14 leagues, seasons 2023-24 to 2026-27 (to 19 Nov), scored by the locked V4.1
model (bands_model.pkl) with information up to each kick-off. Weekend = Friday to Sunday (London). Pool = selected fixtures
(High, Medium incl. report Weak, trump card); sides with fewer than 3 league games rejected. Weekends with fewer than 20 selected: no bet.

Strategies per weekend: (a) 100 random 20-folds drawn from the pool, £10 each; (b) the top 20 by model score as one 20-fold;
(c) the top 20 split into 4 groups of 5 (snake order by score), counting groups that landed.

Results (counts):

| Season | Weekends | 20+ selected | Random 20-folds: weekends with a winner | Top 20 as one 20-fold | 4x5: 1+ group | 2+ | 3+ |
|---|---|---|---|---|---|---|---|
| 2023-24 | 42 | 28 | 0 | 0 | 11 | 2 | 1 |
| 2024-25 | 39 | 5 | 0 | 0 | 2 | 0 | 0 |
| 2025-26 | 40 | 23 | 0 | 0 | 9 | 1 | 0 |
| 2026-27 | 12 | 8 | 0 | 0 | 5 | 0 | 0 |
| Total | 133 | 64 | 0 (0 of 6,400 tickets) | 0 | 27 | 3 | 1 |

Caveats: 2023-24 and 2024-25 are the model's training seasons (flattering); cut points were chosen on 2025-26; only 2026-27 is clean.
Run: `python3 -I acca_bt.py football.db` (writes acca_weeks.csv, one row per weekend).
