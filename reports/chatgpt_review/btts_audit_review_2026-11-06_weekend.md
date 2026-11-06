# BTTS audit review: weekend_20261106_0807

Audit version btts_audit_v1, created 2026-11-06 08:09 UTC. Production outputs for this run are unchanged; this file is a second, independent reading of the same evidence.
Fixtures: 130. Flags: none 91, moderate 13, note 13, mild 11, severe 2.

How to read: the production BTTS verdict is a hand rule (YES exactly when the goal pattern is 'Both teams contribute', which needs an Over 2.5 route for each side).
The audit assessment uses the trained BTTS model band plus the card counts. Neither is overridden; both are listed so each can be scored against the result.
Model bands: High p >= 0.575, Medium p >= 0.514. Evidence score 0 to 30 = each side's scored-in + conceded-in + BTTS counts of 5, with venue adjustments.

## Severe (2)

### Bromley v Rotherham  (FA Cup, Sat 07 Nov 15:00 UK)  fixture_id 1646795
- Over 2.5: Medium (model score 0.619). Production BTTS: NO (Medium, p 0.575). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.575 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Bromley: scored in 3/5, 2+ in 1/5, conceded in 5/5, 2+ against in 3/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 0-1; 0-4; 1-1; 1-4; 2-3. Home last 3: 2-1; 0-4; 1-1 (BTTS 2/3).
- Rotherham: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 5/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-4; 0-2; 2-2; 3-3; 1-2. Away last 3: 0-1; 0-2; 1-2 (BTTS 1/3).
- Evidence score: 23. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.575). Bromley scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5; Rotherham scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Wimborne Town v Crawley Town  (FA Cup, Sun 08 Nov 15:00 UK)  fixture_id 1646817
- Over 2.5: Medium (model score 0.628). Production BTTS: NO (Medium, p 0.575). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.575 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Wimborne Town: scored in 4/5, 2+ in 3/5, conceded in 2/5, 2+ against in 2/5, BTTS 2/5, clean sheets 3/5, failed to score 1/5. Last five: 6-3; 1-2; 3-0; 0-0; 2-0. Home last 3: 6-3; 3-0; 2-0 (BTTS 1/3).
- Crawley Town: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-2; 1-2; 2-3; 1-1; 1-0. Away last 3: 0-2; 1-2; 1-0 (BTTS 1/3).
- Evidence score: 20. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.575). Wimborne Town scored in 4 of 5, conceded in 2 of 5, BTTS 2 of 5; Crawley Town scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

## Moderate (13)

### West Brom v Millwall  (Championship, Sat 07 Nov 15:00 UK)  fixture_id 1563261
- Over 2.5: rejected (model score 0.577). Production BTTS: NO (Medium, p 0.566). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.566) with supporting evidence (score 26, both sides BTTS at least 3 of 5); 55% to 59% historically.
- West Brom: scored in 5/5, 2+ in 3/5, conceded in 5/5, 2+ against in 1/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-1; 3-2; 1-1; 3-1; 1-1. Home last 3: 0-1; 3-2; 1-1 (BTTS 2/3).
- Millwall: scored in 3/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 0-1; 2-2; 1-2; 4-1; 0-3. Away last 3: 1-0; 1-2; 0-3 (BTTS 1/3).
- Evidence score: 26. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 26). Model Medium (p 0.566). West Brom scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Millwall scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Barnet v Tranmere  (FA Cup, Sat 07 Nov 15:00 UK)  fixture_id 1646791
- Over 2.5: Medium (model score 0.587). Production BTTS: NO (Medium, p 0.550). Pattern: Low scoring.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.550) with supporting evidence (score 29, both sides BTTS at least 4 of 5); 55% to 59% historically.
- Barnet: scored in 5/5, 2+ in 2/5, conceded in 5/5, 2+ against in 1/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-1; 1-3; 1-1; 3-1; 1-1. Home last 3: 1-3; 1-1; 3-1 (BTTS 3/3).
- Tranmere: scored in 5/5, 2+ in 1/5, conceded in 4/5, 2+ against in 1/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-1; 1-2; 1-0; 1-1; 3-1. Away last 3: 2-4; 1-0; 1-1 (BTTS 2/3).
- Evidence score: 29. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'Low scoring' while the card shows both sides scoring and conceding regularly (evidence score 29). Model Medium (p 0.550). Barnet scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Tranmere scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Barnsley v Aldershot Town  (FA Cup, Sat 07 Nov 15:00 UK)  fixture_id 1646906
- Over 2.5: Medium (model score 0.599). Production BTTS: NO (Medium, p 0.565). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.565) with supporting evidence (score 25, both sides BTTS at least 2 of 5); 55% to 59% historically.
- Barnsley: scored in 5/5, 2+ in 0/5, conceded in 5/5, 2+ against in 4/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-3; 1-2; 1-2; 1-2; 1-1. Home last 3: 1-1; 1-2; 1-1 (BTTS 3/3).
- Aldershot Town: scored in 3/5, 2+ in 0/5, conceded in 4/5, 2+ against in 3/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 1-3; 1-3; 0-1; 0-2; 1-0. Away last 3: 1-2; 1-3; 0-2 (BTTS 2/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.565). Barnsley scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Aldershot Town scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5.

