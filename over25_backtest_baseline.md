# Over 2.5 backtest baseline

The 21 October audit and the 28 October V2/V3 test, unchanged, kept together for reference.

---

# Audit of the 3+ goals selection rules, 21 October 2026

Scope: four live weeks (3 Oct, 10 Oct, 14 to 18 Oct, 19 to 20 Oct) plus chronological out-of-sample tests on history. Model trained on 2023-24 and 2024-25 only. Thresholds are chosen on Aug to Dec 2025 and evaluated on Jan to Jun 2026 and on this season to 18 Oct 2026, never on the same matches. Rates are given with a 95% range; when the ranges of two groups overlap heavily the difference is not established.

Out-of-sample sizes: Jan to Jun 2026 = 5984 fixtures, Aug to Oct 2026 = 3439 fixtures, selection window = 8556.

## 1. High versus Medium

Candidate High cuts were set on the selection window as the lowest score at which the band held a target rate, then applied unchanged to the out-of-sample fixtures.


**Out-of-sample hit rates by band**

| | hit | rate | 95% range |
|---|---|---|---|
| Original (top decile) (cut 0.630), Jan-Jun 26: High | 346 of 492 | 70% | 66 to 74% |
| Original (top decile) (cut 0.630), Jan-Jun 26: Medium | 821 of 1340 | 61% | 59 to 64% |
| Original (top decile) (cut 0.630), Aug-Oct 26: High | 474 of 688 | 69% | 65 to 72% |
| Original (top decile) (cut 0.630), Aug-Oct 26: Medium | 486 of 796 | 61% | 58 to 64% |
| Original (top decile) (cut 0.630), both: High | 820 of 1180 | 69% | 67 to 72% |
| Original (top decile) (cut 0.630), both: Medium | 1307 of 2136 | 61% | 59 to 63% |
| 0.65 (set 21 Oct) (cut 0.650), Jan-Jun 26: High | 161 of 225 | 72% | 65 to 77% |
| 0.65 (set 21 Oct) (cut 0.650), Jan-Jun 26: Medium | 1006 of 1607 | 63% | 60 to 65% |
| 0.65 (set 21 Oct) (cut 0.650), Aug-Oct 26: High | 157 of 217 | 72% | 66 to 78% |
| 0.65 (set 21 Oct) (cut 0.650), Aug-Oct 26: Medium | 803 of 1267 | 63% | 61 to 66% |
| 0.65 (set 21 Oct) (cut 0.650), both: High | 318 of 442 | 72% | 68 to 76% |
| 0.65 (set 21 Oct) (cut 0.650), both: Medium | 1809 of 2874 | 63% | 61 to 65% |
| target 68% on selection window (cut 0.645), Jan-Jun 26: High | 201 of 287 | 70% | 64 to 75% |
| target 68% on selection window (cut 0.645), Jan-Jun 26: Medium | 966 of 1545 | 63% | 60 to 65% |
| target 68% on selection window (cut 0.645), Aug-Oct 26: High | 196 of 271 | 72% | 67 to 77% |
| target 68% on selection window (cut 0.645), Aug-Oct 26: Medium | 764 of 1213 | 63% | 60 to 66% |
| target 68% on selection window (cut 0.645), both: High | 397 of 558 | 71% | 67 to 75% |
| target 68% on selection window (cut 0.645), both: Medium | 1730 of 2758 | 63% | 61 to 65% |
| target 70% on selection window (cut 0.651), Jan-Jun 26: High | 154 of 218 | 71% | 64 to 76% |
| target 70% on selection window (cut 0.651), Jan-Jun 26: Medium | 1013 of 1614 | 63% | 60 to 65% |
| target 70% on selection window (cut 0.651), Aug-Oct 26: High | 152 of 208 | 73% | 67 to 79% |
| target 70% on selection window (cut 0.651), Aug-Oct 26: Medium | 808 of 1276 | 63% | 61 to 66% |
| target 70% on selection window (cut 0.651), both: High | 306 of 426 | 72% | 67 to 76% |
| target 70% on selection window (cut 0.651), both: Medium | 1821 of 2890 | 63% | 61 to 65% |
| One combined Selected band, both OOS | 2127 of 3316 | 64% | 62 to 66% |
| Rejected, both OOS | 3297 of 6107 | 54% | 53 to 55% |

