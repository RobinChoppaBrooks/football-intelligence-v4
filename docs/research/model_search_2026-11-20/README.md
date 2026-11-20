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

## 4. Rest days and fixture congestion (rest.py, no API calls)
Per side, from every competition in the database: days since last match, days to next match, games in last 14 and 21 days,
played in Europe within 4.5 days, first game after a break (both sides 11+ days).
- Added to the V4.1 recipe, walk-forward, test top 20: 654 v 650 for the refit without it (+4, range -6 to +14). V4.1 as published 661.
- After Europe looked positive at the same V4.1 score (694 of 1,174 v 662.5 expected) but against the same clubs' other league
  games it is 694 v 717.6 expected: it described which clubs play in Europe, not the effect of playing midweek. Rejected.
- First game after a break: 671 of 1,184 v 647.7 expected at the same V4.1 score, within normal variation. Not established.
- Shorter or longer rest and games in the last 14 days: flat (no band of rest stands out).

## 5. Rob's last-N counts and clean sheets (last5.py, last5_eval.py, last5_grid.csv)
Counts only, built fresh from results: goals scored, goals conceded, clean sheets, failed to score, 3+ games, over the last
3, 4, 5, 6, 8 and 10 league games (this season), all games or home-at-home / away-at-away. 180 ranking formulas plus 5
clean-sheet gates. Chosen on 2023-25, judged on 2025-27 (1,057 picks). V4.1 661.
- Both sides' goals scored, last 5 league games: 662 (490 + 172). Equal to V4.1 (+1, range -27 to +30) with only 553 of
  1,057 picks in common. Last 8: also 662 (best on training).
- Goals in both sides' games (scored + conceded): 608 at last 5; best window 629 (last 10).
- Goals conceded only: 548, below a random pick (584). Adding conceded or clean sheets to scoring made every formula worse.
- Clean-sheet gates, against V4.1 picking the same number each weekend: neither side kept a clean sheet 217 of 386 v 246;
  each side 1 or fewer 1,213 of 2,180 v 1,302; 1 or fewer between them 787 of 1,402 v 865; 2 or fewer between them 1,596 of
  2,864 v 1,677. Every gate lost to V4.1.
- Note: V4.1's own last-5 inputs are stored as per-game figures (count divided by games); with 5 games played they rank the
  same as counts.
