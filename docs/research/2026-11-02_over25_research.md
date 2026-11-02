# Over 2.5 research, 2 November 2026

Research record for the investigations of 2 November 2026 (Rob, Claude, ChatGPT review). Nothing here changed V4.1: the
selection model, the High and Medium cuts, BTTS, the trump card and every published prediction are as they were. Data and
scripts are in `reports/research/2026-11-02/`. The policy that governs any follow-up is `docs/research_policy.md`.

## Status at a glance

| Finding | Status |
|---|---|
| V4.1 High beat Medium out of sample (69% v 61%, 1,180 and 2,136 fixtures) | Validated before today (over25_backtest_baseline.md); unchanged |
| A two-goal lead reached early is followed by more goals far more often than one reached late | Descriptive fact on 570 exact 2-0 leads; must be built into any 'relentless' measure |
| Some teams keep scoring after 2-0, some stop | Hypothesis: descriptive only, three to nine matches per team |
| Two leaky, goal-contributing teams whose games stay open after the break give more 3+ games | Hypothesis: the open-game filter separates A from C overall but has not shown value beyond the model score |
| Independent weekend A/B shortlist (21 fixtures) | Unsuccessful: 10 of 21 |
| Top 16 rejected fixtures went 12 of 16 on 30 Oct against High 10 of 16 | One weekend only; watched from now on (Top 10 rejected group) |

## 1. Weekend of 30 Oct to 1 Nov (the starting point)

Two runs covered the weekend and were scored separately on 2 Nov.

| Band | V4 run (Thu 29 Oct, weekend_20261029_0917) | V4.1 run (Fri 30 Oct, weekend_20261030_1200) |
|---|---|---|
| High | 16 of 23 | 10 of 16 |
| Medium | 61 of 96 | 13 of 24 |
| rejected | 96 of 147 | 57 of 94 |
| Everything | 173 of 266 | 80 of 134 |

Equal-size comparison on the V4.1 run: the 16 highest-scoring rejected fixtures (model scores 0.555 to 0.580, all just under
the Medium cut of 0.581) went 12 of 16; the top 24 rejected 17 of 24; all 94 rejected 57 of 94; High 10 of 16. In V4.1 no
gate rejected anything (no rejected fixture scored above the Medium cut), so this compares score bands, not rules. One weekend
is well inside normal variation: the backtest already shows the score is flat below the top fifth of the selected band.

BTTS checks on the same run: the verdict mapping (YES = BTTS model High band) and the trump card were verified fixture by
fixture with no mismatch; the clean-sheet caution had not run because it was committed at 13:28 UTC, after the run at 12:03
UTC. It first ran live on 2 Nov.

## 2. Independent weekend A/B shortlist (unsuccessful)

Rob and ChatGPT picked 21 fixtures from the 30 Oct run with a stricter both-sides-score-and-concede filter: tier A 10, tier
B 11. Result: **10 of 21** (A 4 of 10, B 6 of 11). Scores are in `weekend_ab_shortlist_2026-10-30_scored.csv`.

Limitations: 17 of the 21 were already inside V4.1's selected band (6 High went 4 of 6, 11 Medium went 5 of 11), so the
filter mostly re-selected from the model's own picks and did no better than the band they came from (selected overall 23 of
40). The 4 the model had rejected went 1 of 4. The rules were applied by judgement, not written down beforehand, so the test
cannot be repeated exactly. One weekend.

## 3. Defensive vulnerability (hypothesis)

Teams that concede in most games, keep one clean sheet or none and concede 2+ repeatedly may add information beyond the
model, which already uses let-in-2+ counts. Tested only inside the open-game filter (section 6). Distinguishing persistent
weakness from one heavy defeat matters: the filter checks the last ten as well as the last five for that reason.

## 4. Relentless attacking after a lead (descriptive)

Goal events for each team's last 10 league games in the 14 leagues (1,413 fixtures wanted, 1,404 usable; 5 National League
North and South 0-0 games came back without events and 4 games had events that did not add up to the final score). Full
report: `relentless_2026-11-02.md`, `relentless_2026-11-02_teams.csv`, `relentless_2026-11-02_team_matches.csv`.

- 698 two-goal leads: 570 exact 2-0, 128 other (3-1, 4-2), kept separate throughout.
- After an exact 2-0 the leading side scored again in 325 of 570; the match produced another goal from either side in 426 of 570; 144 finished exactly 2-0.
- **Time remaining dominates.** Leading side scored again after a 2-0 reached:

| 2-0 reached | leads | scored again | finished exactly 2-0 |
|---|---|---|---|
| 1 to 30 min | 152 | 121 | 11 |
| 31 to 45 | 133 | 84 | 13 |
| 46 to 60 | 121 | 70 | 28 |
| 61 to 75 | 83 | 37 | 34 |
| 76 and later | 81 | 13 | 58 |

  Any per-team 'relentless' measure must be judged against this timing baseline, otherwise it simply counts early goals,
  which the scored-2+ form the model already uses explains.
