# V4.2 side-by-side test against V4.1 (11 November 2026)

Rob's V4.2 changes: no averages in the model (every input a count), FT-only results, the whale trump card, no BTTS model,
cut points stored at 3 decimals. This file is the change-control test (methodology section 11): identical fixtures,
counts only. Data: football.db from branch `data`, results to 8 Nov 2026. Training 2023-24 and 2024-25, cut points set
on 2025-26, so 2026-27 is the only season neither model has seen in any way.

Engines compared, all classified as production does (fewer than 3 league games for a side = rejected, trump card on
its own row, using the V4.2 whale rule for all three so only the model differs):
- V4.1 locked: the current bands_model.pkl (38 inputs including per-game averages and the division's 3+ share), cut points rounded to 3 decimals.
- V4.1 engine, FT-only refit: the same 38 V4.1 inputs retrained on FT-only results, new cut points by the same rule.
- V4.2 counts: the new model, 38 counts, no averages.

Each cell: fixtures that went 3+ out of fixtures in the band.

## Rob's 14 leagues, 2026-27 (live, unseen by every engine)

| Engine | High | Medium | Weak | Trump card | rejected | All selected |
|---|---|---|---|---|---|---|
| V4.1 locked | 74 of 108 | 92 of 148 | 54 of 83 | 17 of 24 | 807 of 1461 | 237 of 363 |
| V4.1 engine, FT-only refit | 77 of 114 | 69 of 118 | 47 of 77 | 17 of 24 | 834 of 1491 | 210 of 333 |
| V4.2 counts | 53 of 93 | 102 of 157 | 56 of 95 | 17 of 24 | 816 of 1455 | 228 of 369 |

## Rob's 14 leagues, 2025-26 (the season the cut points were set on)

| Engine | High | Medium | Weak | Trump card | rejected | All selected |
|---|---|---|---|---|---|---|
| V4.1 locked | 58 of 93 | 255 of 427 | 164 of 269 | 68 of 87 | 2639 of 4988 | 545 of 876 |
| V4.1 engine, FT-only refit | 42 of 72 | 237 of 392 | 124 of 220 | 68 of 87 | 2713 of 5093 | 471 of 771 |
| V4.2 counts | 112 of 174 | 296 of 499 | 184 of 338 | 68 of 87 | 2524 of 4766 | 660 of 1098 |

## Cups (European and domestic), 2026-27

| Engine | High | Medium | Weak | Trump card | rejected | All selected |
|---|---|---|---|---|---|---|
| V4.1 locked | 31 of 44 | 91 of 147 | 36 of 57 | 8 of 11 | 730 of 1185 | 166 of 259 |
| V4.1 engine, FT-only refit | 33 of 48 | 89 of 136 | 27 of 49 | 8 of 11 | 739 of 1200 | 157 of 244 |
| V4.2 counts | 61 of 102 | 98 of 148 | 22 of 35 | 8 of 11 | 707 of 1148 | 189 of 296 |

## Cups, 2025-26

| Engine | High | Medium | Weak | Trump card | rejected | All selected |
|---|---|---|---|---|---|---|
| V4.1 locked | 59 of 85 | 141 of 228 | 75 of 119 | 15 of 22 | 1001 of 1684 | 290 of 454 |
| V4.1 engine, FT-only refit | 46 of 73 | 151 of 223 | 57 of 100 | 15 of 22 | 1022 of 1720 | 269 of 418 |
| V4.2 counts | 86 of 137 | 187 of 313 | 54 of 92 | 15 of 22 | 949 of 1574 | 342 of 564 |

## Equal-size test (no rejection gate, no trump card): best fixtures by score


### 2025-26 (validation season), 14 leagues: 5864 fixtures, 3184 went 3+

| Band | V4.1 (averages) | V4.2 (counts) |
|---|---|---|
| High | 102 of 154 | 151 of 222 |
| Medium | 298 of 488 | 313 of 521 |
| Weak | 175 of 283 | 187 of 343 |
| rejected | 2609 of 4939 | 2533 of 4778 |
| Best 10 in 100 by score | 363 of 586 | 365 of 586 |
| Best 20 in 100 by score | 724 of 1172 | 701 of 1172 |
| Best 30 in 100 by score | 1048 of 1759 | 1025 of 1759 |

### 2025-26 (validation season), cups: 2138 fixtures, 1291 went 3+

| Band | V4.1 (averages) | V4.2 (counts) |
|---|---|---|
| High | 471 of 705 | 375 of 589 |
| Medium | 234 of 389 | 569 of 948 |
| Weak | 103 of 167 | 75 of 126 |
| rejected | 483 of 877 | 272 of 475 |
| Best 10 in 100 by score | 142 of 213 | 137 of 213 |
| Best 20 in 100 by score | 283 of 427 | 279 of 427 |
| Best 30 in 100 by score | 423 of 641 | 404 of 641 |

### 2026-27 live, to 8 Nov, 14 leagues: 1824 fixtures, 1044 went 3+

| Band | V4.1 (averages) | V4.2 (counts) |
|---|---|---|
| High | 122 of 181 | 65 of 110 |
| Medium | 122 of 200 | 107 of 162 |
| Weak | 67 of 101 | 57 of 96 |
| rejected | 733 of 1342 | 815 of 1456 |
| Best 10 in 100 by score | 123 of 182 | 112 of 182 |
| Best 20 in 100 by score | 231 of 364 | 227 of 364 |
| Best 30 in 100 by score | 342 of 547 | 329 of 547 |

### 2026-27 live, to 8 Nov, cups: 1444 fixtures, 896 went 3+

| Band | V4.1 (averages) | V4.2 (counts) |
|---|---|---|
| High | 322 of 504 | 300 of 505 |
| Medium | 203 of 326 | 453 of 722 |
| Weak | 68 of 100 | 39 of 59 |
| rejected | 303 of 514 | 104 of 158 |
| Best 10 in 100 by score | 91 of 144 | 91 of 144 |
| Best 20 in 100 by score | 183 of 288 | 179 of 288 |
| Best 30 in 100 by score | 272 of 433 | 265 of 433 |

## Whale trump card (16+ goals in a side's last 5 league games, opponent kept fewer than 2 clean sheets), FT-only data

| | 2023-25 | 2025-26 | 2026-27 |
|---|---|---|---|
| Whale, 14 leagues | 96 of 147 | 68 of 87 | 17 of 24 |
| Ignored because opponent kept 2+ clean sheets, 14 leagues | 65 of 106 | 18 of 29 | 11 of 17 |
| Old V4.1 trump card, 14 leagues | 17 of 30 | 12 of 21 | 3 of 4 |
| Whale, cups | 39 of 57 | 15 of 22 | 8 of 11 |

## Reading

- Across everything it selects, V4.2 lands about where V4.1 does on 2026-27 (14 leagues: 228 of 369 against 237 of 363),
  and selects more in cups with the same strike (189 of 296 against 166 of 259).
- The V4.2 High label is weaker on 2026-27 (53 of 93 against 74 of 108) while its Medium is stronger (102 of 157 against
  92 of 148). On 2025-26 the V4.2 High band was stronger (112 of 174 against 58 of 93). The High band is not yet a
  reliable step above Medium in either engine; treat the selected fixtures as one pool until it is.
- At the very top (best 10 and 20 in 100) V4.2 trails V4.1 by a few fixtures per 100 on 2026-27. That is the cost of
  the no-averages rule measured on unseen games.
- Rob's decision, 11 Nov 2026: no averages in any prediction. V4.2 is not merged until he approves this test.
