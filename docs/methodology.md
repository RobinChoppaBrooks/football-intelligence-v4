# OVER 2.5 MODEL: METHODOLOGY (V4.2)

Version 4.2, 11 November 2026 (Rob's changes; supersedes the V4 lock of 28 October and V4.1 of 30 October). The exact
current rules are in `config/model_config.json` and the history in `docs/changelog.md`; where this file and the config
disagree, the config is right. Benchmarks are in `config/benchmarks.json`, written by `benchmarks.py`. Previous versions
of this file and the code are in the git history of this repository.

## 1. What the system is for
Find fixtures that are credible for 3 or more total goals (Over 2.5). There is no BTTS verdict (removed in V4.2); each
card shows each side's scoring counts instead. Rob makes the final choice of fixtures, and judges prices himself:
bookmaker prices are never used for selection and are not shown.

## 2. Data (API-Football, PRO plan, charged per call)
- Database `football.db`, kept on the branch `data` and refreshed by GitHub Actions (`download.py --results`, about 65 calls).
  Never run a full statistics download without asking. Never schedule daily pulls.
- Competitions: config.py and config/competitions.json (Rob's 14 leagues, the European cups and the domestic cups of
  those countries). FORM_LEAGUES are loaded only so European opponents have domestic form.
- A result counts only when the match finished in normal time (status FT). Extra-time (AET) and penalties (PEN) games
  are not used as form and are not graded, because the stored score on those games is not reliably the 90-minute score.
  Abandoned, awarded and cancelled games never count.
- Predictions use THIS season's results only. Earlier seasons are used only to train and validate.

## 3. Evidence per fixture (counts only: no averages, no percentages, in the model or on the page)
For each side, last 5 completed league games this season, oldest to newest: games with 3+, scored 2+, let in 2+, both
teams scored, scored at least once, conceded at least once, clean sheets, failed to score, goals scored and conceded.
Venue: home side's last home league games, away side's last away league games (sample size shown when fewer).
Division: this season's games with 3+ out of games played, shown as a bar (hot, warm, cold). Supporting evidence.

## 4. How a fixture is selected (the gate)  [do not change without the test in section 11]
A gradient-boosted model trained on 2023-24 and 2024-25 and validated on 2025-26 scores every fixture from 38 counts:
each side's last 5 league games (goals scored, conceded and in total, games with 3+, 4+, BTTS, scored 2+, let in 2+,
clean sheets, failed to score, biggest total in one game, games played), each side's last 3 league games at the venue
(goals scored, conceded and in total, games with 3+, games played) and the competition (games played so far, cup or
league, games with 3+ in its last 50 games this season, games in that window). No input is an average.
- Cut points come from the 2025-26 validation season split into ten equal groups by score: High from the lowest group
  where 65 or more in 100 went 3+, the selection line from the lowest group where 58 or more in 100 did, Weak = the
  bottom quarter of the selected range below High. Stored at 3 decimals and scores compared at 3 decimals, so a printed
  score always shows its band. V4.2: High 0.622+, Medium 0.590 to 0.621, Weak 0.579 to 0.589, rejected 0.578 and below.
- Validation (2025-26, every competition, model bands only): High 1,343 of 2,036 went 3+, Medium 1,811 of 2,959,
  Weak 683 of 1,145, rejected 7,525 of 14,162.
- Fewer than 3 league games for either side = rejected (not enough evidence).
- Trump card (Rob's rule, scored on its own): a side that scored 16+ goals across its last 5 league games carries the
  fixture to High, unless the opponent kept 2 or more clean sheets in its last 5 (both sides need 5 games). BTTS is
  never assumed. Tested on Rob's 14 leagues: 96 of 147 went 3+ on 2023-25, 68 of 87 on 2025-26, 17 of 24 on 2026-27.
- Shown = High, Medium, Weak. Rejected fixtures are listed, not drawn.

## 5. What is explained on each card
- OVER 2.5 YES with confidence High / Medium / Weak and the model score.
- Scoring line, each side: scored in x of 5, failed to score in x, both teams scored in x. No verdict.
- Goal pattern: Both teams contribute / One side dominates / Low scoring, from the counts.
- Catch: clean sheets 2+ of 5, failed to score 2+ of 5, 3+ of 5 under, venue overs 1 or fewer of 3, thin sample.
- Why / Risk / Route lines built from the counts. Match-up lines give goal totals, never per-game figures.
- Colour: green = positive for a 3+ bet, amber = middle, red = danger only.

## 6. Presentation
Shortlist ranked by model score, then cards in league seniority order (config.ORDER), alphabetical by home team.
Rejected fixtures listed by competition at the end. No percentages, no averages; counts are written "3 of 5".

## 7. Logging and review
`data/predictions/predictions_log.csv` gets one row per fixture per run with model_version, every input count,
confidence, trump card, pattern, why and risk. Results go in `data/results/results_log.csv`, written by `run_v4.py review`
(Monday), which reports counts only, split by model version so V4.1 and V4.2 rows are never mixed: High, trump card,
Medium, Weak, rejected, by competition and by count pattern. Extra-time and penalties games are listed as not graded.
Do not change thresholds on one bad week; look for 40+ fixtures per band before moving a cut point.

## 8. Timing
Midweek run Monday 12:30 (Monday to Friday fixtures); weekend run Friday 07:00 (Saturday and Sunday), Europe/London.

## 9. Not available, never invented
Injuries, suspensions, lineups, rotation, weather, xG below the Championship.

## 10. Rob's standing rulings
- No averages anywhere, the model's inputs included. Counts of events only.
- No percentages on the page.
- No bookmaker prices in selection or reports; Rob judges prices himself.
- BTTS is never a verdict and never vetoes Over 2.5.
- Analyse only the fixtures in the run; never add fixtures.
- Keep API calls minimal; results-only refreshes.

## 11. Change control
Any proposed change to selection is tested against the current model on identical chronological out-of-sample
fixtures with counts and by-competition results, kept out of production until Rob approves it, and logged in
docs/changelog.md. The V4.2 side-by-side test against V4.1 is in docs/research/2026-11-11_v4_2_side_by_side.md.

## 12. Research policy (2 November 2026)
- No additional signal, filter, threshold or weighting goes into V4.1 without a meaningful improvement in chronological out-of-sample testing: pre-match information only, equal selection sizes, several periods and leagues, comparison within V4.1 score ranges, value beyond the model score, sample sizes and ranges reported, failed experiments kept. Full text: docs/research_policy.md.
- Research views (top 10 rejected, experimental open-game watchlist, complete rankings) are reporting only and never change a classification. Record of the 2 Nov investigations: docs/research/2026-11-02_over25_research.md.