### Gillingham v Barrow  (FA Cup, Sat 07 Nov 15:00 UK)  fixture_id 1646910
- Over 2.5: Medium (model score 0.602). Production BTTS: NO (Medium, p 0.569). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.569) with supporting evidence (score 29, both sides BTTS at least 4 of 5); 55% to 59% historically.
- Gillingham: scored in 5/5, 2+ in 2/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 4-1; 1-3; 1-1; 1-4; 2-1. Home last 3: 0-0; 1-1; 1-4 (BTTS 2/3).
- Barrow: scored in 5/5, 2+ in 4/5, conceded in 4/5, 2+ against in 1/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 3-0; 2-1; 2-1; 3-2; 1-1. Away last 3: 4-2; 2-1; 3-2 (BTTS 3/3).
- Evidence score: 29. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 29). Model Medium (p 0.569). Gillingham scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Barrow scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Luton v Forest Green  (FA Cup, Sat 07 Nov 15:00 UK)  fixture_id 1646912
- Over 2.5: Medium (model score 0.622). Production BTTS: NO (Medium, p 0.565). Pattern: Both teams contribute.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.565) with supporting evidence (score 27, both sides BTTS at least 4 of 5); 55% to 59% historically.
- Luton: scored in 5/5, 2+ in 4/5, conceded in 4/5, 2+ against in 0/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-1; 2-1; 3-1; 2-0; 1-1. Home last 3: 2-1; 2-1; 3-1 (BTTS 3/3).
- Forest Green: scored in 5/5, 2+ in 4/5, conceded in 4/5, 2+ against in 3/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 3-3; 1-1; 2-4; 2-0; 2-2. Away last 3: 1-0; 1-1; 3-3 (BTTS 2/3).
- Evidence score: 27. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'Both teams contribute' while the card shows both sides scoring and conceding regularly (evidence score 27). Model Medium (p 0.565). Luton scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Forest Green scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Salisbury v Sholing  (FA Cup, Sat 07 Nov 15:00 UK)  fixture_id 1646816
- Over 2.5: Medium (model score 0.593). Production BTTS: NO (Medium, p 0.569). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.569) with supporting evidence (score 27, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Salisbury: scored in 5/5, 2+ in 4/5, conceded in 3/5, 2+ against in 0/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 2-0; 2-1; 1-1; 2-0; 2-1. Home last 3: 5-1; 2-0; 1-1 (BTTS 2/3).
- Sholing: scored in 5/5, 2+ in 2/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-1; 2-3; 1-1; 1-1; 4-2. Away last 3: 1-1; 1-1; 1-1 (BTTS 3/3).
- Evidence score: 27. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 27). Model Medium (p 0.569). Salisbury scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5; Sholing scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### Real Sociedad v Rayo Vallecano  (La Liga, Sun 08 Nov 15:15 UK)  fixture_id 1570449
- Over 2.5: Medium (model score 0.617). Production BTTS: NO (Medium, p 0.562). Pattern: Both teams contribute.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.562) with supporting evidence (score 27, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Real Sociedad: scored in 5/5, 2+ in 4/5, conceded in 5/5, 2+ against in 4/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 3-2; 3-2; 5-2; 2-1; 1-2. Home last 3: 0-3; 3-2; 2-1 (BTTS 2/3).
- Rayo Vallecano: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 1/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 2-1; 1-1; 1-1; 0-3; 3-0. Away last 3: 1-4; 1-1; 1-1 (BTTS 3/3).
- Evidence score: 27. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'Both teams contribute' while the card shows both sides scoring and conceding regularly (evidence score 27). Model Medium (p 0.562). Real Sociedad scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Rayo Vallecano scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Auxerre v Paris FC  (Ligue 1, Sat 07 Nov 18:00 UK)  fixture_id 1552811
- Over 2.5: rejected (model score 0.557). Production BTTS: NO (Medium, p 0.560). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.560) with supporting evidence (score 28, both sides BTTS at least 4 of 5); 55% to 59% historically.
- Auxerre: scored in 5/5, 2+ in 2/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-1; 1-4; 3-1; 1-1; 1-5. Home last 3: 1-0; 2-1; 1-1 (BTTS 2/3).
- Paris FC: scored in 4/5, 2+ in 3/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 2-1; 0-1; 4-3; 1-2; 3-1. Away last 3: 3-2; 0-1; 1-2 (BTTS 2/3).
- Evidence score: 28. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 28). Model Medium (p 0.560). Auxerre scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Paris FC scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Merthyr Town v Hebburn Town  (National League North, Sat 07 Nov 15:00 UK)  fixture_id 1587894
- Over 2.5: rejected (model score 0.523). Production BTTS: NO (Medium, p 0.559). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.559) with supporting evidence (score 26, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Merthyr Town: scored in 4/5, 2+ in 1/5, conceded in 5/5, 2+ against in 3/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 1-1; 1-3; 0-3; 3-3. Home last 3: 1-2; 1-1; 1-3 (BTTS 3/3).
- Hebburn Town: scored in 3/5, 2+ in 1/5, conceded in 5/5, 2+ against in 3/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 1-1; 0-3; 0-2; 2-2; 1-1. Away last 3: 1-5; 1-1; 2-2 (BTTS 3/3).
- Evidence score: 26. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 26). Model Medium (p 0.559). Merthyr Town scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Hebburn Town scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Folkestone Invicta v Truro City  (National League South, Sat 07 Nov 15:00 UK)  fixture_id 1588441
- Over 2.5: rejected (model score 0.575). Production BTTS: NO (Medium, p 0.554). Pattern: Both teams contribute.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.554) with supporting evidence (score 25, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Folkestone Invicta: scored in 4/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-1; 2-1; 2-0; 0-2; 2-2. Home last 3: 1-2; 2-1; 2-0 (BTTS 2/3).
- Truro City: scored in 5/5, 2+ in 5/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-2; 2-1; 4-3; 3-1; 3-0. Away last 3: 2-2; 2-1; 4-3 (BTTS 3/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'Both teams contribute' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.554). Folkestone Invicta scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Truro City scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Hemel Hempstead Town v Maidstone Utd  (National League South, Sat 07 Nov 15:00 UK)  fixture_id 1588443
- Over 2.5: rejected (model score 0.545). Production BTTS: NO (Medium, p 0.561). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.561) with supporting evidence (score 25, both sides BTTS at least 2 of 5); 55% to 59% historically.
- Hemel Hempstead Town: scored in 2/5, 2+ in 1/5, conceded in 4/5, 2+ against in 3/5, BTTS 2/5, clean sheets 1/5, failed to score 3/5. Last five: 0-0; 0-1; 1-3; 3-3; 0-5. Home last 3: 1-1; 1-1; 1-3 (BTTS 3/3).
- Maidstone Utd: scored in 5/5, 2+ in 3/5, conceded in 5/5, 2+ against in 1/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-1; 2-1; 1-1; 1-3; 2-1. Away last 3: 1-2; 2-1; 1-1 (BTTS 3/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.561). Hemel Hempstead Town scored in 2 of 5, conceded in 4 of 5, BTTS 2 of 5; Maidstone Utd scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### Sporting CP v Moreirense  (Primeira Liga, Sat 07 Nov 20:30 UK)  fixture_id 1575543
- Over 2.5: rejected (model score 0.569). Production BTTS: NO (Medium, p 0.540). Pattern: Both teams contribute.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.540) with supporting evidence (score 27, both sides BTTS at least 4 of 5); 55% to 59% historically.
- Sporting CP: scored in 5/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-1; 2-2; 3-1; 1-2; 2-0. Home last 3: 2-0; 2-2; 1-2 (BTTS 2/3).
- Moreirense: scored in 4/5, 2+ in 3/5, conceded in 5/5, 2+ against in 0/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 3-1; 1-1; 0-1; 3-1; 2-1. Away last 3: 1-2; 1-1; 3-1 (BTTS 3/3).
- Evidence score: 27. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'Both teams contribute' while the card shows both sides scoring and conceding regularly (evidence score 27). Model Medium (p 0.540). Sporting CP scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Moreirense scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### ST Johnstone v Dundee  (Scottish Premiership, Sat 07 Nov 15:00 UK)  fixture_id 1556703
- Over 2.5: rejected (model score 0.547). Production BTTS: NO (Medium, p 0.554). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.554) with supporting evidence (score 28, both sides BTTS at least 3 of 5); 55% to 59% historically.
- ST Johnstone: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-0; 1-1; 0-4; 2-2; 2-2. Home last 3: 1-1; 1-1; 2-2 (BTTS 3/3).
- Dundee: scored in 5/5, 2+ in 4/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-1; 2-1; 2-2; 1-2; 3-1. Away last 3: 1-2; 2-1; 1-2 (BTTS 3/3).
- Evidence score: 28. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 28). Model Medium (p 0.554). ST Johnstone scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Dundee scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

## Mild (11)

