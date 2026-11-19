# Model pressure test for fixture picking (19 Nov 2026, research only, V4.1 unchanged)

Rob's brief: test model variants like V4.1 against season data and find the best fixture picker. Target chosen by Rob:
highest 3+ goals hit rate on unseen seasons; each model sets its own cut-off. Fair comparison also at a fixed top 20, 30 and 50 a weekend.

Method: walk-forward (train on earlier seasons only, test on 2024-25, 2025-26, 2026-27 to 19 Nov). Picks: Rob's 14 leagues, Friday
to Sunday, both sides with 3+ league games. Training data: Rob's leagues and cups (and, in two variants, every league in the database).
"Own cut-off" is set on the previous season so it averaged at least 20 picks a weekend. Paired weekend resampling for ranges.
Note: V4.1 as published trained on 2023-24 and 2024-25, so its 2024-25 score is flattered; the clean head-to-head uses 2025-26 and 2026-27.

## Top 20 a weekend, all three test seasons (1,868 picks)
| Model | Hits |
|---|---|
| Blend: all-features + logistic + last-10 + V4.1 recipe | 1,143 |
| V4.1 recipe trained on every league in the database | 1,141 |
| V4.1 as published (2024-25 flattered) | 1,139 |
| HGB on all 300+ features | 1,135 |
| V4.1 recipe refitted walk-forward | 1,106 |
| Counts-only model (no averages) | 1,075 |
| Rule: Scored 2+ plus Let in 2+ counts | 1,059 |
| Rule: two routes (attack v defence) | 1,040 |
Full tables: h_res.csv, h2_res.csv, h3_res.csv (also top 30, top 50, own cut-off, by season).

## Clean head-to-head v V4.1 as published (2025-26 and 2026-27, 53 weekends, 1,057 picks)
Best: blend of all-features + logistic + last-10, 673 v 661 (12 more hits; range -6 to +31; better in 85 of 100 resamples): not proven.
Capping picks at 4 a league cost 19 to 26 hits. Counts-only, simple rules, deeper or slower trees, league identity and recency
weighting did not beat V4.1 (clean_h2h.csv).

## Market benchmark (prices; outside the no-prices rule, reference only)
Priced leagues, 2025-26 and 2026-27, top 20 a weekend (1,037 picks): market fair chance 676, best blend 650, V4.1 636.
Blending 75% market rank with 25% best-blend rank: 514 of 793 (2024-25), 512 of 798 (2025-26), 164 of 239 (2026-27), against the
blend alone 452, 493, 157. Highest hit rate is not highest profit: short prices hit more and pay less (see docs/research/v5_short_overs).
