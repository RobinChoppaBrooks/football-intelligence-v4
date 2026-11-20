# Over 2.5 goals model discovery lab: final report
Research only. Production V4.1 untouched. Run 20 Nov 2026 on the repository database (results to 17 Nov 2026). Rob's 14 leagues, league fixtures, FT results only, both sides with 3+ league games this season.

## 1. Executive summary
- **No new formula or model convincingly beats V4.1.** Recommendation: keep V4.1 as the selection engine, unchanged.
- 510,223 formula evaluations and 25 model variants across 12 families were tested. On the untouched 2026-27 season the best challenger (a random forest) won **270 v V4.1's 268** from the top 20 a window (425 picks). The paired range for the difference is -13 to +18: noise.
- The 10 pre-registered formulas won **885 v V4.1's 921** on 2026-27 at identical volume. On 2025-26, where they were chosen, they had led 2919 to 2837. The lead was selection luck and disappeared on fresh data.
- Chance alone manufactures impressive formulas. The same search run on shuffled results (league rates kept, team form destroyed) found a formula winning 173 of 244. That is better than the best real formula at that volume (223 of 324).
- The ceiling is low for every approach. On 2026-27 the base was 810 of 1422 (1 in 1.76). V4.1's top 20 a window won 268 of 425 (1 in 1.59). Pre-match goal counts move the needle a little, and every method hits the same wall.
- Accumulators: no model landed a 15 or 20-fold in any window of 2025-26 or 2026-27. V4.1 5-folds landed in 12 of 86 full windows and 10-folds in 1 of 72.