### Cardiff v Burnley  (Championship, Sat 07 Nov 15:00 UK)  fixture_id 1563254
- Over 2.5: Medium (model score 0.598). Production BTTS: NO (Medium, p 0.565). Pattern: Both teams contribute.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.565) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Cardiff: scored in 4/5, 2+ in 3/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 5-1; 2-2; 1-0; 0-3; 3-3. Home last 3: 5-1; 1-0; 3-3 (BTTS 2/3).
- Burnley: scored in 4/5, 2+ in 1/5, conceded in 4/5, 2+ against in 3/5, BTTS 4/5, clean sheets 1/5, failed to score 1/5. Last five: 2-2; 1-2; 1-4; 0-0; 1-1. Away last 3: 4-0; 1-4; 1-1 (BTTS 2/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'Both teams contribute' with evidence score 23 and model Medium (p 0.565); the NO is unsupported rather than contradicted. Cardiff scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Burnley scored in 4 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Espanyol v Deportivo La Coruna  (La Liga, Sat 07 Nov 15:15 UK)  fixture_id 1570446
- Over 2.5: rejected (model score 0.533). Production BTTS: NO (Medium, p 0.546). Pattern: Low scoring.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.546) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Espanyol: scored in 4/5, 2+ in 0/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-3; 1-1; 0-1; 1-2; 1-0. Home last 3: 1-1; 1-3; 0-1 (BTTS 2/3).
- Deportivo La Coruna: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 1/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 2-3; 1-1; 0-1; 2-1. Away last 3: 1-1; 2-3; 0-1 (BTTS 2/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'Low scoring' with evidence score 24 and model Medium (p 0.546); the NO is unsupported rather than contradicted. Espanyol scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Deportivo La Coruna scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Le Mans v Monaco  (Ligue 1, Sun 08 Nov 16:15 UK)  fixture_id 1552814
- Over 2.5: rejected (model score 0.557). Production BTTS: NO (Medium, p 0.552). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.552) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Le Mans: scored in 3/5, 2+ in 1/5, conceded in 5/5, 2+ against in 3/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 2-1; 1-3; 0-3; 1-1; 0-2. Home last 3: 2-2; 2-1; 0-3 (BTTS 2/3).
- Monaco: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 2-1; 2-2; 0-1; 1-1; 1-3. Away last 3: 1-1; 0-1; 1-3 (BTTS 2/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 24 and model Medium (p 0.552); the NO is unsupported rather than contradicted. Le Mans scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5; Monaco scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Lens v Marseille  (Ligue 1, Sun 08 Nov 19:45 UK)  fixture_id 1552818
- Over 2.5: rejected (model score 0.58). Production BTTS: NO (Medium, p 0.557). Pattern: Both teams contribute.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.557) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Lens: scored in 4/5, 2+ in 3/5, conceded in 5/5, 2+ against in 1/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-2; 2-1; 3-1; 2-1; 0-1. Home last 3: 0-1; 2-1; 2-1 (BTTS 2/3).
- Marseille: scored in 5/5, 2+ in 4/5, conceded in 3/5, 2+ against in 3/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 1-2; 2-0; 5-2; 4-3; 2-0. Away last 3: 0-1; 2-0; 5-2 (BTTS 1/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'Both teams contribute' with evidence score 24 and model Medium (p 0.557); the NO is unsupported rather than contradicted. Lens scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Marseille scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5.

### AFC Telford United v Spalding United  (National League North, Sat 07 Nov 15:00 UK)  fixture_id 1587885
- Over 2.5: rejected (model score 0.543). Production BTTS: NO (Medium, p 0.557). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.557) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- AFC Telford United: scored in 5/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-2; 2-1; 2-2; 1-0; 2-1. Home last 3: 0-5; 2-1; 2-2 (BTTS 2/3).
- Spalding United: scored in 3/5, 2+ in 2/5, conceded in 5/5, 2+ against in 4/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 1-2; 0-1; 0-2; 2-2; 3-2. Away last 3: 1-2; 0-1; 0-2 (BTTS 1/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.557); the NO is unsupported rather than contradicted. AFC Telford United scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Spalding United scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Brackley Town v Chester  (National League North, Sat 07 Nov 15:00 UK)  fixture_id 1587886
- Over 2.5: rejected (model score 0.547). Production BTTS: NO (Medium, p 0.560). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.560) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Brackley Town: scored in 4/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 2-1; 2-3; 0-1; 2-2; 1-0. Home last 3: 3-2; 2-1; 0-1 (BTTS 2/3).
- Chester: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 1/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 4-1; 1-0; 1-3; 2-1; 0-1. Away last 3: 1-1; 1-3; 1-3 (BTTS 3/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.560); the NO is unsupported rather than contradicted. Brackley Town scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Chester scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Slough Town v Walton & Hersham  (National League South, Sat 07 Nov 15:00 UK)  fixture_id 1588446
- Over 2.5: rejected (model score 0.552). Production BTTS: NO (Medium, p 0.559). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.559) with supporting evidence (score 23, both sides BTTS at least 1 of 5); 55% to 59% historically.
- Slough Town: scored in 5/5, 2+ in 0/5, conceded in 5/5, 2+ against in 5/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-5; 1-2; 1-3; 1-3; 1-2. Home last 3: 1-1; 1-2; 1-3 (BTTS 3/3).
- Walton & Hersham: scored in 2/5, 2+ in 1/5, conceded in 4/5, 2+ against in 2/5, BTTS 1/5, clean sheets 1/5, failed to score 3/5. Last five: 3-1; 1-0; 0-1; 0-2; 0-3. Away last 3: 3-1; 1-0; 0-1 (BTTS 1/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.559); the NO is unsupported rather than contradicted. Slough Town scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Walton & Hersham scored in 2 of 5, conceded in 4 of 5, BTTS 1 of 5.

