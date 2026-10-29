# BTTS classification audit, weekend run 2026-10-29 (run id weekend_20261029_0917)

Audit date 29 October 2026. Audit version btts_audit_v1. Scope: all 274 fixtures in the run, the code that produces the BTTS verdict and likelihood, a recomputation of every last-five count from stored scores, a chronological backtest of the existing logic against alternatives, the run schedules, and a completion manifest. Nothing in the production model, thresholds, features, published predictions or historical results was changed. Every new file sits under a new path.

## 1. Headline

The BTTS verdict in V4 is not produced by the BTTS model. It is a hand rule in analyse_fixtures.py (line 200): the verdict is YES exactly when the Over 2.5 goal pattern is "Both teams contribute", and NO otherwise. That pattern requires an Over 2.5 "route" for each side (an attack scoring 2+ in 3 of 5, or a defence conceding 2+ in 3 of 5). BTTS only needs one goal from each side, so a fixture like Groningen v Sparta Rotterdam, where both sides scored in 5 of 5 and 4 of 5 but one attack has only 2 of 5 with 2+, is called "One side dominates" and therefore BTTS NO. The trained BTTS model (btts_model.pkl) only supplies the High/Medium/Low likelihood word that is printed in brackets. "NO (High)" therefore means: the pattern rule says NO, the model says this is in its strongest YES band.

The pattern carries no BTTS information. "One side dominates" fixtures went BTTS 5,859 of 10,678 (55%) on the 2025-26 validation season and 1,153 of 2,013 (57%) out of sample in 2026-27, which is the base rate in both periods. The rule says NO on 83% of fixtures and those NO calls were right 1,064 of 2,437 (44%) out of sample, worse than a coin flip and worse than calling YES on everything (57%). Since the 19 October legacy runs the live record is the same: NO verdicts correct 136 of 318 (43%), and the 27 fixtures published as "NO (High)" went BTTS 18 times.

Contradictions in this run: 36 severe, 22 moderate, 27 mild, 0 reverse, 7 informational notes, 8 data flags. The 36 severe ones include 15 of the 23 High Over 2.5 selections.

## 2. Code trace (question 1)

Files read: analyse_fixtures.py, btts.py, bands.py, features.py, run_v4.py, report_v4.py, review.py, config/model_config.json.

- features.py builds the rolling counts (last 5 league games this season, last 3 at venue) for every fixture, from FT/AET/PEN matches only.
- btts.py fits a HistGradientBoosting model on the same 38 features as the Over 2.5 model (train 2023-24 and 2024-25, cut points from 2025-26 deciles: High p >= 0.5746, Medium p >= 0.5138). Its docstring says "Verdict YES = HIGH or MEDIUM". That verdict is never used.
- analyse_fixtures.py line 198 computes btts_lab from the model. Line 199 computes the goal pattern in pattern_text(). Line 200: btts_yes = pattern == "Both teams contribute". Line 201 writes btts=YES/NO and btts_lik=the model band. The comment on line 69 records the intent: "The BTTS verdict is YES exactly when this pattern holds, so the two never disagree", meaning the verdict and the pattern never disagree. The verdict and the model disagree constantly.
- pattern_text(): route_h = home scored 2+ in 3 of 5 or away conceded 2+ in 3 of 5; route_a = the mirror; both_scoring = both sides scored in 4 of 5 and both conceded in 3 of 5. "Both teams contribute" needs all three. Anything with one route is "One side dominates", with none is "Low scoring".
- config/model_config.json btts_engine.verdict_rule confirms: "YES when goal pattern is 'both teams contribute'".
- run_v4.py, report_v4.py and review.py carry the verdict through unchanged; review.py scores btts_correct against it.

So yes, the "One side dominates" pattern is directly and incorrectly driving BTTS NO. It is not a leak or a bug in the model; it is the design of the verdict rule. The rule re-stated in btts_rules.py reproduces all 274 verdicts and patterns in this run exactly (rule_replicates_all = true in the audit JSON).

## 3. Recomputation of the evidence (question 2)

Every last-five count was recomputed independently from football.db (stored final scores, league matches this season, kickoff strictly before the fixture) for all 274 fixtures and both sides: scored in, scored 2+, conceded in, conceded 2+, BTTS, clean sheets, failed to score, Over 2.5, and the venue last-three equivalents. Script: reports/btts_audit/scripts in the patch (recompute.py), output reports/btts_audit/2026-10-29/recompute_2026-10-29.csv.