Selected fixtures split into fifths by score, out of sample (does the score rank inside the band?):

| fifth (low to high) | hit | n | rate |
|---|---|---|---|
| 1 | 432 | 664 | 65% |
| 2 | 384 | 663 | 58% |
| 3 | 401 | 663 | 60% |
| 4 | 478 | 705 | 68% |
| 5 | 432 | 621 | 70% |

This season by week, Selected band (High + Medium):

| week | High | Medium | Rejected |
|---|---|---|---|
| w/c 03 Aug | 15/31 | 10/29 | 66/146 |
| w/c 05 Oct | 37/52 | 38/55 | 70/134 |
| w/c 06 Jul | 8/13 | 2/4 | 19/45 |
| w/c 07 Sep | 64/85 | 63/97 | 93/170 |
| w/c 10 Aug | 26/33 | 20/38 | 122/206 |
| w/c 12 Oct | 48/72 | 55/90 | 88/151 |
| w/c 13 Jul | 6/16 | 11/14 | 28/48 |
| w/c 14 Sep | 30/41 | 62/102 | 87/159 |
| w/c 17 Aug | 9/11 | 26/41 | 112/212 |
| w/c 20 Jul | 4/6 | 15/37 | 32/61 |
| w/c 21 Sep | 85/115 | 20/32 | 38/64 |
| w/c 24 Aug | 46/61 | 61/92 | 145/223 |
| w/c 27 Jul | 3/7 | 8/18 | 39/68 |
| w/c 28 Sep | 29/51 | 40/61 | 33/55 |
| w/c 31 Aug | 64/94 | 55/86 | 109/213 |

## Live record, four weeks (as issued)


**Four weeks by light**

| | hit | rate | 95% range |
|---|---|---|---|
| GREEN | 24 of 38 | 63% | 47 to 77% |
| AMBER | 89 of 139 | 64% | 56 to 72% |
| RED | 103 of 193 | 53% | 46 to 60% |

By week:

| week | High | Medium | Rejected |
|---|---|---|---|
| 03 Oct | 4/6 | 17/23 | 13/22 |
| 10 Oct | 2/5 | 24/34 | 28/61 |
| 14 Oct | 15/21 | 36/65 | 38/72 |
| 19 Oct | 3/6 | 12/17 | 24/38 |

## 2. Rejected fixtures that went over

103 of 193 rejected fixtures finished with 3+ (53%).

Why they were rejected (every red is a model score below the Medium cut; the only hard rules are the two caps):

- fewer than 3 league games for a side: 0 fixtures, of which 0 went over
- score below the Medium cut: the rest.

Rejected winners against rejected losers, what the counts looked like:

| | rejected winners | rejected losers |
|---|---|---|
| combined dots (of 10) | 5.12 | 4.49 |
| division share with 3+ | 0.55 | 0.50 |
| home clean sheets | 1.31 | 1.24 |
| away clean sheets | 1.27 | 1.39 |
| home failed to score | 1.40 | 1.51 |
| away failed to score | 1.21 | 1.51 |

By competition (rejected only):

| competition | over | n | rate |
|---|---|---|---|
| Championship | 10 | 16 | 62% |
| League One | 14 | 24 | 58% |
| League Two | 18 | 44 | 41% |
| Ligue 1 | 4 | 7 | 57% |
| National League North | 9 | 16 | 56% |
| National League South | 9 | 17 | 53% |
| Premier League | 4 | 10 | 40% |
| Scottish Championship | 3 | 9 | 33% |
| Scottish League One | 6 | 8 | 75% |
| Scottish Premiership | 5 | 6 | 83% |
| Southern Premier Central | 6 | 10 | 60% |
| Southern Premier South | 5 | 6 | 83% |
| Super Lig | 3 | 5 | 60% |

Rejected fixtures by combined dots (live four weeks):

