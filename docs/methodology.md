# OVER 2.5 MODEL V4: LOCKED METHODOLOGY

Version 4, locked 28 October 2026 (supersedes version 2 of 19 October; that file is kept as versions_FOOTBALL_PREDICTION_RULES_v2_20261028.md). This file is the method. Scripts in this folder implement it; a fresh conversation
reads this file first. Previous versions of the code are kept as `versions_*_v1_20261019.py`.

## 1. What the system is for
Find fixtures Rob supplies that are credible for 3 or more total goals (Over 2.5), and give a separate Both Teams To
Score verdict. Accuracy and selectivity over volume: five strong fixtures beat thirty questionable ones. Rob makes the
final choice of fixtures; the system filters and explains.

## 2. Data (API-Football, PRO plan, charged per call)
- Database `football.db` on Rob's PC (`C:\Users\chopp\Downloads\over25`). The sandbox cannot reach the API.
- Refresh: `py download.py --results` (fixture lists and scores for every competition in config.py, about 65 calls).
  Never run a full statistics download without asking. Never schedule daily pulls.
- Competitions: config.py. English Premier League to Southern Premier (and Division Ones), English cups, Scottish
  Premiership to League Two and cups, Bundesliga, La Liga, Ligue 1, Eredivisie, Primeira Liga, Super Lig, Champions
  League, Europa League, Conference League. FORM_LEAGUES (Serie A, Belgium, etc.) are loaded only so European
  opponents have domestic form; they are never presented on their own.
- Predictions use THIS season's league results only. Earlier seasons are used only to validate rules.

## 3. Evidence per fixture (counts only, never averages or percentages)
For each side, last 5 completed league games this season, oldest to newest:
game had 3+, scored 2+, let in 2+, both teams scored, scored at least once, conceded at least once, clean sheets,
failed to score. Venue: home side's last 5 home league games, away side's last 5 away league games (sample size
shown when fewer). Division: this season's count of games with 3+ out of games played, shown as a ten-block bar
(hot = about two in three or more, warm = more than half, cold = half or fewer). Division rate is supporting
evidence, not the selection criterion.

## 4. How a fixture is selected (the gate)  [LOCKED: do not change without the test in section 11]
A gradient-boosted model trained on 2023-24 and 2024-25 and validated on 2025-26 (walk-forward, no leakage) scores
every fixture from the last-5 league counts, venue-3 counts and division rate. Validation: High band 66% actual 3+,
Medium 62%, rejected 52%. Cut points come from validation deciles, not judgement.
- Shown = High or Medium. Rejected fixtures are listed, not drawn, and are not worth betting (52% actual, break-even
  at typical prices is 55 to 59%).
- "Weak" = bottom quarter of the Medium band; flagged in the catch.
- Hand rules were tested against the model (Oct 2026): the document's STRONG rule hit 61.5% v the model's 67.9%,
  and added nothing inside the model's High band. The model gates; the factors below explain. Any new rule must
  beat the model on history before it changes a verdict.
- Fewer than 3 league games for either side = rejected (not enough evidence).

## 5. What is explained on each card
- OVER 2.5 YES with confidence High / Medium / Weak.
- Goal pattern: Both teams contribute / One side dominates / Low scoring. A route exists when an attack scores 2+ in
  3 of 5 or the opposing defence lets in 2+ in 3 of 5. "Both teams contribute" needs two routes AND each side scoring
  in 4 of 5 and conceding in 3 of 5 (59% BTTS on 2,190 validation fixtures v 55% base).
- BTTS verdict is YES exactly when the pattern is "Both teams contribute", so pattern and verdict can never disagree
  (21 Oct 2026). Likelihood High / Medium / Low comes from a second validated model (High 61%, Medium 55%, Low 50%
  on 2025-26). BTTS is a weak signal in this data: treat as a lean, not a pick.
- Catch: validated warnings only. Clean sheets 2+ of 5, failed to score 2+ of 5, 3+ of 5 under, venue overs 1 or
  fewer of 3, thin sample, Weak. Removed 19 Oct 2026 after testing: "average leans on one big game" (pointed the
  wrong way on 51,551 fixtures).
- Why / Risk / Route lines built from the counts.
- No traffic light on the card. Colour: green = positive for a 3+ bet, amber = middle, red = danger only.

## 6. Presentation
Page 1 shortlist (competition, fixture, kickoff, Over 2.5, confidence, BTTS, likelihood, pattern), alphabetical by
competition then kickoff. Then cards in league seniority order (config.ORDER), alphabetical by home team.
Rejected fixtures listed by competition at the end. No percentages, no averages, no fractions like 4/5 as decoration;
counts are written "3 of 5".

## 7. Logging and review
`predictions_log.csv` gets one row per fixture per run: every input count, both verdicts, confidence, pattern, catch,
why, risk. After results: `py download.py --results`, then `python3 review.py football.db` fills score, Over 2.5
result and BTTS result, and reports hit rates separately for Over 2.5 and BTTS by confidence, competition, pattern
and catch. Do not change thresholds on one bad week; look for 40+ fixtures per band before moving a cut point.
Rob's staking record lives in `slips_YYYYMMDD.csv`.

## 8. Timing
A weekend list is run on Friday after a results pull, a midweek list on the day, so the last 5 includes the most
recent round. Lights set on Wednesday for Saturday are stale.

## 9. Not available, never invented
Injuries, suspensions, lineups, rotation, weather, xG below the Championship, historical odds.

## 10. Rob's standing rulings
- No averages anywhere. Counts of events only.
- No percentage probabilities on the page.
- Analyse only the fixtures supplied; never add fixtures.
- A High on 4 or 5 of 10 dots and a Medium on 8 or more are equals; the catch decides.
- Reds are a filter, not a menu.
- Keep API calls minimal; results-only refreshes.

## 11. V4 lock (28 October 2026)
- Selection engine: the validated model above, unchanged (config and hashes in over25_model_v4_config.json). Classes High / Medium / Weak / rejected.
- Scored 2+ and Let in 2+ for both sides are the most prominent rows on every card; "both attacks 3 of 5+" is highlighted as supporting evidence (Selected 66%, High 71% v 68%) and is never a qualification rule (High fixtures failing a 2-of-5 attacking rule hit 73% on 222).
- V2 alignment (62% Primary + Secondary) and V3 formulas (62 to 66% at comparable sizes; no weighting or weaker-route emphasis helped) were tested on 7,535 out-of-sample fixtures and are not used for selection. Tables: over25_backtest_baseline.md.
- Production report: report_v4.py (summary, ranked selected list, grouped shortlist by date / competition / confidence, cards with the five scorelines, rejected with reasons, coverage, methodology) plus a CSV of every fixture.
- Prediction record: predictions_log.csv, one row per fixture per run with model_version, generated_at, league_id, teams, confidence, both verdicts, all counts and the model score; results filled by review.py after the games. Pre-match rows are never edited.
- Dashboard: review.py reports High / Medium / Weak / selected hit rates, BTTS accuracy, by competition, by Scored 2+ and Let in 2+ counts, both-attacks-3/5+, one-sided v two-way, with sample sizes, against the out-of-sample baseline.
- Change control: any proposed change is tested against this model on identical chronological out-of-sample fixtures with counts, rates, ranges and by-competition results, and must show a meaningful improvement before adoption. Experimental scripts stay out of production. Every change goes in over25_changelog.md.
- Market price at prediction time is recorded when available (download.py --extras pulls all markets into market_odds; fixture_odds holds goals prices).