Result: 266 of 274 fixtures reproduce exactly. The 8 differences all have one cause. Four matches this season are recorded with status ABD (abandoned) but carry a partial score: Cove Rangers v East Kilbride 0-1 (24 Oct), Obolon'-Brovar v Kryvbas KR 1-0 (10 Oct), Rayo Vallecano v Athletic Club 0-0 (10 Oct), Barrow v Forest Green 1-0 (24 Oct). analyse_fixtures.last_n() keeps any match with a score (ft_home not null), so each of those teams' cards counts the abandoned match as a result; features.py keeps only FT/AET/PEN, so the model does not. The affected fixtures are Barrow v Eastleigh, Forest Green v Harrogate Town, Airdrie United v Cove Rangers, East Kilbride v Ross County, Athletic Club v Real Sociedad, Rayo Vallecano v Celta Vigo, Kryvbas KR v Dynamo Kyiv, Obolon'-Brovar v Shakhtar Donetsk. None of the eight changes an Over 2.5 classification or a BTTS verdict in this run, but the card and the model are looking at different games. The database holds 13 such matches across all seasons (6 ABD with scores: 4, AWD 8, Canc 1). Proposed fix A (one line, awaiting approval): last_n() filters status to FT/AET/PEN, matching features.py.

No other inconsistency was found: scored 2+ and let in 2+ counts in predictions_2026-10-29.json match the recomputation for all 266 clean fixtures; the four Scottish Cup ties with no league games are correctly shown as 0 of 0 and rejected; the postponed Dundee Utd v Hearts fixture was correctly excluded.

## 4. Contradictions found (questions 3 and 6)

Flag tiers, each with a written explanation in the audit CSV, JSON and review file. Historical BTTS rates are from the backtest in section 6 (validation 2025-26, then out of sample 2026-27).

| tier | rule | this run | historical BTTS rate when this happened |
|---|---|---|---|
| severe | verdict NO while the BTTS model is in its High band | 36 | 641 of 1,081 (59%); 177 of 265 (67%) |
| moderate | verdict NO, model Medium, and both sides BTTS in 4+ of 5 or evidence score 25+ | 22 | 568 of 1,003 (57%); 108 of 186 (58%) |
| mild | verdict NO, model Medium, evidence score 23 or 24 | 27 | 697 of 1,247 (56%); 129 of 241 (54%) |
| reverse | verdict YES while the model is in its Low band | 0 | 22 of 52 (42%); 8 of 12 |
| note | verdict YES with one side BTTS in 2 or fewer of 5 | 7 | 185 of 288 (64%); 34 of 53 (64%) |
| data | an abandoned match with a score inside a last-five window | 8 | n/a |

The disagreement does not prove each prediction wrong, and the historical rates say how often it did: a severe flag meant the NO was wrong (the match went BTTS) about 6 times in 10, a moderate one about 5.7 in 10. The 7 "note" fixtures are not contradictions; the group has historically gone BTTS 64% of the time despite one side's thin BTTS record, so they are listed for information only and their YES stands.

Severe fixtures (36): Alfreton Town v AFC Emley, Gainsborough Trinity v Bamber Bridge, Ilkeston Town v Hyde United, United of Manchester v Lancaster City, Cheshunt v Chatham Town, Leatherhead v Stanway Rovers, Welling United v Carshalton Athletic, Whitehawk v St Albans City, Whyteleafe v Dulwich Hamlet, Wimborne Town v Chippenham Town, Edinburgh City v Dumbarton, Kelty Hearts v Elgin City, Spartans v Annan Athletic, Stirling Albion v Forfar Athletic, Bayer Leverkusen v VfB Stuttgart, Bayern Munich v Borussia Dortmund, Borussia Monchengladbach v SC Paderborn 07, Eintracht Frankfurt v Hamburger SV, SV Elversberg v FSV Mainz 05, Levante v Atletico Madrid, Ajax v AZ Alkmaar, Cambuur v GO Ahead Eagles, Excelsior v Twente, Feyenoord v Fortuna Sittard, Groningen v Sparta Rotterdam, Heerenveen v NEC Nijmegen, PEC Zwolle v ADO Den Haag, PSV Eindhoven v Willem II, Telstar v Utrecht, Cercle Brugge v Antwerp, Charleroi v RAAL La Louviere, St. Truiden v OH Leuven, Aalesund v Sandefjord, Brann v Molde, Fredrikstad v Rosenborg, KFUM Oslo v Ham-Kam.

Cause of each category:

- severe, moderate, mild: all the same mechanism. The verdict is the Over 2.5 pattern, not the BTTS model or the BTTS evidence. The model band and the card counts both say otherwise, to a degree that sets the tier. There is no second cause.
- reverse: would be the same mechanism in the other direction (pattern says YES, model says Low); none this run.
- data: abandoned matches counted as results by last_n(), section 3.
- The remaining 174 NO verdicts without a flag are not evidence-based either. Historically NO has been right 44% to 46% of the time in every period for every rule tested, so they are "unsupported" rather than "contradicted". They are left unflagged so the flag list stays actionable.

