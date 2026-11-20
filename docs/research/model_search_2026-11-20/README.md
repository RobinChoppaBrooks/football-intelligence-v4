# Model pressure test, round 2 (20 Nov 2026, research only, V4.1 unchanged)

Follows docs/research/model_search_2026-11-19 and tests what it did not: a brute-force count-formula search, team strength
ratings, per-league models and blends. Same scoring: top 20 a weekend, Rob's 14 leagues, Friday to Sunday, both sides with 3+
league games. Clean test = 2025-26 and 2026-27 to 18 Nov (53 weekends, 1,057 picks), never used to choose anything.
Database: slim football.db from the data branch, 20 Nov 2026 10:41 UTC.

## Reference points (test, 1,057 picks)
| | Hits |
|---|---|
| V4.1 as published | 661 |
| Random 20 a weekend (expected) | 584 |

## 1. Formula search: 59,048 count formulas
Ten terms (sums of both sides, last 5 league games unless stated): Scored 2+, Let in 2+, 3+ games, clean sheets (minus),
failed to score (minus), BTTS games, venue 3+ games (last 3 home / away), division 3+ rate so far, two-route match-up,
3+ games last 10. Weights 0, 1 or 2 each. Chosen on 2023-24 and 2024-25, then judged on the test.
- Best formula on training: 648 of 1,057. Top 100 training formulas on test: 635 to 658, middle 647. None beat V4.1.
- Best in hindsight on the test (picked by looking at the answers, so not usable): 667. That is the ceiling for count formulas.
- Single terms on test: division 3+ rate 656, Scored 2+ 652 to 655, 3+ games last 10 633, BTTS games 619, 3+ games last 5 612,
  failed to score 611, venue 3+ 610, two-route 605, clean sheets 589, Let in 2+ 569 to 583 (no better than random).

## 2. Team strength ratings (attack and defence per team, updated after every match, Poisson chance of 3+)
15 settings; chosen on training (learning rate 0.05, 50% carried into a new season): 649 of 1,057 (rating_grid.csv).

## 3. Per-league models and blends (c.py)
| Model | Test hits | v V4.1 | 90% range |
|---|---|---|---|
| V4.1 refit + rating inputs | 662 | +1 | -19 to +20 |
| Blend 2x V4.1 + rating + per-league | 659 | -2 | -18 to +15 |
| Division 3+ rate alone | 656 | -5 | -25 to +14 |
| V4.1 + rating blend | 651 | -10 | -26 to +7 |
| V4.1 refit | 650 | -11 | -28 to +6 |
| Rating alone | 649 | -12 | -39 to +14 |
| V4.1 + division blend | 647 | -14 | -31 to +5 |
| One model per league | 636 | -25 | -52 to +1 |

## Conclusion
Nothing beats V4.1 by a margin that can be told apart from luck. Across both rounds (about 59,100 variants) the top 20 lands
roughly 62 to 63 in 100 against 55 for a random pick from the same leagues. Most of V4.1's edge is the division's scoring
rate plus each side's Scored 2+ count. Let in 2+ on its own adds nothing at the top of the list.