| dots | over | n |
|---|---|---|
| -1 | 55 | 104 |
| 1 | 0 | 1 |
| 2 | 1 | 6 |
| 3 | 3 | 5 |
| 4 | 11 | 23 |
| 5 | 17 | 27 |
| 6 | 9 | 17 |
| 7 | 4 | 7 |
| 8 | 3 | 3 |

Same question on the out-of-sample history (rejected fixtures):

| | over | n | rate |
|---|---|---|---|
| rejected, dots 8+ | 205 | 359 | 57% |
| rejected, hot division | 91 | 153 | 59% |
| rejected, dots 8+ in hot division | 7 | 15 | 47% |
| rejected, everything else | 3008 | 5610 | 54% |

## 3. Count-based patterns against the model (out of sample)

Each rule selects fixtures from the same out-of-sample pool; the model row is the current Selected band. A rule has to beat the model at a similar size to be useful.


**Rules on the out-of-sample pool (full 5-game samples only)**

| | hit | rate | 95% range |
|---|---|---|---|
| Model Selected (current) | 1528 of 2388 | 64% | 62 to 66% |
| Model High (original cut) | 474 of 679 | 70% | 66 to 73% |
| dots 8+ of 10 | 639 of 1027 | 62% | 59 to 65% |
| dots 9+ of 10 | 164 of 268 | 61% | 55 to 67% |
| both score 2+ in 3 of 5 | 621 of 984 | 63% | 60 to 66% |
| both let in 2+ in 3 of 5 | 519 of 905 | 57% | 54 to 61% |
| two routes (attack 2+ in 3/5 or opp defence 2+ in 3/5, both ways) | 1397 of 2355 | 59% | 57 to 61% |
| both BTTS in 4 of 5 | 340 of 567 | 60% | 56 to 64% |
| venue: home 3 of 3 and away 3 of 3 over | 193 of 299 | 65% | 59 to 70% |
| dots 8+ and hot division | 186 of 266 | 70% | 64 to 75% |
| dots 8+ and no side with 2+ clean sheets | 394 of 650 | 61% | 57 to 64% |
| model Selected and dots 8+ | 489 of 756 | 65% | 61 to 68% |
| model Selected and dots 6 or fewer | 628 of 959 | 65% | 62 to 68% |