## 5. Independent BTTS assessment (question 4)

btts_audit.py writes, for every fixture, an audit_assessment that never overrides the production verdict:

- YES: the BTTS model is in its High band. 990 of 1,627 (61%) on validation, 299 of 449 (67%) out of sample.
- LEAN YES: model Medium, and either both sides have BTTS in 4+ of 5 or the evidence score is 23+. 54% to 58%.
- NO LEAN: everything else. No tested rule found a NO group that was right more than half the time this season (model Low band: 1,650 of 3,294 (50%) on validation, 293 of 521 (56%) out of sample; a side scoring in 2 or fewer of 5: 356 of 628 (57%); a side with 3+ clean sheets: 362 of 646 (56%)), so the honest output is "no lean", not NO.

The evidence score (0 to 30, counts only, no model) is each side's scored-in count plus conceded-in count plus BTTS count out of 5 (clean sheets and failed-to-score are the complements of those), minus 1 for a side that failed to score or kept a clean sheet in 2+ of its last 3 at this venue, plus 1 for a side with BTTS in all 3 at this venue. The lean cut of 23 was chosen on 2023 to 2025 only (first cut with 60% YES precision) and then applied unchanged to 2026-27.

For this run: YES 48, LEAN YES 70, NO LEAN 156. The audit agrees with the production verdict (YES against YES or LEAN YES) on 181 of 274.

## 6. Backtest (question 5)

Data: features rebuilt from football.db for every finished fixture (67,622). The BTTS model was trained on 2023-24 and 2024-25 and had its cut points chosen on 2025-26, so 2025-26 is validation and the only clean out-of-sample period is season 2026-27 (August to 28 October 2026). Rule candidates are not fitted; the evidence cut was chosen on 2023 to 2025. Main table: league fixtures with five league games for both sides. Full tables in reports/btts_audit/backtest/.

Out of sample 2026-27, 2,931 league fixtures, base rate 1,676 of 2,931 (57%):

| rule | YES calls | YES right | YES precision | NO calls | NO right | NO precision | accuracy |
|---|---|---|---|---|---|---|---|
| production pattern rule | 494 | 303 | 61% | 2,437 | 1,064 | 44% | 47% |
| model High only (audit YES) | 449 | 299 | 67% | 2,482 | 1,105 | 45% | 48% |
| model High or Medium (btts.py intent) | 2,410 | 1,383 | 57% | 521 | 228 | 44% | 55% |
| audit YES or LEAN YES | 1,109 | 674 | 61% | 1,822 | 820 | 45% | 51% |
| both sides scoring, no routes (production minus the 2+ test) | 936 | 546 | 58% | 1,995 | 865 | 43% | 48% |
| both sides BTTS 3 of 5+ | 1,165 | 685 | 59% | 1,766 | 775 | 44% | 50% |
| evidence score 23+ | 974 | 580 | 60% | 1,957 | 861 | 44% | 49% |
| model High and evidence 25+ | 198 | 141 | 71% | 2,733 | 1,198 | 44% | 46% |
| always YES | 2,931 | 1,676 | 57% | 0 | 0 | | 57% |
| league rate over 50% | 2,394 | 1,377 | 58% | 537 | 238 | 44% | 55% |

Validation 2025-26, 15,263 league fixtures, base rate 55%: production YES 1,167 of 1,976 (59%), NO 6,040 of 13,287 (45%); model High 990 of 1,627 (61%); audit YES or LEAN YES 2,839 of 4,892 (58%); model High and evidence 25+ 339 of 560 (61%). Train 2023-25, 30,149 fixtures: production YES 58%, model High 63%.

Cup ties out of sample (405): production YES 43 of 76 (57%), model High 77 of 118 (65%), base rate 60%.

Model calibration out of sample by decile: the bottom decile (p below 0.507) went BTTS 54%, the top decile (p 0.586 and above) 67%. The model orders fixtures correctly at the top but cannot find a genuine NO group this season; the base rate has risen from 55% to 57%.

Reading: the model's High band beats the production rule on YES precision in all three periods (63/61/67 against 58/59/61) at a similar number of calls. Nothing beats the base rate on NO. The strongest YES group is model High with evidence 25+, 71% out of sample on 198 fixtures, 61% on validation; that is a small group and the validation figure is the one to trust.

## 7. Schedules (question 10)

Delivery side (Claude scheduled tasks, checked 29 Oct): "Football V4 cloud" review Monday 10:09, midweek Monday 14:09, weekend Thursday 10:09, all CRON_TZ=Europe/London, enabled. The three earlier PC-based tasks are disabled. Correct.