- After timing adjustment, teams above expectation (three or more two-goal leads): Torquay, West Ham, Real Madrid, Oxford City, Gillingham, Southampton, Amed, PSV, Boreham Wood, Corum, Fenerbahce, Bayern, Barcelona, RB Leipzig. Teams whose 2-0 tends to stay 2-0: Dundee, Blackburn, Newcastle, Dover, Norwich, Worksop, Cheltenham, Sporting, Wycombe, Stoke. Three to nine matches each: descriptive, not evidence.
- Going two behind: 696 cases, conceded again in 372. 1-0 turned into 3-0 or better: 162 (54 from 1-0 at half time).
- A goal after a lead shows the team scored again, not how hard it attacked; shots and shots on target exist for 11 of the 14 leagues (none for the National League divisions).
- Half-time-only proxy computed before the events arrived (no minutes): 167 cases of 2-0 at half time, a third goal in 100. `relentless_halftime_proxy_2026-11-02.csv`.

## 5. Second-half openness (hypothesis)

Fixtures between two teams that both contribute goals, concede often and keep producing goals after the break, including
after one side leads. Measured from rebuilt scorelines: second-half goals, goals after 60' and 75', and whether a 1-0 or
2-0 reached before 75' was followed by another goal. Part of the open-game filter.

## 6. Open-game A/B/C filter (hypothesis, not validated)

### Definitions, fixed before any result was looked at

For each team, from its last five league games with goal events (one point each unless stated, out of 7):
conceded in 4+ of 5; conceded 2+ in 2+ of 5; 1 or 0 clean sheets; scored in 4+ of 5 (half a point for 3 of 5); at least 6
second-half goals in its games (half for 4 or 5); a goal after the 60th minute in 3+ of 5; after a 1-0, 0-1, 2-0 or 0-2
reached before the 75th minute, another goal by either side in at least two in three of 3+ such cases (half a point for at
least half of 2+ cases). A team 'shuts games down' when it kept 3+ clean sheets or conceded in 2 or fewer of 5. Persistence
over ten games: conceded 2+ in at least 4 in 10 and clean sheets in at most 3 in 10.

- **A**: neither side shuts games down, both score 5.5+ and at least one side's weakness persists over ten.
- **B**: both 4+, or one 5.5+ and the other 3.5+.
- **C**: everything else, or either side shuts games down.

Code: `open_game.py` (production copy, used only for the watchlist), `reports/research/2026-11-02/scripts/opengame_original.py` (the run of 2 Nov).

### Historical test

Chronological: each fixture's category uses only the two teams' previous five games with events; the outcome is the final
score. 639 fixtures, 12 Sep to 1 Nov 2026 (`open_game_history_2026-11-02_original.csv`).

| Category | Over 2.5 | Rate |
|---|---|---|
| A | 130 / 208 | 62.5% |
| B | 138 / 225 | 61.3% |
| C | 107 / 206 | 51.9% |

Inside V4.1's own bands (fixtures that were in the repository's prediction log):

| V4.1 band | A | B | C |
|---|---|---|---|
| rejected | 42 / 72 | 51 / 91 | 44 / 83 |
| Medium | 22 / 33 | 14 / 23 | 14 / 22 |
| High | 6 / 11 | 8 / 9 | none |

Conclusions: A and B performed alike, both above C. Within a V4.1 band the gap is small and the samples are 22 to 91
fixtures, so **the filter has not demonstrated meaningful predictive value beyond the V4.1 model score**. 591 of the 639
fixtures are October games: one season, one short period. Re-running the same definitions with `open_game.py` on every
fixture with events (a team's earlier games that sat only in its opponents' last-10 sets now count) gives 675 fixtures:
A 129 of 209, B 147 of 239, C 118 of 227, the same picture (`open_game_history_2026-11-02_rerun_open_game_py.csv`).

### Midweek 2 to 5 Nov: the seven category A fixtures

From the 14-league midweek run (model scores as published by V4.1):

| Fixture | League | UK kick-off | V4.1 |
|---|---|---|---|
| Charlton v Bolton | Championship | Tue 3 Nov 19:45 | rejected 0.538 |
| Derby v Norwich | Championship | Tue 3 Nov 19:45 | rejected 0.534 |
| Watford v Lincoln | Championship | Tue 3 Nov 19:45 | rejected 0.548 |
| Dorking Wanderers v Hampton & Richmond | National League South | Tue 3 Nov 19:45 | Medium 0.594 |
| Farnborough v Ebbsfleet United | National League South | Tue 3 Nov 19:45 | rejected 0.558 |
| Genclerbirligi v Alanyaspor | Super Lig | Mon 2 Nov 17:00 | rejected 0.544 |
| Deportivo La Coruna v Osasuna | La Liga | Mon 2 Nov 20:00 | rejected 0.539 |

Every team's last five with goal-by-goal progression: `open_game_midweek_breakdown_2026-11-02.txt` and `open_game_midweek_2026-11-02.json`.

## 7. What changed operationally (reporting only)

- Every prediction run writes `reports/research_groups/<run_id>.csv`, frozen at run time: all eligible fixtures ranked by model score, the ten highest-scoring rejected fixtures, and the experimental open-game category.
- The run email adds three sections below the official shortlist: Top 10 rejected fixtures to watch, EXPERIMENTAL open-game watchlist, complete eligible fixture rankings.
- The Monday review adds `reports/performance/research_groups_<date>.md`: official High, official Medium, top 10 rejected, open-game A and all fixtures, scored side by side with overlaps.
- Goal events are pulled for each team's last 10 league games (`download_events.py`, incremental) and kept in the slim database.

## 8. What would be needed before any of this touches selection

Goal events for 2025-26 and earlier 2026-27, a model score for every test fixture, and the chronological comparison set out
in `docs/research_policy.md`: does the signal predict 3+ goals within the same V4.1 score range, at equal selection sizes,
across periods and leagues, with sample sizes and ranges.