Most recent result only (exact scoreline shape of each side's last game), out of sample:

| last game of BOTH sides was | over | n | rate |
|---|---|---|---|
| (exact last-scoreline test needs the per-game sequence, not stored in the feature table; done on the live weeks below) | | | |

Live 14 to 18 Oct, by whether each side's most recent game had 3+:

| | over | n |
|---|---|---|
| both last games 3+ | 31 | 59 |
| one of them | 48 | 74 |
| neither | 10 | 25 |

## 4. BTTS and the goal-distribution pattern (out of sample)


**BTTS**

| | hit | rate | 95% range |
|---|---|---|---|
| all fixtures, BTTS | 4067 of 7233 | 56% | 55 to 57% |
| Both teams contribute: BTTS | 614 of 1033 | 59% | 56 to 62% |
| Both teams contribute: Over 2.5 | 621 of 1033 | 60% | 57 to 63% |
| One side dominates: BTTS | 2854 of 5089 | 56% | 55 to 57% |
| One side dominates: Over 2.5 | 2936 of 5089 | 58% | 56 to 59% |
| Low scoring: BTTS | 599 of 1111 | 54% | 51 to 57% |
| Low scoring: Over 2.5 | 575 of 1111 | 52% | 49 to 55% |
| BTTS model High: BTTS | 566 of 931 | 61% | 58 to 64% |
| BTTS model Medium: BTTS | 3031 of 5402 | 56% | 55 to 57% |
| BTTS model Low: BTTS | 470 of 900 | 52% | 49 to 55% |
| Within model-Selected: pattern Both, BTTS | 402 of 667 | 60% | 57 to 64% |
| Within model-Selected: pattern not Both, BTTS | 996 of 1721 | 58% | 56 to 60% |
| Within fixtures that DID go over: pattern Both, BTTS | 502 of 621 | 81% | 78 to 84% |
| Within fixtures that DID go over: not Both, BTTS | 2779 of 3511 | 79% | 78 to 80% |

## 5. Each catch separately

Question: among fixtures the model selected, does the warning lower the hit rate? Out of sample first, then the two live weeks that logged catches.


**Out of sample, model-Selected fixtures**

| | hit | rate | 95% range |
|---|---|---|---|
| Selected, no warning at all | 224 of 356 | 63% | 58 to 68% |
| Selected with either side 2+ clean sheets | 744 of 1147 | 65% | 62 to 68% |
| Selected without either side 2+ clean sheets | 784 of 1241 | 63% | 60 to 66% |
| Selected with either side 3+ clean sheets | 233 of 374 | 62% | 57 to 67% |
| Selected without either side 3+ clean sheets | 1295 of 2014 | 64% | 62 to 66% |
| Selected with either side failed to score 2+ | 714 of 1085 | 66% | 63 to 69% |
| Selected without either side failed to score 2+ | 814 of 1303 | 62% | 60 to 65% |
| Selected with either side failed to score 3+ | 228 of 335 | 68% | 63 to 73% |
| Selected without either side failed to score 3+ | 1300 of 2053 | 63% | 61 to 65% |
| Selected with either side 3+ of 5 under | 538 of 806 | 67% | 63 to 70% |
| Selected without either side 3+ of 5 under | 990 of 1582 | 63% | 60 to 65% |
| Selected with venue: 1 or fewer of 3 over (either) | 647 of 1028 | 63% | 60 to 66% |
| Selected without venue: 1 or fewer of 3 over (either) | 881 of 1360 | 65% | 62 to 67% |
| Selected with venue: 0 of 3 over (either) | 90 of 131 | 69% | 60 to 76% |
| Selected without venue: 0 of 3 over (either) | 1438 of 2257 | 64% | 62 to 66% |

**Live 14 to 20 Oct, shown fixtures**

| | hit | rate | 95% range |
|---|---|---|---|
| no catch | 7 of 10 | 70% | 40 to 89% |
| any catch | 59 of 99 | 60% | 50 to 69% |
| with 'clean sheets' | 33 of 55 | 60% | 47 to 72% |
| with 'failed to score' | 26 of 48 | 54% | 40 to 67% |
| with '3/5 under' | 22 of 38 | 58% | 42 to 72% |
| with 'venue 1/3 or fewer' | 30 of 46 | 65% | 51 to 77% |
| with 'thin venue sample' | 9 of 13 | 69% | 42 to 87% |
| with 'match-up contradicts (Mixed)' | 7 of 10 | 70% | 40 to 89% |
| with 'goals rely on poor defending (Chaos)' | 3 of 3 | 100% | 44 to 100% |

## 6. By competition, out of sample, Selected band

| competition | over | n | rate | rejected rate |
|---|---|---|---|---|
| Champions League | 70 | 111 | 63% | 55% (n=96) |
| Europa League | 14 | 30 | 47% | 54% (n=167) |
| Championship | 16 | 25 | 64% | 53% (n=377) |
| League One | 21 | 40 | 52% | 53% (n=364) |
| National League | 88 | 146 | 60% | 61% (n=272) |
| FA Cup | 192 | 292 | 66% | 56% (n=86) |
| EFL Trophy | 54 | 74 | 73% | 60% (n=5) |
| FA Trophy | 129 | 196 | 66% | 58% (n=19) |
| National League North | 69 | 113 | 61% | 58% (n=300) |
| National League South | 26 | 41 | 63% | 54% (n=366) |
| Isthmian Div One North | 33 | 48 | 69% | 53% (n=154) |
| Isthmian Div One South Central | 105 | 156 | 67% | 58% (n=24) |
| NPL Div One West | 34 | 64 | 53% | 63% (n=134) |
| Southern Div One South | 79 | 128 | 62% | 44% (n=54) |
| Isthmian Div One South East | 113 | 173 | 65% | 86% (n=7) |
| Isthmian Premier | 165 | 252 | 65% | 66% (n=91) |
| Northern Premier League | 49 | 74 | 66% | 51% (n=269) |
| Southern Premier South | 130 | 203 | 64% | 56% (n=142) |
| Bundesliga | 122 | 180 | 68% | 66% (n=47) |
| Eredivisie | 120 | 185 | 65% | 68% (n=53) |
| Scottish Cup | 25 | 47 | 53% | 50% (n=14) |
| Scottish Challenge Cup | 92 | 127 | 72% | 75% (n=8) |
| Scottish League Two | 34 | 60 | 57% | 59% (n=87) |
| Scottish League Cup | 40 | 72 | 56% | 60% (n=20) |
| Conference League | 37 | 61 | 61% | 53% (n=260) |
| Southern Premier Central | 40 | 71 | 56% | 54% (n=269) |
| Southern Div One Central | 141 | 198 | 71% | 100% (n=2) |
## 7. Conclusions: current method against proposals

| Question | Current method | Proposal tested | Verdict | Evidence |
|---|---|---|---|---|
| Does High beat Medium? | High = top decile (0.630) | one combined Selected band; higher cuts (0.645, 0.650, 0.651) | **High is real on history**: 69% v 61%, ranges 67-72 v 59-63 do not overlap, 1,180 v 2,136 out-of-sample fixtures, and it held in both halves (Jan-Jun 26 and Aug-Oct 26). Live four weeks (24 of 38 v 89 of 139) does not contradict it; the live High range is 47 to 77%. Higher cuts gain 2 to 3 points, ranges overlap, and lose 60% of High fixtures: **not established**. | keep two tiers; revisit at 100 live High |
| Does the score rank inside Selected? | | fifths by score | top fifth 70%, bottom fifth 65%, middle fifths 58 to 60%: the score ranks at the top but is flat below it | ranking within Medium is not meaningful; High v Medium is |
| Are rejection rules producing false negatives? | model score below the Medium cut; caps for thin data | | no hard rule rejected a winner (0 cap rejections in four weeks). Rejected winners had slightly more dots (5.1 v 4.6 of 10) and sat in slightly hotter divisions. On history, rejected with 8+ dots = 57%, rejected in a hot division = 59%: both below the Medium band (61 to 63%), so promoting them would dilute Selected | no change |
| Rejected by competition | | | **finding**: in Bundesliga (66%), Eredivisie (68%), Isthmian Premier (66%), National League (61%) and Scottish Challenge Cup (75%) the rejected fixtures hit as often as Medium does elsewhere. The model's cut is one line across all divisions and under-selects in hot divisions. Live: Scottish Premiership 5 of 6 rejected went over, Southern Premier South 5 of 6, Scottish League One 6 of 8 (tiny samples) | proposal: test a per-division cut on the selection window, evaluate out of sample before deploying |
| Do count patterns beat the model? | GBM on counts | 11 count rules (dots 8+, both score 2+, both let in 2+, two routes, both BTTS 4 of 5, venue 3 of 3 each, combinations) | none beats Model High (70%). "dots 8+ in a hot division" matches it at 70% (n=266, range 64-75); the rest are 57 to 65%. Inside Selected, dots do not separate (65% v 65%) | no change; the dots rule for near-equal High/Medium picks is not supported inside the Selected band |
| Most recent scoreline | | both sides' last game had 3+ | live week only (n=158): both 53%, one 65%, neither 40%; no signal, sample too small | insufficient evidence |
| BTTS pattern | verdict follows "Both teams contribute" | | pattern Both = 59% BTTS (56-62), One side = 56%, Low = 54%: ordered correctly but small gaps. Independent of Over 2.5 it adds nothing: among games that did go over, Both 81% v not-Both 79%. The BTTS model separates a little more (High 61%, Low 52%, non-overlapping) | BTTS stays experimental; no edge established beyond a few points |
| Catches | shown as danger in red | each catch tested alone on 2,388 out-of-sample Selected fixtures | **none lowers the hit rate**: no-warning 63%; clean sheets 2+ 65%; 3+ 62%; failed to score 2+ 66%, 3+ 68%; 3 of 5 under 67%; venue 1 of 3 or fewer 63%; venue 0 of 3 69%. Live 14-20 Oct: any catch 60% v none 70% (n=10) | proposal: stop presenting these as danger. Keep the counts on the card (clean sheets, failed to score) as information in neutral colour; drop the red "catch" line, or rename it "notes" |
| Weak-amber flag | bottom quarter of Medium flagged | | bottom fifth of Selected hit 65% out of sample, not worse than the middle | proposal: drop the flag |
| By competition, Selected band | | | weak: Europa League 47% (n=30), League One 52% (n=40), NPL Div One West 53%, Southern Premier Central 56%, Scottish League Two 57%. Strong: EFL Trophy 73%, Scottish Challenge Cup 72%, Southern Div One Central 71%, Isthmian Div One North 69%, Bundesliga 68% | report alongside the cards; a per-division cut would address both ends |

**Deployed today and reverted:** the High cut was moved to 0.650 at 11:53 and put back to 0.630 at the end of this audit. The 21 to 25 October cards were issued with the 0.650 cut (9 High); under the original cut they would show more High fixtures. Nothing else changed. All proposals above are untested in production and wait on your decision.


---

# V3 scoring test, 28 October 2026

Out of sample: Jan to Jun 2026 and Aug to Oct 2026, 7,535 fixtures with full five-game samples, 57% base rate. Score cut points set on Aug to Dec 2025 only. Ranges are 95%.

| Method | selected | hit 3+ | range | winners rejected |
|---|---|---|---|---|
| A. Model High | 729 | 69% | 66-72 | 88% |
| A. Model Selected (High + Medium) | 2,518 | 64% | 62-66 | 63% |
| B. V2 Primary | 87 | 62% | 52-72 | 99% |
| B. V2 Primary + Secondary | 710 | 62% | 59-66 | 90% |
| C. V3 70/30, top fifth of hard-rule passers | 701 | 63% | 59-67 | 90% |
| C. V3 70/30, top tenth | 321 | 63% | 58-68 | 95% |
| C. V3 60/40 top fifth / top tenth | 703 / 319 | 64% / 64% | | |
| C. V3 80/20 top fifth / top tenth | 692 / 307 | 63% / 64% | | |
| C. geometric mean top fifth / top tenth | 722 / 304 | 62% / 66% | | |

Weighting the weaker route: fifths by MIN of routes 54 / 57 / 57 / 59 / 59%; by MEAN 53 / 57 / 58 / 58 / 61%; by MAX 53 / 57 / 57 / 58 / 61%. No gain from MIN.

Hard rule (both scored 2+ in at least 2 of 5): passes 59%, fails 55%. Inside the model it adds nothing: Selected & passes 64%, Selected & fails 64%; High & passes 67%, High & fails 73% (222 fixtures). The rule would remove the model's best fixtures.

Threshold grid (both sides): scored 2+ >= 3 gives 64% (847) whatever the let-in threshold; let-in thresholds alone give 58 to 59%. Scoring form carries the signal; conceding form does not.

Inside the model: Selected & both attacks 3 of 5+ = 66% (669); one side = 62% (1,324); neither = 65% (525). High & both = 71% (245); High & not both = 68% (484).

One-sided strong route (other side scored 2+ in 0 or 1 of 5): 57% (737); with model Selected 60% (357). Below Selected.

By league (40+ model selections), model v V3 top fifth: V3 ahead in National League 73% v 63% (49 v 125), Isthmian Premier 73 v 66, Bundesliga 73 v 66, National League South 74 v 71, Southern Premier Central 62 v 54; behind in NPL Div One West 41 v 52, Scottish League Two 50 v 59, Champions League 60 v 70. V3 samples are 10 to 55 per league; none of these gaps is outside the ranges.

Recommendation: the validated model remains the strongest defensible gate (69% High, 64% Selected). V3 does not improve on it under any weighting, the weaker-route emphasis does not rank better, and the hard rule would discard a 73% slice. Both-attacks-3-of-5 is worth showing as information (a few points inside the bands) but not as a gate. The one-sided category is information only. Nothing deployed as a selection rule; the recommended shortlist is the model's, with the attacking counts printed on every card.