Compute side (.github/workflows/football.yml): cron "30 8 * * 1", "30 12 * * 1", "30 8 * * 4". GitHub cron is UTC only. config/schedules.json says Europe/London 10:00, 14:00, 10:00 "a few minutes early". In GMT (now until 28 March 2027) the runs are 08:30, 12:30 and 08:30 London, 1h39m before delivery. In BST they will be 09:30, 13:30 and 09:30 London, 39 minutes before delivery. Today's weekend run started at 09:17 London for an 08:30 cron (47 minutes of queueing, normal for GitHub schedules); the same delay in BST would land at 10:17, after the 10:09 delivery task, whose four 5-minute waits end at about 10:30. The delivery prompts also say "at 08:30 UTC today", which is only true in winter. Reports are committed before delivery: the commit step runs after run_v4.py and adds reports, data, logs and runs together, and the delivery task checks executions.csv, which is in that same commit. One gap: if run_v4.py fails, the workflow stops before the commit step, so the error row never reaches the repository and the delivery task cannot tell "failed" from "not yet run".

Proposed (patch/proposed/football.yml, diff alongside): two cron entries per slot (GMT and BST variants) with a guard in "Pick the mode" that skips the wrong one using TZ=Europe/London date +%Z, so the model runs at 08:30/12:30/08:30 London all year; the manifest and commit steps run with if: always() so a failed run is recorded; the manifest step and an optional BTTS audit step. Also update config/schedules.json and the three delivery prompts to say 08:30/12:30/08:30 London and to check reports/manifests/latest_<mode>.json.

## 8. Completion manifest (question 11)

write_manifest.py <run_id> writes reports/manifests/<run_id>.json and reports/manifests/latest_<mode>.json: run id, mode, model version, creation time (UTC and London), git commit, fixture window, completion status/start/finish/message from executions.csv, sha256 of both model files, database state (last finished kickoff, counts, scored-but-not-finished matches), fixture counts by classification, every report file with size and sha256 (missing files listed), data-quality warnings (from the run plus the abandoned-match check), and a single boolean complete. Generated for this run: reports/manifests/weekend_20261029_0917.json, complete = true, 5 warnings.

## 9. Recommended corrective changes (question 12: none applied)

1. Approve proposed fix B: btts_yes = btts_lab == "HIGH" in analyse_fixtures.py. One line, same YES/NO schema, so report_v4.py, review.py and the email tasks keep working. Expected effect: YES precision 61% to 67% out of sample at about the same number of YES calls (449 against 494); the 36 severe contradictions disappear by construction. This is what btts.py was written to do.
2. Approve proposed fix A: last_n() ignores abandoned, awarded and cancelled matches, matching features.py.
3. Stop printing a hard NO. Nothing tested predicts NO better than 46%. Show YES / lean YES / no lean (the audit_assessment), and score YES calls only in the weekly review, or keep NO but label it "no lean" in the cards and the email. This needs small changes in report_v4.py, review.py and the delivery prompts, so it is a second step after 1 and 2.
4. Keep the evidence score as the printed explanation, not as the verdict: on its own it is 60% at best; combined with model High it is the strongest group (71% out of sample, 61% validation) and worth tracking for a season before any cut is moved.
5. Apply the workflow proposal (section 7) and update config/schedules.json and the three delivery prompts.
6. Run btts_audit.py and write_manifest.py on every midweek and weekend run so ChatGPT reviews the audit file with the manifest, and score both the production verdict and the audit assessment against results in the Monday review (data/results/results_log.csv already has fixture_id and run_id; the audit CSV joins on both).

## 10. What is in the patch and what is not

New files (no existing file changed): btts_rules.py, btts_audit.py, backtest_btts.py, write_manifest.py, docs/btts_audit_2026-10-29.md, reports/btts_audit/2026-10-29/ (audit CSV, JSON, recomputation CSV), reports/btts_audit/backtest/ (four tables), reports/chatgpt_review/btts_audit_review_2026-10-29_weekend.md, reports/manifests/weekend_20261029_0917.json and latest_weekend.json.

Proposed, not applied, each as a diff under patch/proposed: football.yml (DST guard, manifest, failure recording, optional audit step), analyse_fixtures.py fix A (abandoned matches), analyse_fixtures.py fix B (BTTS verdict from the model band).

Unchanged: bands_model.pkl, btts_model.pkl, bands.py, btts.py, features.py, every threshold in config/model_config.json, reports/weekend/2026-10-29/*, data/predictions/predictions_log.csv, data/results/results_log.csv, predictions_log.csv.