## 2. Dataset audit
- Source: `football.db` from branch `data` (77,435 fixtures, 70 competitions). No API calls were made. 14 leagues, seasons 2023-24 to 2026-27: 17,783 eligible fixtures, 9,535 finished Over 2.5.
| season   | split          |   eligible fixtures |   Over 2.5 |   Under 2.5 | frequency   |   windows |
|:---------|:---------------|--------------------:|-----------:|------------:|:------------|----------:|
| 2023-24  | development    |                5492 |       2989 |        2503 | 1 in 1.84   |        80 |
| 2024-25  | development    |                5452 |       2786 |        2666 | 1 in 1.96   |        81 |
| 2025-26  | validation     |                5417 |       2950 |        2467 | 1 in 1.84   |        81 |
| 2026-27  | untouched test |                1422 |        810 |         612 | 1 in 1.76   |        25 |
- Quality: 0 duplicate fixture IDs and 0 missing full-time scores in the 14 leagues. 25 playoff ties finishing AET or PEN are excluded as results (FT rule) but kept as form. Teams are keyed by API ID, so there are no name mismatches. Fixtures where either side had fewer than 3 league games are excluded for every model (V4.1's rule), which drops the first weeks of each season.
- Leakage control: every feature uses only league games that kicked off before the fixture, and league rates use only earlier calendar days. An automatic check recomputed 4,000 values from raw results with 0 mismatches. V4.1 scores were rebuilt with production `features.py` and `bands_model.pkl`; 693 of 897 published live rows match the logged score within 0.001. The rest differ only because the live runs saw the data available at run time.
- Limitations: (1) **2026-27 is not pristine.** The 21 Oct, 28 Oct and 19 Nov research sessions already scored other models on it. This lab never tuned on it and opened it once, after `preregistered.json` was committed (commit 541f8d8). (2) V4.1 trained on 2023-24 and 2024-25, so its scores there are in-sample and only 2025-26 and 2026-27 are fair comparisons. (3) 2026-27 is 25 windows, so test ranges are wide. (4) There is no xG, lineups or injuries for most leagues, so the study is goals-based only. (5) Only 4 seasons exist, so league-specific formulas could not be supported.

## 3. Experiments conducted
| experiment                                           |   count |
|:-----------------------------------------------------|--------:|
| Atoms (single count thresholds)                      |     712 |
| Two-condition AND formulas (full grid)               |  253116 |
| Three-condition AND formulas (random, seed 20261120) |   59747 |
| Integer-weight points formulas x 3 cut-offs          |  196605 |
| Decision trees (depth 2 to 4), leaves as rules       |       9 |
| Null searches on shuffled results                    |       3 |
| Formulas shortlisted on DEV and scored on VAL        |    1375 |
| Formulas frozen for the test                         |      10 |
| Model variants (12 families)                         |      25 |
| Walk-forward seasons per fitted model                |       3 |
- Search space: last-5 league counts this season (scored 1+/2+/3+, let in 1+/2+/3+, clean sheets, failed to score, 3+ games, 4+ games, BTTS, both 2+, one side 3+) per side and as sum, min and max; venue last 3; last 10; attack-v-defence routes; drivers20; and the league running rate.
- On VAL only 146 of 1375 shortlisted formulas beat V4.1 at identical volume (33 tied, 1196 worse). Selection rule, finalists and metrics were frozen in `results/preregistered.json` before the test season was opened.

### 12 model families on the validation season (2025-26, top 20 a window, 1,443 picks; V4.1 out of sample here)
| family                                   | model             |   top 20 won |   top 20 picks |   top 5 won |   top 10 won |    brier |
|:-----------------------------------------|:------------------|-------------:|---------------:|------------:|-------------:|---------:|
| 11 Machine learning                      | f11_rf            |          856 |           1443 |         253 |          467 |   0.2451 |
| 6 Momentum (baseline, no momentum terms) | f6_base_logit     |          854 |           1443 |         241 |          463 |   0.2465 |
| V4.1 (locked)                            | v4                |          851 |           1443 |         248 |          456 |   0.2465 |
| 6 Momentum                               | f6_momentum_logit |          847 |           1443 |         253 |          457 |   0.2463 |
| 11 Machine learning                      | f11_hgb           |          844 |           1443 |         240 |          452 |   0.2461 |
| 11 Machine learning                      | f11_hgb_shallow   |          843 |           1443 |         243 |          459 |   0.2457 |
| 11 Machine learning                      | f11_logit_l2      |          839 |           1443 |         240 |          448 |   0.2488 |
| 11 Machine learning                      | f11_logit_l1      |          836 |           1443 |         247 |          447 |   0.2461 |
| 9 Historical match DNA (kNN)             | f9_knn150         |          833 |           1443 |         235 |          455 |   0.2483 |
| 10 Poisson / Dixon-Coles                 | f10_dixon_coles   |          831 |           1443 |         238 |          437 |   0.2556 |
| 10 Poisson / Dixon-Coles                 | f10_poisson       |          831 |           1443 |         238 |          437 |   0.256  |
| 2 Two powerful attacks                   | f2_two_attacks    |          830 |           1443 |         235 |          444 | nan      |
| 1 Attack v Defence collision             | f1_collision      |          820 |           1443 |         218 |          422 | nan      |
| 4 One-sided goal potential               | f4_one_sided      |          816 |           1443 |         239 |          437 | nan      |
| 5 Combined counts (goals, last 10)       | f_goals10         |          816 |           1443 |         239 |          427 | nan      |
| 10 Poisson / Dixon-Coles                 | f10_poisson_s5    |          810 |           1443 |         236 |          434 |   0.2638 |
| 5 Combined counts (drivers20)            | f3b_drivers20     |          809 |           1443 |         235 |          440 | nan      |
| 7 Home/away specialists                  | f7b_venue_blend   |          806 |           1443 |         240 |          432 | nan      |
| 9 Historical match DNA (kNN)             | f9_knn400         |          805 |           1443 |         251 |          454 |   0.2472 |
| 8 Opponent-adjusted                      | f8_opp_adjusted   |          802 |           1443 |         219 |          437 | nan      |
| 7 Home/away specialists                  | f7_venue          |          801 |           1443 |         226 |          419 | nan      |
| 5 Combined counts (Over 2.5 counts)      | f_o25_counts      |          795 |           1443 |         219 |          429 | nan      |
| 4 One-sided goal potential               | f4b_one_sided3    |          793 |           1443 |         222 |          425 | nan      |
| 9 Historical match DNA (kNN)             | f9_knn50          |          781 |           1443 |         215 |          415 |   0.2531 |
| 3 Defensive vulnerability                | f3_defensive      |          754 |           1443 |         220 |          408 | nan      |

## 4. Top 10 formulas (frozen before the test; ranked on VAL; TEST shown as found)
All use only finished league results with kick-off times (`fixtures`: date, teams, FT score; HT not needed). Counts are each side's last 5 league games this season unless stated. 'v V4.1' = V4.1 taking the same number of fixtures in the same windows.

### F01  `h.one3 >= 3 AND h.c2 <= 3 AND max.s2 >= 4`
Home side's last 5 had 3+ games where one team scored 3+; home side let in 2+ in 3 or fewer of 5; at least one side scored 2+ in 4 or 5 of 5.

| season   | split   |   eligible |   selected |   won |   lost | frequency   |   V4.1 same volume won |   v V4.1 |   rejected |   rejected that won |
|:---------|:--------|-----------:|-----------:|------:|-------:|:------------|-----------------------:|---------:|-----------:|--------------------:|
| 2023-24  | DEV     |       5492 |        351 |   229 |    122 | 1 in 1.53   |                    239 |      -10 |       5141 |                2760 |
| 2024-25  | DEV     |       5452 |        251 |   157 |     94 | 1 in 1.60   |                    171 |      -14 |       5201 |                2629 |
| 2025-26  | VAL     |       5417 |        286 |   196 |     90 | 1 in 1.46   |                    188 |        8 |       5131 |                2754 |
| 2026-27  | TEST    |       1422 |        100 |    60 |     40 | 1 in 1.67   |                     63 |       -3 |       1322 |                 750 |
League by league (won of selected): Bundesliga 70 of 97 / 6 of 6; Championship 26 of 42 / 3 of 6; Eredivisie 70 of 95 / 6 of 16; La Liga 29 of 44 / 7 of 8; League One 22 of 40 / 1 of 3; League Two 29 of 54 / 2 of 3; Ligue 1 29 of 43 / 2 of 3; National League 54 of 85 / 11 of 17; National League North 51 of 84 / 5 of 7; National League South 39 of 72 / 8 of 14; Premier League 50 of 73 / 1 of 2; Primeira Liga 34 of 47 / 2 of 6; Scottish Premiership 31 of 42 / 0 of 0; Super Lig 48 of 70 / 6 of 9  (DEV+VAL / TEST)

Robustness: one-step threshold changes beating V4.1: VAL 6 of 6, TEST 0 of 6. Test range for wins: 50 to 69 of 100.
Limitations: Behind V4.1 in both development seasons. Behind V4.1 on TEST.

### F02  `h.o25 >= 5`
Home side's last 5 league games all finished with 3+ goals.

| season   | split   |   eligible |   selected |   won |   lost | frequency   |   V4.1 same volume won |   v V4.1 |   rejected |   rejected that won |
|:---------|:--------|-----------:|-----------:|------:|-------:|:------------|-----------------------:|---------:|-----------:|--------------------:|
| 2023-24  | DEV     |       5492 |        267 |   148 |    119 | 1 in 1.80   |                    186 |      -38 |       5225 |                2841 |
| 2024-25  | DEV     |       5452 |        195 |   102 |     93 | 1 in 1.91   |                    128 |      -26 |       5257 |                2684 |
| 2025-26  | VAL     |       5417 |        254 |   173 |     81 | 1 in 1.47   |                    158 |       15 |       5163 |                2777 |
| 2026-27  | TEST    |       1422 |         75 |    47 |     28 | 1 in 1.60   |                     47 |        0 |       1347 |                 763 |
League by league (won of selected): Bundesliga 54 of 80 / 3 of 7; Championship 20 of 40 / 2 of 5; Eredivisie 49 of 74 / 10 of 16; La Liga 13 of 24 / 6 of 7; League One 25 of 51 / 3 of 4; League Two 19 of 41 / 1 of 2; Ligue 1 20 of 32 / 1 of 1; National League 37 of 68 / 5 of 7; National League North 34 of 64 / 3 of 4; National League South 47 of 76 / 9 of 13; Premier League 46 of 71 / 1 of 1; Primeira Liga 21 of 33 / 1 of 3; Scottish Premiership 16 of 24 / 1 of 2; Super Lig 22 of 38 / 1 of 3  (DEV+VAL / TEST)

Robustness: one-step threshold changes beating V4.1: VAL 0 of 2, TEST 0 of 2. Test range for wins: 39 to 55 of 75.
Limitations: Behind V4.1 in both development seasons. Level with V4.1 on TEST.

### F03  `[sum.s2 - sum.o25 + sum.cs - sum.fts + 2*route.s2c2 + v3sum.o25 + 2*lg.o25x10] >= 29`
Points score of 29 or more: (both sides' Scored 2+) minus (both sides' 3+ games) plus (both sides' clean sheets) minus (both sides' failed to score) plus 2 x (best attack-v-defence route: one side's Scored 2+ plus the other's Let in 2+) plus (both sides' 3+ games in their last 3 at venue) plus 2 x (league's running Over 2.5 rate in tenths).

| season   | split   |   eligible |   selected |   won |   lost | frequency   |   V4.1 same volume won |   v V4.1 |   rejected |   rejected that won |
|:---------|:--------|-----------:|-----------:|------:|-------:|:------------|-----------------------:|---------:|-----------:|--------------------:|
| 2023-24  | DEV     |       5492 |        748 |   467 |    281 | 1 in 1.60   |                    484 |      -17 |       4744 |                2522 |
| 2024-25  | DEV     |       5452 |        479 |   280 |    199 | 1 in 1.71   |                    299 |      -19 |       4973 |                2506 |
| 2025-26  | VAL     |       5417 |        607 |   397 |    210 | 1 in 1.53   |                    375 |       22 |       4810 |                2553 |
| 2026-27  | TEST    |       1422 |        192 |   124 |     68 | 1 in 1.55   |                    126 |       -2 |       1230 |                 686 |
League by league (won of selected): Bundesliga 157 of 224 / 15 of 20; Championship 33 of 64 / 8 of 15; Eredivisie 164 of 248 / 38 of 56; La Liga 38 of 58 / 7 of 10; League One 31 of 68 / 2 of 5; League Two 62 of 112 / 1 of 2; Ligue 1 42 of 77 / 3 of 6; National League 121 of 196 / 22 of 31; National League North 96 of 166 / 2 of 4; National League South 85 of 135 / 9 of 13; Premier League 143 of 220 / 3 of 6; Primeira Liga 65 of 91 / 6 of 10; Scottish Premiership 60 of 95 / 2 of 4; Super Lig 47 of 80 / 6 of 10  (DEV+VAL / TEST)

Robustness: one-step threshold changes beating V4.1: VAL 2 of 2, TEST 0 of 2. Test range for wins: 111 to 136 of 192.
Limitations: Behind V4.1 in both development seasons. Behind V4.1 on TEST.

### F04  `max.s3 >= 3 AND hv3.s2 >= 2`
One side scored 3+ in 3 or more of its last 5; home side scored 2+ in 2 or 3 of its last 3 home games.

| season   | split   |   eligible |   selected |   won |   lost | frequency   |   V4.1 same volume won |   v V4.1 |   rejected |   rejected that won |
|:---------|:--------|-----------:|-----------:|------:|-------:|:------------|-----------------------:|---------:|-----------:|--------------------:|
| 2023-24  | DEV     |       5492 |        411 |   265 |    146 | 1 in 1.55   |                    275 |      -10 |       5081 |                2724 |
| 2024-25  | DEV     |       5452 |        306 |   199 |    107 | 1 in 1.54   |                    198 |        1 |       5146 |                2587 |
| 2025-26  | VAL     |       5417 |        321 |   213 |    108 | 1 in 1.51   |                    204 |        9 |       5096 |                2737 |
| 2026-27  | TEST    |       1422 |         94 |    55 |     39 | 1 in 1.71   |                     59 |       -4 |       1328 |                 755 |
League by league (won of selected): Bundesliga 89 of 117 / 3 of 3; Championship 26 of 48 / 7 of 11; Eredivisie 67 of 88 / 7 of 16; La Liga 31 of 51 / 6 of 8; League One 28 of 50 / 1 of 5; League Two 27 of 58 / 2 of 2; Ligue 1 37 of 53 / 2 of 3; National League 60 of 96 / 6 of 10; National League North 47 of 78 / 2 of 4; National League South 53 of 91 / 9 of 15; Premier League 63 of 98 / 2 of 3; Primeira Liga 56 of 77 / 3 of 5; Scottish Premiership 43 of 55 / 0 of 0; Super Lig 50 of 78 / 5 of 9  (DEV+VAL / TEST)

Robustness: one-step threshold changes beating V4.1: VAL 3 of 4, TEST 1 of 4. Test range for wins: 46 to 64 of 94.
Limitations: Mixed against V4.1 in development. Behind V4.1 on TEST.

### F05  `[2*sum.s2 - sum.fts - route.s2c2 + lg.o25x10] >= 11`
Points score of 11 or more: 2 x (both sides' Scored 2+) minus (both sides' failed to score) minus (best attack-v-defence route) plus (league's running Over 2.5 rate in tenths).

| season   | split   |   eligible |   selected |   won |   lost | frequency   |   V4.1 same volume won |   v V4.1 |   rejected |   rejected that won |
|:---------|:--------|-----------:|-----------:|------:|-------:|:------------|-----------------------:|---------:|-----------:|--------------------:|
| 2023-24  | DEV     |       5492 |        687 |   422 |    265 | 1 in 1.63   |                    455 |      -33 |       4805 |                2567 |
| 2024-25  | DEV     |       5452 |        514 |   312 |    202 | 1 in 1.65   |                    319 |       -7 |       4938 |                2474 |
| 2025-26  | VAL     |       5417 |        640 |   402 |    238 | 1 in 1.59   |                    389 |       13 |       4777 |                2548 |
| 2026-27  | TEST    |       1422 |        210 |   136 |     74 | 1 in 1.54   |                    138 |       -2 |       1212 |                 674 |
League by league (won of selected): Bundesliga 126 of 183 / 14 of 18; Championship 54 of 96 / 12 of 25; Eredivisie 144 of 207 / 28 of 37; La Liga 40 of 77 / 7 of 12; League One 61 of 106 / 4 of 10; League Two 78 of 128 / 6 of 11; Ligue 1 61 of 103 / 4 of 7; National League 112 of 196 / 25 of 32; National League North 93 of 156 / 4 of 9; National League South 86 of 155 / 9 of 12; Premier League 124 of 189 / 3 of 5; Primeira Liga 52 of 77 / 5 of 10; Scottish Premiership 46 of 73 / 5 of 8; Super Lig 59 of 95 / 10 of 14  (DEV+VAL / TEST)

Robustness: one-step threshold changes beating V4.1: VAL 0 of 2, TEST 1 of 2. Test range for wins: 122 to 149 of 210.
Limitations: Behind V4.1 in both development seasons. Behind V4.1 on TEST.

### F06  `sum.fts <= 4 AND v3sum.s2 >= 3 AND l10sum.o25 >= 14`
Both sides together failed to score 4 or fewer times in their last 5; together scored 2+ in 3 or more of their last 3 at venue; together had 14 or more 3+ games in their last 10.

| season   | split   |   eligible |   selected |   won |   lost | frequency   |   V4.1 same volume won |   v V4.1 |   rejected |   rejected that won |
|:---------|:--------|-----------:|-----------:|------:|-------:|:------------|-----------------------:|---------:|-----------:|--------------------:|
| 2023-24  | DEV     |       5492 |        435 |   289 |    146 | 1 in 1.51   |                    289 |        0 |       5057 |                2700 |
| 2024-25  | DEV     |       5452 |        259 |   148 |    111 | 1 in 1.75   |                    181 |      -33 |       5193 |                2638 |
| 2025-26  | VAL     |       5417 |        437 |   277 |    160 | 1 in 1.58   |                    273 |        4 |       4980 |                2673 |
| 2026-27  | TEST    |       1422 |         59 |    41 |     18 | 1 in 1.44   |                     35 |        6 |       1363 |                 769 |
League by league (won of selected): Bundesliga 87 of 139 / 0 of 0; Championship 23 of 35 / 4 of 7; Eredivisie 85 of 125 / 10 of 13; La Liga 20 of 36 / 3 of 4; League One 27 of 55 / 0 of 1; League Two 27 of 42 / 0 of 0; Ligue 1 17 of 32 / 0 of 0; National League 93 of 140 / 14 of 18; National League North 71 of 117 / 3 of 4; National League South 65 of 107 / 1 of 4; Premier League 89 of 144 / 0 of 0; Primeira Liga 37 of 51 / 1 of 2; Scottish Premiership 37 of 55 / 1 of 1; Super Lig 36 of 53 / 4 of 5  (DEV+VAL / TEST)

Robustness: one-step threshold changes beating V4.1: VAL 6 of 6, TEST 6 of 6. Test range for wins: 34 to 47 of 59.
Limitations: Mixed against V4.1 in development. Ahead on TEST, but by a margin smaller than the noise for 1 of 10 frozen formulas; inconclusive.

### F07  `sum.s3 >= 3 AND lg.o25x10 >= 6`
Both sides together scored 3+ in 3 or more of their last 5; league's running Over 2.5 rate rounds to 6 in 10 or higher.

| season   | split   |   eligible |   selected |   won |   lost | frequency   |   V4.1 same volume won |   v V4.1 |   rejected |   rejected that won |
|:---------|:--------|-----------:|-----------:|------:|-------:|:------------|-----------------------:|---------:|-----------:|--------------------:|
| 2023-24  | DEV     |       5492 |        721 |   444 |    277 | 1 in 1.62   |                    467 |      -23 |       4771 |                2545 |
| 2024-25  | DEV     |       5452 |        399 |   242 |    157 | 1 in 1.65   |                    260 |      -18 |       5053 |                2544 |
| 2025-26  | VAL     |       5417 |        506 |   318 |    188 | 1 in 1.59   |                    314 |        4 |       4911 |                2632 |
| 2026-27  | TEST    |       1422 |        242 |   152 |     90 | 1 in 1.59   |                    160 |       -8 |       1180 |                 658 |
League by league (won of selected): Bundesliga 221 of 327 / 21 of 33; Championship 12 of 31 / 20 of 31; Eredivisie 159 of 239 / 26 of 39; La Liga 0 of 0 / 14 of 22; League One 2 of 3 / 6 of 13; League Two 61 of 106 / 0 of 0; Ligue 1 33 of 60 / 9 of 13; National League 106 of 191 / 32 of 51; National League North 106 of 158 / 5 of 10; National League South 57 of 108 / 0 of 0; Premier League 162 of 260 / 2 of 2; Primeira Liga 26 of 42 / 4 of 8; Scottish Premiership 47 of 71 / 3 of 5; Super Lig 12 of 30 / 10 of 15  (DEV+VAL / TEST)

Robustness: one-step threshold changes beating V4.1: VAL 2 of 4, TEST 2 of 4. Test range for wins: 137 to 166 of 242.
Limitations: Behind V4.1 in both development seasons. Behind V4.1 on TEST.

### F08  `sum.s3 >= 2 AND v3sum.s2 >= 3 AND l10sum.o25 >= 11 AND route.s3c3 >= 4`
Both sides together scored 3+ at least twice in their last 5; together scored 2+ in 3+ of their last 3 at venue; together 11+ games with 3+ in their last 10; best 3-goal route (one side Scored 3+ plus other side Let in 3+) 4 or more.

| season   | split   |   eligible |   selected |   won |   lost | frequency   |   V4.1 same volume won |   v V4.1 |   rejected |   rejected that won |
|:---------|:--------|-----------:|-----------:|------:|-------:|:------------|-----------------------:|---------:|-----------:|--------------------:|
| 2023-24  | DEV     |       5492 |        469 |   312 |    157 | 1 in 1.50   |                    325 |      -13 |       5023 |                2677 |
| 2024-25  | DEV     |       5452 |        311 |   197 |    114 | 1 in 1.58   |                    203 |       -6 |       5141 |                2589 |
| 2025-26  | VAL     |       5417 |        380 |   241 |    139 | 1 in 1.58   |                    239 |        2 |       5037 |                2709 |
| 2026-27  | TEST    |       1422 |         81 |    48 |     33 | 1 in 1.69   |                     50 |       -2 |       1341 |                 762 |
League by league (won of selected): Bundesliga 108 of 151 / 3 of 4; Championship 30 of 46 / 6 of 11; Eredivisie 79 of 106 / 10 of 17; La Liga 17 of 36 / 5 of 7; League One 33 of 55 / 0 of 1; League Two 39 of 67 / 0 of 0; Ligue 1 35 of 56 / 0 of 0; National League 78 of 116 / 11 of 16; National League North 55 of 97 / 2 of 4; National League South 65 of 112 / 10 of 14; Premier League 72 of 115 / 0 of 1; Primeira Liga 52 of 68 / 0 of 0; Scottish Premiership 44 of 58 / 0 of 1; Super Lig 43 of 77 / 1 of 5  (DEV+VAL / TEST)

Robustness: one-step threshold changes beating V4.1: VAL 4 of 8, TEST 1 of 8. Test range for wins: 39 to 56 of 81.
Limitations: Behind V4.1 in both development seasons. Behind V4.1 on TEST.

### F09  `hv3.s2 >= 3`
Home side scored 2+ in all of its last 3 home league games.

| season   | split   |   eligible |   selected |   won |   lost | frequency   |   V4.1 same volume won |   v V4.1 |   rejected |   rejected that won |
|:---------|:--------|-----------:|-----------:|------:|-------:|:------------|-----------------------:|---------:|-----------:|--------------------:|
| 2023-24  | DEV     |       5492 |        596 |   362 |    234 | 1 in 1.65   |                    386 |      -24 |       4896 |                2627 |
| 2024-25  | DEV     |       5452 |        495 |   277 |    218 | 1 in 1.79   |                    302 |      -25 |       4957 |                2509 |
| 2025-26  | VAL     |       5417 |        544 |   337 |    207 | 1 in 1.61   |                    335 |        2 |       4873 |                2613 |
| 2026-27  | TEST    |       1422 |        139 |    85 |     54 | 1 in 1.64   |                     87 |       -2 |       1283 |                 725 |
League by league (won of selected): Bundesliga 79 of 118 / 7 of 10; Championship 83 of 131 / 9 of 15; Eredivisie 85 of 128 / 5 of 9; La Liga 54 of 92 / 7 of 10; League One 66 of 121 / 3 of 7; League Two 58 of 112 / 5 of 11; Ligue 1 55 of 90 / 1 of 3; National League 91 of 162 / 17 of 20; National League North 69 of 129 / 11 of 18; National League South 81 of 142 / 9 of 14; Premier League 85 of 143 / 0 of 4; Primeira Liga 57 of 89 / 4 of 7; Scottish Premiership 53 of 76 / 3 of 3; Super Lig 60 of 102 / 4 of 8  (DEV+VAL / TEST)

Robustness: one-step threshold changes beating V4.1: VAL 0 of 2, TEST 0 of 2. Test range for wins: 73 to 96 of 139.
Limitations: Behind V4.1 in both development seasons. Behind V4.1 on TEST.

### F10  `drivers20 >= 8 AND sum.s2 >= 5 AND sum.o35 >= 5`
drivers20 (both Scored 2+ plus both Let in 2+) 8 or more; both sides together Scored 2+ 5 or more; both sides together 5 or more games with 4+ goals.

| season   | split   |   eligible |   selected |   won |   lost | frequency   |   V4.1 same volume won |   v V4.1 |   rejected |   rejected that won |
|:---------|:--------|-----------:|-----------:|------:|-------:|:------------|-----------------------:|---------:|-----------:|--------------------:|
| 2023-24  | DEV     |       5492 |        724 |   450 |    274 | 1 in 1.61   |                    481 |      -31 |       4768 |                2539 |
| 2024-25  | DEV     |       5452 |        487 |   286 |    201 | 1 in 1.70   |                    308 |      -22 |       4965 |                2500 |
| 2025-26  | VAL     |       5417 |        591 |   365 |    226 | 1 in 1.62   |                    362 |        3 |       4826 |                2585 |
| 2026-27  | TEST    |       1422 |        235 |   137 |     98 | 1 in 1.72   |                    156 |      -19 |       1187 |                 673 |
League by league (won of selected): Bundesliga 148 of 214 / 14 of 21; Championship 38 of 73 / 13 of 24; Eredivisie 121 of 195 / 33 of 50; La Liga 43 of 72 / 12 of 18; League One 46 of 84 / 5 of 15; League Two 62 of 119 / 3 of 12; Ligue 1 59 of 89 / 4 of 7; National League 128 of 200 / 17 of 27; National League North 96 of 166 / 5 of 12; National League South 88 of 158 / 19 of 26; Premier League 115 of 178 / 2 of 6; Primeira Liga 56 of 89 / 2 of 6; Scottish Premiership 41 of 64 / 2 of 4; Super Lig 60 of 101 / 6 of 7  (DEV+VAL / TEST)

Robustness: one-step threshold changes beating V4.1: VAL 3 of 6, TEST 0 of 6. Test range for wins: 122 to 151 of 235.
Limitations: Behind V4.1 in both development seasons. Behind V4.1 on TEST.

## 5. Best model for each selection size
Each size's challenger is chosen on VAL (most wins), then read on TEST. Picks per size are identical for every model.
| size            | picks VAL / TEST   | challenger picked on VAL          |   challenger VAL |   V4.1 VAL |   challenger TEST |   V4.1 TEST |
|:----------------|:-------------------|:----------------------------------|-----------------:|-----------:|------------------:|------------:|
| top 5 a window  | 392 / 119          | Random forest (all count windows) |              253 |        248 |                71 |          72 |
| top 10 a window | 758 / 226          | Consensus (rank average of 5)     |              474 |        456 |               140 |         143 |
| top 15 a window | 1111 / 330         | Consensus (rank average of 5)     |              665 |        656 |               204 |         208 |
| top 20 a window | 1443 / 425         | Random forest (all count windows) |              856 |        851 |               270 |         268 |

Verdict: V4.1 is the validated choice at every size. The challengers' margins (largest: +2 on TEST) sit well inside the noise.

## 6. Comparison with V4.1
| model                                             |   TEST top 20 wins v V4.1 |   range low |   range high |   resamples better |   windows |
|:--------------------------------------------------|--------------------------:|------------:|-------------:|-------------------:|----------:|
| Random forest (all count windows)                 |                         2 |         -13 |           18 |              0.586 |        25 |
| Logistic, 11 core counts                          |                        -2 |         -13 |           10 |              0.34  |        25 |
| Logistic + momentum                               |                        -5 |         -19 |            9 |              0.221 |        25 |
| Gradient boosting (V4.1 settings, wider features) |                        -5 |         -18 |            6 |              0.175 |        25 |
| Gradient boosting, shallow                        |                        -8 |         -22 |            4 |              0.109 |        25 |
| Consensus (rank average of 5)                     |                        -2 |         -14 |           11 |              0.359 |        25 |

Live published V4.1 picks (prediction log, 507 unique finished fixtures, 13 runs): V4.1 won 98 of 149. The random forest taking the same number per run would have won 101, with 99 picks in common. That is level.
Calibration (TEST): Brier Random forest (all count windows) 0.2429, Logistic, 11 core counts 0.2441, V4.1 (locked) 0.2428, Logistic + momentum 0.2444, Gradient boosting (V4.1 settings, wider features) 0.2437, Gradient boosting, shallow 0.2436. Lower is better; V4.1 is the best or level. Poisson and Dixon-Coles were the worst calibrated on VAL (Brier 0.2556 v V4.1 0.2465), and the fitted rho went to the edge of its range.

## 7. Recommended implementation
**Keep V4.1 exactly as it is.** Nothing here clears the research policy bar, so no production change is proposed.
If you want one live trial, the only candidate worth the effort is a shadow log (research only, never shown in the pick list):
```
for each run window:
    fit RandomForest(n=400, min_leaf=60, max_features=0.3, seed=20261120) on every finished 14-league fixture before the window
    features = each side's league counts over last 3/5/10 this season, last 10/15 any season, last 3/5 at venue, league running rate
    rank the window's fixtures; log the top 20 beside V4.1's top 20 (fixture_id, rank, score) before kick-off
after results: count wins for both lists on identical windows
```
Second-order reality check before you build it: the per-window difference between two models this similar swings by about 1.6 wins (one standard deviation, from the TEST resampling). Proving a real edge of 1 win every 4 windows would take about 154 windows (about 1.9 seasons at 81 windows a season), and the challenger would need to lead by 39+ wins. A shadow log will very likely finish 'not proven' too. The higher-leverage move is to stop searching for a better pre-match formula from these same inputs.

## 8. Failed hypotheses
| hypothesis                                                | evidence                                                                                                                                                                  |
|:----------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Defensive weakness alone (both Let in 2+)                 | Weakest count family: 754 of 1,443 top-20 picks on VAL v V4.1 851; ranks almost no better than chance.                                                                    |
| Two powerful attacks rule                                 | 830 on VAL; behind V4.1 in both walk-forward seasons.                                                                                                                     |
| Attack v defence collision / drivers20 / one-sided routes | All between 793 and 830 on VAL; the routes are already inside V4.1.                                                                                                       |
| Home/away specialist counts                               | Venue-only drivers20 801, blended 806 on VAL: venue splits add noise, not signal.                                                                                         |
| Opponent-adjusted goals                                   | 802 on VAL; adjusting for opposition quality did not help.                                                                                                                |
| Momentum (last 3 v last 10)                               | Logistic + momentum 847 v the same model without it 854 on VAL, and 263 v 266 on TEST.                                                                                    |
| Historical match DNA (nearest neighbours)                 | Best k=150: 833 on VAL; small k overfits (k=50: 781).                                                                                                                     |
| Poisson and Dixon-Coles                                   | 831 on VAL; worst calibration of the fitted models; the Dixon-Coles correction moved Brier only from 0.2560 to 0.2556.                                                    |
| Model consensus                                           | 843 on VAL, 266 on TEST: agreement did not add accuracy.                                                                                                                  |
| Mined formulas                                            | Best 10 of 510,223 lost to V4.1 on TEST (885 v 921).                                                                                                                      |
| 'Strong attack meets tight defence' explains losses       | Inside V4.1's top 20 (VAL+TEST) that pattern won 252 of 409 (1 in 1.62), the rest 867 of 1459 (1 in 1.68). It does not mark losers, so it should not be used as a filter. |
Losing picks look the same as winning picks on every count. The most common losing scores are 1-1, 1-0 and 2-0: ordinary low-scoring games rather than a pattern a filter could catch.

## 9. Confidence assessment
- **Strong evidence:** V4.1 is not beaten by any approach tested here. Formula mining on these inputs produces mostly chance (null search; VAL to TEST collapse). Accumulators of 10 or more legs essentially never land (0 of 106 full 15 and 20-fold windows for V4.1 over VAL and TEST).
- **Promising but inconclusive:** F06 (+6 on TEST from 59 picks, all 6 threshold variants ahead on VAL and TEST, but 33 behind V4.1 in 2024-25). The random forest (+2 on TEST, +5 on VAL, +3 on the live log).
- **Overfitted:** every mined formula whose development rate looked best. The 10 finalists led V4.1 by 82 on VAL, the season they were picked on, then trailed by 36 on TEST.
- **Insufficient samples:** league-specific rules (most finalists pick fewer than 50 fixtures a season in most leagues); top 5 comparisons (119 TEST picks).

## 10. Next steps
1. Keep V4.1 and its pick process. Nothing here justifies a change.
2. Let the live log keep scoring V4.1. Review per band only once each band has 40+ new results, as the methodology says.
3. If you want more edge, it has to come from information the model does not have (lineups, injuries, rotation), not from new combinations of the same goal counts. That is a data question before a modelling one.
4. Optional: shadow-log the random forest only (one challenger keeps the test honest) from the next run, with the decision rule fixed now: adopt only if it leads V4.1 by 39+ top-20 wins after 154+ windows.

## Files
`scripts/01..09` reproduce everything (`python3 scripts/NN_*.py` in order; seed 20261120; scikit-learn 1.8.0, pandas 3.0, numpy 2.5). `data/features.parquet` is the reusable point-in-time dataset (58,379 league fixtures, all leagues). `results/master_formulas.xlsx` holds every shortlisted formula with DEV, VAL and TEST counts, plus all the tables above. `results/preregistered.json` is the frozen selection.