### Weston-super-Mare v Braintree  (National League South, Sat 07 Nov 15:00 UK)  fixture_id 1588448
- Over 2.5: rejected (model score 0.575). Production BTTS: NO (Medium, p 0.569). Pattern: Both teams contribute.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.569) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Weston-super-Mare: scored in 4/5, 2+ in 1/5, conceded in 5/5, 2+ against in 4/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 2-3; 1-1; 1-6; 1-2; 0-2. Home last 3: 3-1; 1-0; 1-1 (BTTS 2/3).
- Braintree: scored in 4/5, 2+ in 1/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-3; 1-2; 0-6; 2-1; 1-0. Away last 3: 2-3; 3-4; 0-6 (BTTS 2/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'Both teams contribute' with evidence score 24 and model Medium (p 0.569); the NO is unsupported rather than contradicted. Weston-super-Mare scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Braintree scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Aberdeen v Hibernian  (Scottish Premiership, Sat 07 Nov 17:45 UK)  fixture_id 1556700
- Over 2.5: rejected (model score 0.521). Production BTTS: NO (Medium, p 0.546). Pattern: Low scoring.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.546) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Aberdeen: scored in 3/5, 2+ in 2/5, conceded in 5/5, 2+ against in 1/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 1-1; 0-1; 3-1; 2-3; 0-1. Home last 3: 0-1; 3-1; 0-1 (BTTS 1/3).
- Hibernian: scored in 4/5, 2+ in 0/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 0-1; 1-2; 1-2; 1-1. Away last 3: 1-2; 0-1; 1-1 (BTTS 2/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'Low scoring' with evidence score 23 and model Medium (p 0.546); the NO is unsupported rather than contradicted. Aberdeen scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5; Hibernian scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Celtic v Kilmarnock  (Scottish Premiership, Sun 08 Nov 16:00 UK)  fixture_id 1556701
- Over 2.5: Medium (model score 0.606). Production BTTS: NO (Medium, p 0.568). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.568) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Celtic: scored in 4/5, 2+ in 4/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 2-0; 7-1; 2-1; 2-2; 0-2. Home last 3: 0-1; 7-1; 2-2 (BTTS 2/3).
- Kilmarnock: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 5/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-3; 3-2; 0-3; 1-3; 2-2. Away last 3: 1-3; 0-3; 1-3 (BTTS 2/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 24 and model Medium (p 0.568); the NO is unsupported rather than contradicted. Celtic scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Kilmarnock scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Galatasaray v Amed  (Super Lig, Sat 07 Nov 16:00 UK)  fixture_id 1584461
- Over 2.5: Medium (model score 0.598). Production BTTS: NO (Medium, p 0.556). Pattern: Both teams contribute.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.556) with supporting evidence (score 23, both sides BTTS at least 2 of 5); 55% to 59% historically.
- Galatasaray: scored in 4/5, 2+ in 3/5, conceded in 3/5, 2+ against in 1/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 0-4; 3-1; 1-0; 2-1; 4-0. Home last 3: 1-0; 3-1; 2-1 (BTTS 2/3).
- Amed: scored in 5/5, 2+ in 4/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 3-2; 2-2; 1-0; 2-1; 5-1. Away last 3: 2-2; 2-2; 2-1 (BTTS 3/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'Both teams contribute' with evidence score 23 and model Medium (p 0.556); the NO is unsupported rather than contradicted. Galatasaray scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5; Amed scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

## Note (13)

### Borussia Dortmund v SV Elversberg  (Bundesliga, Sat 07 Nov 14:30 UK)  fixture_id 1575212
- Over 2.5: Medium (model score 0.619). Production BTTS: YES (High, p 0.578). Pattern: Low scoring.
- Audit assessment: YES. BTTS model High band (p 0.578 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Borussia Dortmund: scored in 4/5, 2+ in 2/5, conceded in 2/5, 2+ against in 2/5, BTTS 2/5, clean sheets 3/5, failed to score 1/5. Last five: 1-0; 2-2; 0-0; 1-0; 2-2. Home last 3: 3-0; 2-2; 1-0 (BTTS 1/3).
- SV Elversberg: scored in 2/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 2/5, clean sheets 1/5, failed to score 3/5. Last five: 0-0; 0-1; 4-3; 0-4; 4-1. Away last 3: 0-0; 0-1; 0-4 (BTTS 0/3).
- Evidence score: 14. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Borussia Dortmund scored in 4 of 5, conceded in 2 of 5, BTTS 2 of 5; SV Elversberg scored in 2 of 5, conceded in 4 of 5, BTTS 2 of 5.

### RB Leipzig v FC Augsburg  (Bundesliga, Sat 07 Nov 14:30 UK)  fixture_id 1575213
- Over 2.5: High (model score 0.681). Production BTTS: YES (High, p 0.577). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.577 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- RB Leipzig: scored in 4/5, 2+ in 3/5, conceded in 2/5, 2+ against in 2/5, BTTS 1/5, clean sheets 3/5, failed to score 1/5. Last five: 0-2; 6-0; 1-6; 4-0; 2-0. Home last 3: 5-0; 6-0; 4-0 (BTTS 0/3).
- FC Augsburg: scored in 5/5, 2+ in 3/5, conceded in 5/5, 2+ against in 4/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-3; 2-2; 3-4; 1-1; 1-2. Away last 3: 4-1; 2-3; 3-4 (BTTS 3/3).
- Evidence score: 22. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 1 of 5; historically this group still went BTTS 64% of the time, so informational only. RB Leipzig scored in 4 of 5, conceded in 2 of 5, BTTS 1 of 5; FC Augsburg scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### SC Paderborn 07 v Eintracht Frankfurt  (Bundesliga, Sat 07 Nov 14:30 UK)  fixture_id 1575220
- Over 2.5: Medium (model score 0.606). Production BTTS: YES (High, p 0.575). Pattern: Low scoring.
- Audit assessment: YES. BTTS model High band (p 0.575 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- SC Paderborn 07: scored in 3/5, 2+ in 2/5, conceded in 3/5, 2+ against in 2/5, BTTS 2/5, clean sheets 2/5, failed to score 2/5. Last five: 3-1; 0-2; 2-2; 1-0; 0-0. Home last 3: 3-1; 0-2; 1-0 (BTTS 1/3).
- Eintracht Frankfurt: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 2-2; 0-6; 1-0; 0-1; 3-1. Away last 3: 3-1; 0-6; 0-1 (BTTS 1/3).
- Evidence score: 16. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. SC Paderborn 07 scored in 3 of 5, conceded in 3 of 5, BTTS 2 of 5; Eintracht Frankfurt scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5.

### VfB Stuttgart v Werder Bremen  (Bundesliga, Sat 07 Nov 17:30 UK)  fixture_id 1575214
- Over 2.5: High (model score 0.649). Production BTTS: YES (High, p 0.585). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.585 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- VfB Stuttgart: scored in 3/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 0-1; 2-0; 0-1; 2-3; 4-2. Home last 3: 4-1; 0-1; 2-3 (BTTS 2/3).
- Werder Bremen: scored in 5/5, 2+ in 5/5, conceded in 4/5, 2+ against in 4/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 3-2; 2-2; 2-2; 3-2; 2-0. Away last 3: 1-1; 2-2; 3-2 (BTTS 3/3).
- Evidence score: 23. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. VfB Stuttgart scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5; Werder Bremen scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### SC Freiburg v Union Berlin  (Bundesliga, Sun 08 Nov 16:30 UK)  fixture_id 1575216
- Over 2.5: High (model score 0.646). Production BTTS: YES (High, p 0.576). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.576 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- SC Freiburg: scored in 5/5, 2+ in 3/5, conceded in 5/5, 2+ against in 3/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-2; 2-1; 1-2; 1-3; 2-1. Home last 3: 5-0; 2-1; 1-3 (BTTS 2/3).
- Union Berlin: scored in 3/5, 2+ in 0/5, conceded in 3/5, 2+ against in 1/5, BTTS 2/5, clean sheets 2/5, failed to score 2/5. Last five: 0-7; 1-0; 0-0; 1-1; 1-1. Away last 3: 0-4; 0-7; 1-1 (BTTS 1/3).
- Evidence score: 22. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. SC Freiburg scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Union Berlin scored in 3 of 5, conceded in 3 of 5, BTTS 2 of 5.

### Excelsior v GO Ahead Eagles  (Eredivisie, Sat 07 Nov 20:00 UK)  fixture_id 1552218
- Over 2.5: High (model score 0.647). Production BTTS: YES (High, p 0.618). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.618 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Excelsior: scored in 2/5, 2+ in 1/5, conceded in 5/5, 2+ against in 4/5, BTTS 2/5, clean sheets 0/5, failed to score 3/5. Last five: 2-2; 1-5; 0-4; 0-1; 0-9. Home last 3: 1-2; 1-5; 0-9 (BTTS 2/3).
- GO Ahead Eagles: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 4/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 3-3; 1-4; 3-2; 0-4. Away last 3: 1-1; 1-4; 0-4 (BTTS 2/3).
- Evidence score: 22. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Excelsior scored in 2 of 5, conceded in 5 of 5, BTTS 2 of 5; GO Ahead Eagles scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Heerenveen v Feyenoord  (Eredivisie, Sun 08 Nov 11:15 UK)  fixture_id 1552221
- Over 2.5: High (model score 0.632). Production BTTS: YES (High, p 0.604). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.604 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Heerenveen: scored in 4/5, 2+ in 3/5, conceded in 2/5, 2+ against in 2/5, BTTS 1/5, clean sheets 3/5, failed to score 1/5. Last five: 4-0; 0-2; 4-0; 3-2; 1-0. Home last 3: 0-0; 4-0; 1-0 (BTTS 0/3).
- Feyenoord: scored in 5/5, 2+ in 3/5, conceded in 3/5, 2+ against in 1/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 5-0; 2-0; 4-3; 1-1; 1-1. Away last 3: 7-0; 4-3; 1-1 (BTTS 2/3).
- Evidence score: 17. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 1 of 5; historically this group still went BTTS 64% of the time, so informational only. Heerenveen scored in 4 of 5, conceded in 2 of 5, BTTS 1 of 5; Feyenoord scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5.

### AZ Alkmaar v Groningen  (Eredivisie, Sun 08 Nov 15:45 UK)  fixture_id 1552224
- Over 2.5: Medium (model score 0.613). Production BTTS: YES (High, p 0.582). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.582 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- AZ Alkmaar: scored in 2/5, 2+ in 1/5, conceded in 4/5, 2+ against in 3/5, BTTS 1/5, clean sheets 1/5, failed to score 3/5. Last five: 1-0; 0-2; 2-2; 0-2; 0-1. Home last 3: 1-1; 1-0; 0-2 (BTTS 1/3).
- Groningen: scored in 5/5, 2+ in 5/5, conceded in 4/5, 2+ against in 3/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 3-0; 5-1; 2-5; 2-2; 2-3. Away last 3: 1-1; 5-1; 2-2 (BTTS 3/3).
- Evidence score: 21. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 1 of 5; historically this group still went BTTS 64% of the time, so informational only. AZ Alkmaar scored in 2 of 5, conceded in 4 of 5, BTTS 1 of 5; Groningen scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Chesterfield v Yeovil Town  (FA Cup, Sat 07 Nov 15:00 UK)  fixture_id 1646907
- Over 2.5: Medium (model score 0.599). Production BTTS: YES (High, p 0.587). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.587 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Chesterfield: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 2-2; 0-1; 1-1; 5-1; 1-4. Home last 3: 4-2; 1-1; 5-1 (BTTS 3/3).
- Yeovil Town: scored in 4/5, 2+ in 3/5, conceded in 3/5, 2+ against in 2/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 6-0; 6-0; 1-2; 2-1; 0-2. Away last 3: 6-0; 2-1; 0-2 (BTTS 1/3).
- Evidence score: 23. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Chesterfield scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Yeovil Town scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5.

### Mansfield Town v Macclesfield  (FA Cup, Sat 07 Nov 15:00 UK)  fixture_id 1646913
- Over 2.5: rejected (model score 0.558). Production BTTS: YES (High, p 0.578). Pattern: Low scoring.
- Audit assessment: YES. BTTS model High band (p 0.578 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Mansfield Town: scored in 3/5, 2+ in 2/5, conceded in 3/5, 2+ against in 1/5, BTTS 2/5, clean sheets 2/5, failed to score 2/5. Last five: 1-1; 3-0; 4-1; 0-2; 0-0. Home last 3: 2-1; 1-1; 0-2 (BTTS 2/3).
- Macclesfield: scored in 5/5, 2+ in 2/5, conceded in 3/5, 2+ against in 2/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 1-1; 1-0; 4-3; 1-2; 3-0. Away last 3: 1-2; 1-1; 3-0 (BTTS 2/3).
- Evidence score: 19. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Mansfield Town scored in 3 of 5, conceded in 3 of 5, BTTS 2 of 5; Macclesfield scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5.

### Plymouth v Alvechurch  (FA Cup, Sat 07 Nov 15:00 UK)  fixture_id 1646914
- Over 2.5: Medium (model score 0.592). Production BTTS: YES (High, p 0.577). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.577 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Plymouth: scored in 2/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 2/5, clean sheets 1/5, failed to score 3/5. Last five: 2-1; 0-2; 0-3; 3-2; 0-0. Home last 3: 2-1; 0-2; 0-0 (BTTS 1/3).
- Alvechurch: scored in 4/5, 2+ in 3/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 0-1; 1-1; 4-4; 2-2; 3-1. Away last 3: 1-1; 4-4; 3-1 (BTTS 3/3).
- Evidence score: 21. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Plymouth scored in 2 of 5, conceded in 4 of 5, BTTS 2 of 5; Alvechurch scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Port Vale v Scunthorpe  (FA Cup, Sat 07 Nov 15:00 UK)  fixture_id 1646815
- Over 2.5: Medium (model score 0.598). Production BTTS: YES (High, p 0.576). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.576 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Port Vale: scored in 4/5, 2+ in 1/5, conceded in 3/5, 2+ against in 2/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 1-0; 1-0; 1-1; 0-2; 4-2. Home last 3: 1-0; 1-0; 4-2 (BTTS 1/3).
- Scunthorpe: scored in 3/5, 2+ in 1/5, conceded in 5/5, 2+ against in 5/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 0-3; 0-2; 2-3; 1-4; 1-2. Away last 3: 0-2; 1-4; 1-2 (BTTS 2/3).
- Evidence score: 19. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Port Vale scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5; Scunthorpe scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Cray Wanderers v Stockport County  (FA Cup, Sun 08 Nov 14:15 UK)  fixture_id 1646909
- Over 2.5: Medium (model score 0.63). Production BTTS: YES (High, p 0.576). Pattern: Both teams contribute.
- Audit assessment: YES. BTTS model High band (p 0.576 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Cray Wanderers: scored in 5/5, 2+ in 4/5, conceded in 5/5, 2+ against in 3/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-3; 3-3; 5-1; 1-2; 4-1. Home last 3: 4-1; 3-3; 1-2 (BTTS 3/3).
- Stockport County: scored in 4/5, 2+ in 2/5, conceded in 3/5, 2+ against in 0/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 1-0; 2-0; 1-1; 0-1; 2-1. Away last 3: 2-0; 1-1; 0-1 (BTTS 1/3).
- Evidence score: 25. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Cray Wanderers scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Stockport County scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5.

## All fixtures

| fixture_id | kickoff UK | competition | fixture | Over 2.5 | BTTS (prod) | p | audit | evidence | flag | status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1575212 | Sat 07 Nov 14:30 | Bundesliga | Borussia Dortmund v SV Elversberg | Medium | YES (High) | 0.578 | YES | 14 | note | note |
| 1575217 | Sat 07 Nov 14:30 | Bundesliga | FSV Mainz 05 v Bayern Munich | High | YES (High) | 0.608 | YES | 28 | - | ok |
| 1575213 | Sat 07 Nov 14:30 | Bundesliga | RB Leipzig v FC Augsburg | High | YES (High) | 0.577 | YES | 22 | note | note |
| 1575220 | Sat 07 Nov 14:30 | Bundesliga | SC Paderborn 07 v Eintracht Frankfurt | Medium | YES (High) | 0.575 | YES | 16 | note | note |
| 1575214 | Sat 07 Nov 17:30 | Bundesliga | VfB Stuttgart v Werder Bremen | High | YES (High) | 0.585 | YES | 23 | note | note |
| 1575219 | Sun 08 Nov 14:30 | Bundesliga | 1. FC Köln v Bayer Leverkusen | Medium | NO (Medium) | 0.569 | NO LEAN | 21 | - | ok |
| 1575216 | Sun 08 Nov 16:30 | Bundesliga | SC Freiburg v Union Berlin | High | YES (High) | 0.576 | YES | 22 | note | note |
| 1575215 | Sun 08 Nov 18:30 | Bundesliga | 1899 Hoffenheim v FC Schalke 04 | Medium | NO (Medium) | 0.552 | NO LEAN | 16 | - | ok |
| 1563253 | Sat 07 Nov 12:30 | Championship | Bristol City v Norwich | rejected | NO (Medium) | 0.552 | NO LEAN | 16 | - | ok |
| 1563257 | Sat 07 Nov 12:30 | Championship | Portsmouth v Stoke City | rejected | NO (Medium) | 0.537 | NO LEAN | 19 | - | ok |
| 1563262 | Sat 07 Nov 12:30 | Championship | Wrexham v Wolves | rejected | NO (Medium) | 0.560 | NO LEAN | 20 | - | ok |
| 1563251 | Sat 07 Nov 15:00 | Championship | Birmingham v Swansea | Medium | NO (Medium) | 0.552 | NO LEAN | 13 | - | ok |
| 1563252 | Sat 07 Nov 15:00 | Championship | Blackburn v West Ham | rejected | NO (Medium) | 0.567 | NO LEAN | 19 | - | ok |
| 1563254 | Sat 07 Nov 15:00 | Championship | Cardiff v Burnley | Medium | NO (Medium) | 0.565 | LEAN YES | 23 | mild | note |
| 1563255 | Sat 07 Nov 15:00 | Championship | Charlton v Sheffield Utd | rejected | NO (Medium) | 0.551 | NO LEAN | 20 | - | ok |
| 1563258 | Sat 07 Nov 15:00 | Championship | Preston v Southampton | rejected | NO (Medium) | 0.562 | NO LEAN | 21 | - | ok |
| 1563259 | Sat 07 Nov 15:00 | Championship | QPR v Lincoln | Medium | NO (Medium) | 0.564 | NO LEAN | 21 | - | ok |
| 1563260 | Sat 07 Nov 15:00 | Championship | Watford v Middlesbrough | rejected | NO (Medium) | 0.567 | NO LEAN | 19 | - | ok |
| 1563261 | Sat 07 Nov 15:00 | Championship | West Brom v Millwall | rejected | NO (Medium) | 0.566 | LEAN YES | 26 | moderate | needs review |
| 1552217 | Sat 07 Nov 15:30 | Eredivisie | Fortuna Sittard v Telstar | Medium | YES (High) | 0.593 | YES | 23 | - | ok |
| 1552220 | Sat 07 Nov 17:45 | Eredivisie | ADO Den Haag v Sparta Rotterdam | High | YES (High) | 0.613 | YES | 28 | - | ok |
| 1552218 | Sat 07 Nov 20:00 | Eredivisie | Excelsior v GO Ahead Eagles | High | YES (High) | 0.618 | YES | 22 | note | note |
| 1552221 | Sun 08 Nov 11:15 | Eredivisie | Heerenveen v Feyenoord | High | YES (High) | 0.604 | YES | 17 | note | note |
| 1552222 | Sun 08 Nov 13:30 | Eredivisie | Twente v Ajax | High | YES (High) | 0.614 | YES | 25 | - | ok |
| 1552224 | Sun 08 Nov 15:45 | Eredivisie | AZ Alkmaar v Groningen | Medium | YES (High) | 0.582 | YES | 21 | note | note |
| 1552219 | Sun 08 Nov 15:45 | Eredivisie | Cambuur v PSV Eindhoven | High | YES (High) | 0.614 | YES | 22 | - | ok |
| 1552223 | Sun 08 Nov 19:00 | Eredivisie | Utrecht v NEC Nijmegen | High | YES (High) | 0.596 | YES | 26 | - | ok |
| 1646804 | Sat 07 Nov 15:00 | FA Cup | AFC Hornchurch v Blackpool | Medium | NO (Medium) | 0.565 | NO LEAN | 19 | - | ok |
| 1646790 | Sat 07 Nov 15:00 | FA Cup | Accrington ST v Wycombe | rejected | YES (High) | 0.579 | YES | 21 | - | ok |
| 1646791 | Sat 07 Nov 15:00 | FA Cup | Barnet v Tranmere | Medium | NO (Medium) | 0.550 | LEAN YES | 29 | moderate | needs review |
| 1646906 | Sat 07 Nov 15:00 | FA Cup | Barnsley v Aldershot Town | Medium | NO (Medium) | 0.565 | LEAN YES | 25 | moderate | needs review |
| 1646792 | Sat 07 Nov 15:00 | FA Cup | Boreham Wood v Wigan | High | NO (Medium) | 0.572 | NO LEAN | 21 | - | ok |
| 1646793 | Sat 07 Nov 15:00 | FA Cup | Bradford v Marine | rejected | NO (Medium) | 0.541 | NO LEAN | 15 | - | ok |
| 1646795 | Sat 07 Nov 15:00 | FA Cup | Bromley v Rotherham | Medium | NO (Medium) | 0.575 | YES | 23 | severe | needs review |
| 1646796 | Sat 07 Nov 15:00 | FA Cup | Burton Albion v AFC Rushden & Diamonds | rejected | NO (Medium) | 0.550 | NO LEAN | 8 | - | ok |
| 1646797 | Sat 07 Nov 15:00 | FA Cup | Carlisle v Salford City | High | YES (Medium) | 0.574 | NO LEAN | 22 | - | ok |
| 1646798 | Sat 07 Nov 15:00 | FA Cup | Cheltenham v FC Halifax Town | Medium | YES (High) | 0.582 | YES | 22 | - | ok |
| 1646907 | Sat 07 Nov 15:00 | FA Cup | Chesterfield v Yeovil Town | Medium | YES (High) | 0.587 | YES | 23 | note | note |
| 1646908 | Sat 07 Nov 15:00 | FA Cup | Colchester v Worcester City | Medium | NO (Medium) | 0.555 | NO LEAN | 19 | - | ok |
| 1646799 | Sat 07 Nov 15:00 | FA Cup | Crewe v AFC Wimbledon | Medium | YES (High) | 0.578 | YES | 23 | - | ok |
| 1646800 | Sat 07 Nov 15:00 | FA Cup | Dover v Wealdstone | Medium | NO (Medium) | 0.556 | NO LEAN | 20 | - | ok |
| 1646801 | Sat 07 Nov 15:00 | FA Cup | Eastleigh v Shrewsbury | Medium | YES (High) | 0.577 | YES | 24 | - | ok |
| 1646802 | Sat 07 Nov 15:00 | FA Cup | Fleetwood Town v Rochdale | Medium | YES (High) | 0.579 | YES | 27 | - | ok |
| 1646910 | Sat 07 Nov 15:00 | FA Cup | Gillingham v Barrow | Medium | NO (Medium) | 0.569 | LEAN YES | 29 | moderate | needs review |
| 1646803 | Sat 07 Nov 15:00 | FA Cup | Guiseley AFC v Sutton Utd | Medium | NO (Medium) | 0.567 | NO LEAN | 21 | - | ok |
| 1646911 | Sat 07 Nov 15:00 | FA Cup | Harrogate Town v AFC Fylde | Medium | NO (Medium) | 0.562 | NO LEAN | 20 | - | ok |
| 1646805 | Sat 07 Nov 15:00 | FA Cup | Huddersfield v Exeter City | Medium | NO (Medium) | 0.558 | NO LEAN | 19 | - | ok |
| 1646806 | Sat 07 Nov 15:00 | FA Cup | Kidderminster Harriers v Doncaster | Medium | NO (Medium) | 0.556 | NO LEAN | 21 | - | ok |
| 1646807 | Sat 07 Nov 15:00 | FA Cup | Leyton Orient v Harborough Town | rejected | NO (Medium) | 0.542 | NO LEAN | 13 | - | ok |
| 1646912 | Sat 07 Nov 15:00 | FA Cup | Luton v Forest Green | Medium | NO (Medium) | 0.565 | LEAN YES | 27 | moderate | needs review |
| 1646913 | Sat 07 Nov 15:00 | FA Cup | Mansfield Town v Macclesfield | rejected | YES (High) | 0.578 | YES | 19 | note | note |
| 1646808 | Sat 07 Nov 15:00 | FA Cup | Milton Keynes Dons v Swindon Town | Medium | NO (Medium) | 0.566 | NO LEAN | 21 | - | ok |
| 1646809 | Sat 07 Nov 15:00 | FA Cup | Newport County v Walsall | Medium | YES (High) | 0.577 | YES | 25 | - | ok |
| 1646812 | Sat 07 Nov 15:00 | FA Cup | Oxford United v Stevenage | rejected | NO (Medium) | 0.539 | NO LEAN | 13 | - | ok |
| 1646914 | Sat 07 Nov 15:00 | FA Cup | Plymouth v Alvechurch | Medium | YES (High) | 0.577 | YES | 21 | note | note |
| 1646815 | Sat 07 Nov 15:00 | FA Cup | Port Vale v Scunthorpe | Medium | YES (High) | 0.576 | YES | 19 | note | note |
| 1646816 | Sat 07 Nov 15:00 | FA Cup | Salisbury v Sholing | Medium | NO (Medium) | 0.569 | LEAN YES | 27 | moderate | needs review |
| 1646818 | Sat 07 Nov 15:00 | FA Cup | York v Northampton | rejected | NO (Medium) | 0.561 | NO LEAN | 20 | - | ok |
| 1646905 | Sat 07 Nov 17:30 | FA Cup | Altrincham v Notts County | rejected | NO (Medium) | 0.570 | NO LEAN | 20 | - | ok |
| 1646813 | Sat 07 Nov 20:00 | FA Cup | Peterborough v Reading | rejected | NO (Medium) | 0.564 | NO LEAN | 17 | - | ok |
| 1646915 | Sun 08 Nov 12:00 | FA Cup | Stafford Rangers v Grimsby | rejected | NO (Medium) | 0.567 | NO LEAN | 11 | - | ok |
| 1646909 | Sun 08 Nov 14:15 | FA Cup | Cray Wanderers v Stockport County | Medium | YES (High) | 0.576 | YES | 25 | note | note |
| 1646817 | Sun 08 Nov 15:00 | FA Cup | Wimborne Town v Crawley Town | Medium | NO (Medium) | 0.575 | YES | 20 | severe | needs review |
| 1646810 | Sun 08 Nov 17:15 | FA Cup | Oldham v Sheffield Wednesday | rejected | NO (Medium) | 0.567 | NO LEAN | 16 | - | ok |
| 1570447 | Sat 07 Nov 13:00 | La Liga | Malaga v Racing Santander | Medium | NO (Medium) | 0.569 | NO LEAN | 22 | - | ok |
| 1570446 | Sat 07 Nov 15:15 | La Liga | Espanyol v Deportivo La Coruna | rejected | NO (Medium) | 0.546 | LEAN YES | 24 | mild | note |
| 1570448 | Sat 07 Nov 17:30 | La Liga | Osasuna v Athletic Club | rejected | NO (Medium) | 0.552 | NO LEAN | 17 | - | ok |
| 1570451 | Sat 07 Nov 20:00 | La Liga | Valencia v Real Madrid | rejected | NO (Medium) | 0.563 | NO LEAN | 21 | - | ok |
| 1570445 | Sun 08 Nov 13:00 | La Liga | Elche v Real Betis | rejected | NO (Medium) | 0.547 | NO LEAN | 16 | - | ok |
| 1570449 | Sun 08 Nov 15:15 | La Liga | Real Sociedad v Rayo Vallecano | Medium | NO (Medium) | 0.562 | LEAN YES | 27 | moderate | needs review |
| 1570444 | Sun 08 Nov 17:30 | La Liga | Celta Vigo v Levante | rejected | NO (Medium) | 0.568 | NO LEAN | 18 | - | ok |
| 1570452 | Sun 08 Nov 17:30 | La Liga | Villarreal v Getafe | rejected | NO (Medium) | 0.553 | NO LEAN | 15 | - | ok |
| 1570443 | Sun 08 Nov 20:00 | La Liga | Atletico Madrid v Barcelona | Medium | NO (Medium) | 0.557 | NO LEAN | 22 | - | ok |
| 1552811 | Sat 07 Nov 18:00 | Ligue 1 | Auxerre v Paris FC | rejected | NO (Medium) | 0.560 | LEAN YES | 28 | moderate | needs review |
| 1552815 | Sat 07 Nov 20:05 | Ligue 1 | Paris Saint Germain v Estac Troyes | Medium | NO (Medium) | 0.560 | NO LEAN | 18 | - | ok |
| 1552816 | Sun 08 Nov 14:00 | Ligue 1 | Rennes v Lille | Medium | NO (Medium) | 0.560 | NO LEAN | 21 | - | ok |
| 1552810 | Sun 08 Nov 16:15 | Ligue 1 | Angers v Nice | Medium | NO (Medium) | 0.565 | NO LEAN | 22 | - | ok |
| 1552813 | Sun 08 Nov 16:15 | Ligue 1 | Le Havre v Lorient | rejected | NO (Medium) | 0.560 | NO LEAN | 18 | - | ok |
| 1552814 | Sun 08 Nov 16:15 | Ligue 1 | Le Mans v Monaco | rejected | NO (Medium) | 0.552 | LEAN YES | 24 | mild | note |
| 1552812 | Sun 08 Nov 16:15 | Ligue 1 | Stade Brestois 29 v Lyon | rejected | NO (Medium) | 0.564 | NO LEAN | 21 | - | ok |
| 1552818 | Sun 08 Nov 19:45 | Ligue 1 | Lens v Marseille | rejected | NO (Medium) | 0.557 | LEAN YES | 24 | mild | note |
| 1587885 | Sat 07 Nov 15:00 | National League North | AFC Telford United v Spalding United | rejected | NO (Medium) | 0.557 | LEAN YES | 23 | mild | note |
| 1587886 | Sat 07 Nov 15:00 | National League North | Brackley Town v Chester | rejected | NO (Medium) | 0.560 | LEAN YES | 23 | mild | note |
| 1587887 | Sat 07 Nov 15:00 | National League North | Chorley v Hereford | rejected | NO (Medium) | 0.555 | NO LEAN | 21 | - | ok |
| 1587890 | Sat 07 Nov 15:00 | National League North | Hednesford Town v Morecambe | rejected | NO (Medium) | 0.545 | NO LEAN | 19 | - | ok |
| 1587891 | Sat 07 Nov 15:00 | National League North | King's Lynn Town v Spennymoor Town | rejected | NO (Medium) | 0.533 | NO LEAN | 14 | - | ok |
| 1587894 | Sat 07 Nov 15:00 | National League North | Merthyr Town v Hebburn Town | rejected | NO (Medium) | 0.559 | LEAN YES | 26 | moderate | needs review |
| 1587895 | Sat 07 Nov 15:00 | National League North | Scarborough Athletic v Buxton | rejected | NO (Medium) | 0.545 | NO LEAN | 20 | - | ok |
| 1587896 | Sat 07 Nov 15:00 | National League North | South Shields v Southport | rejected | NO (Medium) | 0.555 | NO LEAN | 20 | - | ok |
| 1588437 | Sat 07 Nov 15:00 | National League South | Chelmsford City v Farnborough | Medium | NO (Medium) | 0.565 | NO LEAN | 14 | - | ok |
| 1588438 | Sat 07 Nov 15:00 | National League South | Dagenham & Redbridge v Billericay Town | rejected | NO (Medium) | 0.535 | NO LEAN | 13 | - | ok |
| 1588439 | Sat 07 Nov 15:00 | National League South | Ebbsfleet United v Chesham United | Medium | NO (Medium) | 0.561 | NO LEAN | 18 | - | ok |
| 1588440 | Sat 07 Nov 15:00 | National League South | Farnham Town v Tonbridge Angels | rejected | NO (Medium) | 0.556 | NO LEAN | 18 | - | ok |
| 1588441 | Sat 07 Nov 15:00 | National League South | Folkestone Invicta v Truro City | rejected | NO (Medium) | 0.554 | LEAN YES | 25 | moderate | needs review |
| 1588442 | Sat 07 Nov 15:00 | National League South | Hampton & Richmond v Maidenhead | rejected | NO (Medium) | 0.556 | NO LEAN | 19 | - | ok |
| 1588443 | Sat 07 Nov 15:00 | National League South | Hemel Hempstead Town v Maidstone Utd | rejected | NO (Medium) | 0.561 | LEAN YES | 25 | moderate | needs review |
| 1588444 | Sat 07 Nov 15:00 | National League South | Horsham v AFC Totton | Medium | NO (Medium) | 0.565 | NO LEAN | 22 | - | ok |
| 1588446 | Sat 07 Nov 15:00 | National League South | Slough Town v Walton & Hersham | rejected | NO (Medium) | 0.559 | LEAN YES | 23 | mild | note |
| 1588448 | Sat 07 Nov 15:00 | National League South | Weston-super-Mare v Braintree | rejected | NO (Medium) | 0.569 | LEAN YES | 24 | mild | note |
| 1557463 | Sat 07 Nov 12:30 | Premier League | Leeds v Tottenham | rejected | NO (Low) | 0.503 | NO LEAN | 17 | - | ok |
| 1557457 | Sat 07 Nov 15:00 | Premier League | Arsenal v Hull City | rejected | NO (Medium) | 0.516 | NO LEAN | 20 | - | ok |
| 1557461 | Sat 07 Nov 15:00 | Premier League | Fulham v Newcastle | rejected | NO (Low) | 0.512 | NO LEAN | 20 | - | ok |
| 1557465 | Sat 07 Nov 17:30 | Premier League | Nottingham Forest v Manchester City | rejected | NO (Low) | 0.493 | NO LEAN | 18 | - | ok |
| 1557458 | Sun 08 Nov 14:00 | Premier League | Brighton v Brentford | rejected | NO (Medium) | 0.519 | NO LEAN | 16 | - | ok |
| 1557459 | Sun 08 Nov 14:00 | Premier League | Crystal Palace v Liverpool | rejected | NO (Medium) | 0.519 | NO LEAN | 12 | - | ok |
| 1557462 | Sun 08 Nov 14:00 | Premier League | Ipswich v Bournemouth | rejected | NO (Medium) | 0.523 | NO LEAN | 20 | - | ok |
| 1557466 | Sun 08 Nov 14:00 | Premier League | Sunderland v Chelsea | rejected | NO (Medium) | 0.514 | NO LEAN | 14 | - | ok |
| 1557464 | Sun 08 Nov 16:30 | Premier League | Manchester United v Aston Villa | rejected | NO (Medium) | 0.521 | NO LEAN | 22 | - | ok |
| 1575540 | Sat 07 Nov 15:30 | Primeira Liga | Nacional v Academico Viseu | rejected | NO (Medium) | 0.538 | NO LEAN | 21 | - | ok |
| 1575536 | Sat 07 Nov 18:00 | Primeira Liga | Alverca v Casa Pia | rejected | NO (Medium) | 0.519 | NO LEAN | 17 | - | ok |
| 1575543 | Sat 07 Nov 20:30 | Primeira Liga | Sporting CP v Moreirense | rejected | NO (Medium) | 0.540 | LEAN YES | 27 | moderate | needs review |
| 1575537 | Sun 08 Nov 15:30 | Primeira Liga | Estoril v Maritimo | rejected | NO (Medium) | 0.534 | NO LEAN | 22 | - | ok |
| 1575542 | Sun 08 Nov 15:30 | Primeira Liga | Santa Clara v GIL Vicente | rejected | NO (Medium) | 0.517 | NO LEAN | 15 | - | ok |
| 1575544 | Sun 08 Nov 18:00 | Primeira Liga | Vitória SC v FC Porto | rejected | NO (Medium) | 0.549 | NO LEAN | 18 | - | ok |
| 1575538 | Sun 08 Nov 20:30 | Primeira Liga | Estrela v Benfica | rejected | NO (Medium) | 0.546 | NO LEAN | 19 | - | ok |
| 1575541 | Sun 08 Nov 20:30 | Primeira Liga | Rio Ave v SC Braga | rejected | NO (Medium) | 0.535 | NO LEAN | 18 | - | ok |
| 1556702 | Sat 07 Nov 15:00 | Scottish Premiership | Dundee Utd v Motherwell | rejected | NO (Medium) | 0.558 | NO LEAN | 21 | - | ok |
| 1556703 | Sat 07 Nov 15:00 | Scottish Premiership | ST Johnstone v Dundee | rejected | NO (Medium) | 0.554 | LEAN YES | 28 | moderate | needs review |
| 1556700 | Sat 07 Nov 17:45 | Scottish Premiership | Aberdeen v Hibernian | rejected | NO (Medium) | 0.546 | LEAN YES | 23 | mild | note |
| 1556704 | Sat 07 Nov 20:00 | Scottish Premiership | ST Mirren v Rangers | rejected | NO (Medium) | 0.564 | NO LEAN | 22 | - | ok |
| 1556705 | Sun 08 Nov 15:00 | Scottish Premiership | Heart Of Midlothian v Falkirk | rejected | NO (Medium) | 0.551 | NO LEAN | 20 | - | ok |
| 1556701 | Sun 08 Nov 16:00 | Scottish Premiership | Celtic v Kilmarnock | Medium | NO (Medium) | 0.568 | LEAN YES | 24 | mild | note |
| 1584460 | Sat 07 Nov 10:30 | Super Lig | Eyüpspor v Kocaelispor | rejected | NO (Medium) | 0.515 | NO LEAN | 16 | - | ok |
| 1584465 | Sat 07 Nov 13:00 | Super Lig | Samsunspor v Konyaspor | rejected | NO (Medium) | 0.533 | NO LEAN | 13 | - | ok |
| 1584461 | Sat 07 Nov 16:00 | Super Lig | Galatasaray v Amed | Medium | NO (Medium) | 0.556 | LEAN YES | 23 | mild | note |
| 1584463 | Sat 07 Nov 16:00 | Super Lig | Göztepe v Başakşehir | Medium | NO (Medium) | 0.563 | NO LEAN | 18 | - | ok |
| 1584464 | Sun 08 Nov 10:30 | Super Lig | Rizespor v Erzurumspor FK | rejected | NO (Medium) | 0.560 | NO LEAN | 16 | - | ok |
| 1584459 | Sun 08 Nov 13:00 | Super Lig | Çorum FK v Fenerbahçe | Medium | NO (Medium) | 0.554 | NO LEAN | 19 | - | ok |
| 1584457 | Sun 08 Nov 15:30 | Super Lig | Alanyaspor v Trabzonspor | rejected | NO (Medium) | 0.567 | NO LEAN | 15 | - | ok |
| 1584458 | Sun 08 Nov 18:00 | Super Lig | Beşiktaş v Gençlerbirliği S.K. | Medium | NO (Medium) | 0.569 | NO LEAN | 16 | - | ok |