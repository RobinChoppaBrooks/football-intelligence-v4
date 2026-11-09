# BTTS audit review: midweek_20261109_1342

Audit version btts_audit_v1, created 2026-11-09 13:46 UTC. Production outputs for this run are unchanged; this file is a second, independent reading of the same evidence.
Fixtures: 21. Flags: none 20, moderate 1.

How to read: the production BTTS verdict is a hand rule (YES exactly when the goal pattern is 'Both teams contribute', which needs an Over 2.5 route for each side).
The audit assessment uses the trained BTTS model band plus the card counts. Neither is overridden; both are listed so each can be scored against the result.
Model bands: High p >= 0.575, Medium p >= 0.514. Evidence score 0 to 30 = each side's scored-in + conceded-in + BTTS counts of 5, with venue adjustments.

## Moderate (1)

### Scarborough Athletic v Marine  (National League North, Tue 10 Nov 19:45 UK)  fixture_id 1587844
- Over 2.5: rejected (model score 0.543). Production BTTS: NO (Medium, p 0.564). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.564) with supporting evidence (score 25, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Scarborough Athletic: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 4/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-4; 2-0; 1-2; 0-2; 2-2. Home last 3: 0-0; 1-2; 2-2 (BTTS 2/3).
- Marine: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-1; 1-0; 1-1; 1-2; 2-4. Away last 3: 2-1; 1-2; 2-4 (BTTS 3/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.564). Scarborough Athletic scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Marine scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

## All fixtures

| fixture_id | kickoff UK | competition | fixture | Over 2.5 | BTTS (prod) | p | audit | evidence | flag | status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1644376 | Fri 13 Nov 20:00 | Copa del Rey | Salamanca UDS v Celta Vigo | rejected | NO (Medium) | 0.555 | NO LEAN | 3 | - | ok |
| 1644370 | Thu 12 Nov 17:30 | Copa del Rey | Calvo Sotelo v Albacete | rejected | NO (Medium) | 0.544 | NO LEAN | 0 | - | ok |
| 1644363 | Thu 12 Nov 18:00 | Copa del Rey | Navalcarnero v Real Betis | rejected | NO (Medium) | 0.552 | NO LEAN | 9 | - | ok |
| 1644379 | Thu 12 Nov 18:00 | Copa del Rey | Tarancón v Levante | rejected | NO (Medium) | 0.555 | NO LEAN | 10 | - | ok |
| 1644336 | Tue 10 Nov 18:00 | Copa del Rey | Anaitasuna v Alaves | rejected | NO (Medium) | 0.543 | NO LEAN | 12 | - | ok |
| 1644365 | Tue 10 Nov 18:00 | Copa del Rey | Pamplona v Eibar | rejected | NO (Medium) | 0.544 | NO LEAN | 0 | - | ok |
| 1644335 | Tue 10 Nov 19:00 | Copa del Rey | Amorebieta v UD Logroñés | rejected | NO (Medium) | 0.544 | NO LEAN | 0 | - | ok |
| 1644362 | Tue 10 Nov 19:00 | Copa del Rey | Mijas Las Lagunas v Real Jaén | rejected | NO (Medium) | 0.544 | NO LEAN | 0 | - | ok |
| 1644382 | Tue 10 Nov 19:00 | Copa del Rey | Trival Valderas v Leganes | rejected | NO (Medium) | 0.544 | NO LEAN | 0 | - | ok |
| 1644380 | Tue 10 Nov 20:00 | Copa del Rey | Tavernes v Valencia | rejected | NO (Medium) | 0.555 | NO LEAN | 7 | - | ok |
| 1647948 | Fri 13 Nov 19:00 | Coupe de France | Dijon v Orleans | rejected | NO (Medium) | 0.543 | NO LEAN | 0 | - | ok |
| 1647959 | Fri 13 Nov 19:00 | Coupe de France | La Neuvillette v Valenciennes | rejected | NO (Medium) | 0.543 | NO LEAN | 0 | - | ok |
| 1647986 | Fri 13 Nov 19:00 | Coupe de France | St-Philbert Gd Lieu v La Roche VF | rejected | NO (Medium) | 0.543 | NO LEAN | 0 | - | ok |
| 1647938 | Thu 12 Nov 18:00 | Coupe de France | Chambéry v Grenoble | rejected | NO (Medium) | 0.543 | NO LEAN | 0 | - | ok |
| 1646814 | Mon 09 Nov 19:30 | FA Cup | Plymouth Parkway v Berkhamsted | Medium | YES (High) | 0.575 | YES | 22 | - | ok |
| 1587888 | Tue 10 Nov 19:45 | National League North | Darlington 1883 v Oxford City | rejected | NO (Medium) | 0.561 | NO LEAN | 21 | - | ok |
| 1587842 | Tue 10 Nov 19:45 | National League North | Morecambe v Hereford | rejected | NO (Medium) | 0.542 | NO LEAN | 20 | - | ok |
| 1587844 | Tue 10 Nov 19:45 | National League North | Scarborough Athletic v Marine | rejected | NO (Medium) | 0.564 | LEAN YES | 25 | moderate | needs review |
| 1588281 | Mon 09 Nov 19:45 | National League South | Chelmsford City v Ebbsfleet United | Medium | NO (Medium) | 0.571 | NO LEAN | 18 | - | ok |
| 1588394 | Tue 10 Nov 19:45 | National League South | Hemel Hempstead Town v Torquay | rejected | NO (Medium) | 0.564 | NO LEAN | 20 | - | ok |
| 1588396 | Tue 10 Nov 19:45 | National League South | Salisbury v Braintree | High | NO (Medium) | 0.555 | NO LEAN | 22 | - | ok |