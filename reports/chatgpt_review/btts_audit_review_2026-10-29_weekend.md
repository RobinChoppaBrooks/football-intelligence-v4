# BTTS audit review: weekend_20261029_0917

Audit version btts_audit_v1, created 2026-10-29 16:08 UTC. Production outputs for this run are unchanged; this file is a second, independent reading of the same evidence.
Fixtures: 274. Flags: none 174, severe 36, mild 27, moderate 22, data 8, note 7.

How to read: the production BTTS verdict is a hand rule (YES exactly when the goal pattern is 'Both teams contribute', which needs an Over 2.5 route for each side).
The audit assessment uses the trained BTTS model band plus the card counts. Neither is overridden; both are listed so each can be scored against the result.
Model bands: High p >= 0.575, Medium p >= 0.514. Evidence score 0 to 30 = each side's scored-in + conceded-in + BTTS counts of 5, with venue adjustments.

## Severe (36)

### Cercle Brugge v Antwerp  (Belgian Pro League, Sun 01 Nov 12:30 UK)  fixture_id 1558664
- Over 2.5: Medium (model score 0.608). Production BTTS: NO (High, p 0.582). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.582 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Cercle Brugge: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 4/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 0-3; 1-1; 2-3; 1-2; 2-5. Home last 3: 0-1; 0-3; 1-2 (BTTS 1/3).
- Antwerp: scored in 3/5, 2+ in 1/5, conceded in 4/5, 2+ against in 3/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 0-1; 1-3; 0-2; 1-5; 3-0. Away last 3: 0-1; 1-3; 1-5 (BTTS 2/3).
- Evidence score: 21. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.582). Cercle Brugge scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Antwerp scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5.

### St. Truiden v OH Leuven  (Belgian Pro League, Sun 01 Nov 15:00 UK)  fixture_id 1558669
- Over 2.5: rejected (model score 0.58). Production BTTS: NO (High, p 0.575). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.575 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- St. Truiden: scored in 3/5, 2+ in 3/5, conceded in 4/5, 2+ against in 4/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 4-0; 0-2; 0-2; 3-4; 2-3. Home last 3: 0-3; 4-0; 0-2 (BTTS 0/3).
- OH Leuven: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 0-3; 1-1; 2-0; 1-1; 2-2. Away last 3: 0-1; 0-3; 1-1 (BTTS 1/3).
- Evidence score: 18. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.575). St. Truiden scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5; OH Leuven scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Charleroi v RAAL La Louvière  (Belgian Pro League, Sun 01 Nov 18:15 UK)  fixture_id 1558665
- Over 2.5: Medium (model score 0.599). Production BTTS: NO (High, p 0.582). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.582 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Charleroi: scored in 4/5, 2+ in 2/5, conceded in 3/5, 2+ against in 3/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 2-3; 1-0; 3-2; 1-0; 0-3. Home last 3: 2-0; 2-3; 3-2 (BTTS 2/3).
- RAAL La Louvière: scored in 3/5, 2+ in 2/5, conceded in 3/5, 2+ against in 3/5, BTTS 1/5, clean sheets 2/5, failed to score 2/5. Last five: 0-4; 3-0; 0-2; 1-4; 3-0. Away last 3: 0-2; 0-4; 0-2 (BTTS 0/3).
- Evidence score: 15. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.582). Charleroi scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5; RAAL La Louvière scored in 3 of 5, conceded in 3 of 5, BTTS 1 of 5.

### SV Elversberg v FSV Mainz 05  (Bundesliga, Fri 30 Oct 19:30 UK)  fixture_id 1575211
- Over 2.5: High (model score 0.649). Production BTTS: NO (High, p 0.591). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.591 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- SV Elversberg: scored in 2/5, 2+ in 1/5, conceded in 4/5, 2+ against in 3/5, BTTS 2/5, clean sheets 1/5, failed to score 3/5. Last five: 1-2; 0-0; 0-1; 4-3; 0-4. Home last 3: 3-2; 1-2; 4-3 (BTTS 3/3).
- FSV Mainz 05: scored in 5/5, 2+ in 3/5, conceded in 4/5, 2+ against in 4/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-3; 4-3; 3-4; 1-0; 2-3. Away last 3: 5-0; 4-3; 1-0 (BTTS 1/3).
- Evidence score: 21. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.591). SV Elversberg scored in 2 of 5, conceded in 4 of 5, BTTS 2 of 5; FSV Mainz 05 scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Bayer Leverkusen v VfB Stuttgart  (Bundesliga, Sat 31 Oct 14:30 UK)  fixture_id 1575204
- Over 2.5: High (model score 0.634). Production BTTS: NO (High, p 0.578). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.578 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Bayer Leverkusen: scored in 4/5, 2+ in 4/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 2-2; 2-0; 4-3; 2-1; 0-3. Home last 3: 4-0; 2-0; 2-1 (BTTS 1/3).
- VfB Stuttgart: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 1-2; 0-1; 2-0; 0-1; 2-3. Away last 3: 1-2; 2-0; 0-1 (BTTS 1/3).
- Evidence score: 19. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.578). Bayer Leverkusen scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; VfB Stuttgart scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5.

### Borussia Monchengladbach v SC Paderborn 07  (Bundesliga, Sat 31 Oct 14:30 UK)  fixture_id 1575208
- Over 2.5: High (model score 0.642). Production BTTS: NO (High, p 0.606). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.606 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Borussia Monchengladbach: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 5/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 0-5; 3-4; 1-2; 1-2; 3-2. Home last 3: 3-4; 3-4; 1-2 (BTTS 3/3).
- SC Paderborn 07: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 0-3; 3-1; 0-2; 2-2; 1-0. Away last 3: 0-0; 0-3; 2-2 (BTTS 1/3).
- Evidence score: 22. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.606). Borussia Monchengladbach scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; SC Paderborn 07 scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5.

### Bayern Munich v Borussia Dortmund  (Bundesliga, Sat 31 Oct 17:30 UK)  fixture_id 1575203
- Over 2.5: Medium (model score 0.701). Production BTTS: NO (High, p 0.576). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.576 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Bayern Munich: scored in 5/5, 2+ in 5/5, conceded in 4/5, 2+ against in 1/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-1; 7-0; 2-2; 6-1; 3-1. Home last 3: 5-1; 7-0; 6-1 (BTTS 2/3).
- Borussia Dortmund: scored in 4/5, 2+ in 2/5, conceded in 1/5, 2+ against in 1/5, BTTS 1/5, clean sheets 4/5, failed to score 1/5. Last five: 3-0; 1-0; 2-2; 0-0; 1-0. Away last 3: 3-2; 1-0; 0-0 (BTTS 1/3).
- Evidence score: 18. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.576). Bayern Munich scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Borussia Dortmund scored in 4 of 5, conceded in 1 of 5, BTTS 1 of 5.

### Eintracht Frankfurt v Hamburger SV  (Bundesliga, Sun 01 Nov 16:30 UK)  fixture_id 1575205
- Over 2.5: Medium (model score 0.642). Production BTTS: NO (High, p 0.584). Pattern: Low scoring.
- Audit assessment: YES. BTTS model High band (p 0.584 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Eintracht Frankfurt: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 3-1; 2-2; 0-6; 1-0; 0-1. Home last 3: 1-4; 2-2; 1-0 (BTTS 2/3).
- Hamburger SV: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 0-5; 2-1; 3-2; 1-0; 0-1. Away last 3: 0-5; 3-2; 0-1 (BTTS 1/3).
- Evidence score: 17. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'Low scoring', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.584). Eintracht Frankfurt scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5; Hamburger SV scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5.

### Fredrikstad v Rosenborg  (Eliteserien, Sat 31 Oct 15:00 UK)  fixture_id 1494791
- Over 2.5: Medium (model score 0.609). Production BTTS: NO (High, p 0.581). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.581 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Fredrikstad: scored in 5/5, 2+ in 1/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-1; 1-1; 1-1; 2-3; 1-5. Home last 3: 1-2; 1-1; 1-1 (BTTS 3/3).
- Rosenborg: scored in 5/5, 2+ in 4/5, conceded in 3/5, 2+ against in 1/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 5-3; 3-1; 1-1; 3-0; 3-0. Away last 3: 3-1; 3-0; 3-0 (BTTS 1/3).
- Evidence score: 26. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.581). Fredrikstad scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Rosenborg scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5.

### Aalesund v Sandefjord  (Eliteserien, Sat 31 Oct 17:00 UK)  fixture_id 1494788
- Over 2.5: Medium (model score 0.607). Production BTTS: NO (High, p 0.586). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.586 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Aalesund: scored in 5/5, 2+ in 3/5, conceded in 5/5, 2+ against in 3/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-2; 2-1; 2-4; 4-1; 1-2. Home last 3: 5-5; 2-0; 2-4 (BTTS 2/3).
- Sandefjord: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 2-3; 3-0; 1-1; 0-2; 0-1. Away last 3: 2-3; 1-1; 0-1 (BTTS 2/3).
- Evidence score: 24. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.586). Aalesund scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Sandefjord scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5.

### Brann v Molde  (Eliteserien, Sun 01 Nov 13:30 UK)  fixture_id 1494790
- Over 2.5: High (model score 0.67). Production BTTS: NO (High, p 0.576). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.576 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Brann: scored in 3/5, 2+ in 2/5, conceded in 5/5, 2+ against in 4/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 0-2; 2-1; 0-2; 1-3; 2-3. Home last 3: 1-2; 2-1; 0-2 (BTTS 2/3).
- Molde: scored in 5/5, 2+ in 4/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 5-1; 1-2; 2-2; 6-1; 5-1. Away last 3: 4-3; 5-1; 2-2 (BTTS 3/3).
- Evidence score: 27. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.576). Brann scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5; Molde scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### KFUM Oslo v Ham-Kam  (Eliteserien, Sun 01 Nov 16:00 UK)  fixture_id 1494792
- Over 2.5: Medium (model score 0.63). Production BTTS: NO (High, p 0.575). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.575 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- KFUM Oslo: scored in 5/5, 2+ in 4/5, conceded in 5/5, 2+ against in 1/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-1; 3-1; 2-1; 1-1; 2-2. Home last 3: 1-1; 2-1; 2-1 (BTTS 3/3).
- Ham-Kam: scored in 3/5, 2+ in 2/5, conceded in 5/5, 2+ against in 5/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 1-5; 2-3; 4-2; 0-2; 0-3. Away last 3: 0-4; 2-3; 4-2 (BTTS 2/3).
- Evidence score: 27. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.575). KFUM Oslo scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Ham-Kam scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Feyenoord v Fortuna Sittard  (Eredivisie, Sat 31 Oct 15:30 UK)  fixture_id 1552207
- Over 2.5: Medium (model score 0.687). Production BTTS: NO (High, p 0.622). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.622 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Feyenoord: scored in 5/5, 2+ in 4/5, conceded in 2/5, 2+ against in 1/5, BTTS 2/5, clean sheets 3/5, failed to score 0/5. Last five: 7-0; 5-0; 2-0; 4-3; 1-1. Home last 3: 2-2; 5-0; 2-0 (BTTS 1/3).
- Fortuna Sittard: scored in 5/5, 2+ in 1/5, conceded in 3/5, 2+ against in 2/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 1-5; 1-0; 1-1; 2-2; 1-0. Away last 3: 3-2; 1-0; 2-2 (BTTS 2/3).
- Evidence score: 19. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.622). Feyenoord scored in 5 of 5, conceded in 2 of 5, BTTS 2 of 5; Fortuna Sittard scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5.

### Heerenveen v NEC Nijmegen  (Eredivisie, Sat 31 Oct 17:45 UK)  fixture_id 1552208
- Over 2.5: Medium (model score 0.667). Production BTTS: NO (High, p 0.605). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.605 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Heerenveen: scored in 3/5, 2+ in 3/5, conceded in 2/5, 2+ against in 2/5, BTTS 1/5, clean sheets 3/5, failed to score 2/5. Last five: 0-0; 4-0; 0-2; 4-0; 3-2. Home last 3: 2-3; 0-0; 4-0 (BTTS 1/3).
- NEC Nijmegen: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 0-3; 1-1; 1-1; 2-2; 2-2. Away last 3: 3-1; 0-3; 1-1 (BTTS 2/3).
- Evidence score: 18. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.605). Heerenveen scored in 3 of 5, conceded in 2 of 5, BTTS 1 of 5; NEC Nijmegen scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### PSV Eindhoven v Willem II  (Eredivisie, Sat 31 Oct 17:45 UK)  fixture_id 1552209
- Over 2.5: High (model score 0.646). Production BTTS: NO (High, p 0.611). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.611 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- PSV Eindhoven: scored in 5/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 4-1; 2-3; 2-0; 1-2; 1-1. Home last 3: 4-1; 2-0; 1-1 (BTTS 2/3).
- Willem II: scored in 4/5, 2+ in 1/5, conceded in 5/5, 2+ against in 4/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-5; 0-1; 1-3; 2-3; 1-6. Away last 3: 1-5; 1-3; 2-3 (BTTS 3/3).
- Evidence score: 27. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.611). PSV Eindhoven scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Willem II scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Ajax v AZ Alkmaar  (Eredivisie, Sat 31 Oct 20:00 UK)  fixture_id 1552210
- Over 2.5: High (model score 0.691). Production BTTS: NO (High, p 0.576). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.576 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Ajax: scored in 5/5, 2+ in 4/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 5-1; 2-2; 1-1; 5-2; 2-1. Home last 3: 5-1; 2-2; 1-1 (BTTS 3/3).
- AZ Alkmaar: scored in 3/5, 2+ in 1/5, conceded in 4/5, 2+ against in 3/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 1-1; 1-0; 0-2; 2-2; 0-2. Away last 3: 3-2; 0-2; 2-2 (BTTS 2/3).
- Evidence score: 25. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.576). Ajax scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; AZ Alkmaar scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5.

### Cambuur v GO Ahead Eagles  (Eredivisie, Sat 31 Oct 20:00 UK)  fixture_id 1552211
- Over 2.5: High (model score 0.67). Production BTTS: NO (High, p 0.613). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.613 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Cambuur: scored in 5/5, 2+ in 3/5, conceded in 3/5, 2+ against in 1/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 3-0; 1-1; 1-0; 2-2; 6-1. Home last 3: 1-4; 3-0; 2-2 (BTTS 2/3).
- GO Ahead Eagles: scored in 5/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-1; 1-1; 3-3; 1-4; 3-2. Away last 3: 3-3; 1-1; 1-4 (BTTS 3/3).
- Evidence score: 27. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.613). Cambuur scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5; GO Ahead Eagles scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### PEC Zwolle v ADO Den Haag  (Eredivisie, Sun 01 Nov 11:15 UK)  fixture_id 1552212
- Over 2.5: Medium (model score 0.645). Production BTTS: NO (High, p 0.610). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.610 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- PEC Zwolle: scored in 2/5, 2+ in 1/5, conceded in 5/5, 2+ against in 2/5, BTTS 2/5, clean sheets 0/5, failed to score 3/5. Last five: 0-7; 0-3; 0-1; 4-1; 1-1. Home last 3: 0-7; 0-1; 4-1 (BTTS 1/3).
- ADO Den Haag: scored in 4/5, 2+ in 3/5, conceded in 5/5, 2+ against in 3/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 0-2; 1-1; 2-2; 2-1; 2-3. Away last 3: 2-2; 0-2; 2-2 (BTTS 2/3).
- Evidence score: 21. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.610). PEC Zwolle scored in 2 of 5, conceded in 5 of 5, BTTS 2 of 5; ADO Den Haag scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Excelsior v Twente  (Eredivisie, Sun 01 Nov 13:30 UK)  fixture_id 1552213
- Over 2.5: Medium (model score 0.623). Production BTTS: NO (High, p 0.608). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.608 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Excelsior: scored in 3/5, 2+ in 1/5, conceded in 5/5, 2+ against in 4/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 1-2; 2-2; 1-5; 0-4; 0-1. Home last 3: 2-1; 1-2; 1-5 (BTTS 3/3).
- Twente: scored in 5/5, 2+ in 3/5, conceded in 3/5, 2+ against in 2/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 2-0; 3-2; 1-1; 1-2; 2-0. Away last 3: 2-2; 1-1; 2-0 (BTTS 2/3).
- Evidence score: 23. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.608). Excelsior scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5; Twente scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5.

### Telstar v Utrecht  (Eredivisie, Sun 01 Nov 13:30 UK)  fixture_id 1552214
- Over 2.5: High (model score 0.654). Production BTTS: NO (High, p 0.604). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.604 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Telstar: scored in 3/5, 2+ in 3/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 2/5. Last five: 0-0; 0-1; 2-2; 3-4; 2-3. Home last 3: 2-2; 2-2; 3-4 (BTTS 3/3).
- Utrecht: scored in 4/5, 2+ in 3/5, conceded in 5/5, 2+ against in 1/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 2-1; 0-5; 3-1; 2-1; 1-1. Away last 3: 2-1; 0-5; 2-1 (BTTS 2/3).
- Evidence score: 24. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.604). Telstar scored in 3 of 5, conceded in 4 of 5, BTTS 3 of 5; Utrecht scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Groningen v Sparta Rotterdam  (Eredivisie, Sun 01 Nov 15:45 UK)  fixture_id 1552215
- Over 2.5: High (model score 0.676). Production BTTS: NO (High, p 0.612). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.612 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Groningen: scored in 5/5, 2+ in 4/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-1; 3-0; 5-1; 2-5; 2-2. Home last 3: 2-2; 3-0; 2-5 (BTTS 2/3).
- Sparta Rotterdam: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 5/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-4; 0-4; 3-3; 3-2; 1-2. Away last 3: 1-2; 1-4; 3-3 (BTTS 3/3).
- Evidence score: 27. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.612). Groningen scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Sparta Rotterdam scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Cheshunt v Chatham Town  (Isthmian Premier, Sat 31 Oct 15:00 UK)  fixture_id 1598835
- Over 2.5: Medium (model score 0.614). Production BTTS: NO (High, p 0.588). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.588 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Cheshunt: scored in 4/5, 2+ in 3/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 2-1; 2-1; 1-1; 0-3; 2-4. Home last 3: 3-1; 2-1; 1-1 (BTTS 3/3).
- Chatham Town: scored in 3/5, 2+ in 3/5, conceded in 3/5, 2+ against in 2/5, BTTS 1/5, clean sheets 2/5, failed to score 2/5. Last five: 3-0; 0-1; 4-0; 3-2; 0-4. Away last 3: 0-1; 4-0; 0-4 (BTTS 0/3).
- Evidence score: 20. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.588). Cheshunt scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Chatham Town scored in 3 of 5, conceded in 3 of 5, BTTS 1 of 5.

### Leatherhead v Stanway Rovers  (Isthmian Premier, Sat 31 Oct 15:00 UK)  fixture_id 1598837
- Over 2.5: Medium (model score 0.624). Production BTTS: NO (High, p 0.585). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.585 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Leatherhead: scored in 2/5, 2+ in 1/5, conceded in 4/5, 2+ against in 3/5, BTTS 2/5, clean sheets 1/5, failed to score 3/5. Last five: 0-0; 3-3; 0-3; 1-2; 0-1. Home last 3: 2-3; 0-0; 1-2 (BTTS 2/3).
- Stanway Rovers: scored in 4/5, 2+ in 1/5, conceded in 4/5, 2+ against in 4/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-2; 1-3; 1-4; 0-2; 3-0. Away last 3: 3-2; 1-4; 0-2 (BTTS 2/3).
- Evidence score: 19. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.585). Leatherhead scored in 2 of 5, conceded in 4 of 5, BTTS 2 of 5; Stanway Rovers scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Welling United v Carshalton Athletic  (Isthmian Premier, Sat 31 Oct 15:00 UK)  fixture_id 1598840
- Over 2.5: High (model score 0.632). Production BTTS: NO (High, p 0.583). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.583 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Welling United: scored in 4/5, 2+ in 2/5, conceded in 3/5, 2+ against in 2/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 1-0; 0-1; 4-2; 2-3; 1-0. Home last 3: 1-0; 4-2; 1-0 (BTTS 1/3).
- Carshalton Athletic: scored in 3/5, 2+ in 2/5, conceded in 5/5, 2+ against in 4/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 0-4; 0-1; 1-2; 2-2; 2-4. Away last 3: 3-2; 2-2; 2-4 (BTTS 3/3).
- Evidence score: 20. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.583). Welling United scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5; Carshalton Athletic scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Whitehawk v St Albans City  (Isthmian Premier, Sat 31 Oct 15:00 UK)  fixture_id 1598841
- Over 2.5: Medium (model score 0.619). Production BTTS: NO (High, p 0.581). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.581 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Whitehawk: scored in 3/5, 2+ in 0/5, conceded in 5/5, 2+ against in 3/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 0-1; 1-4; 0-5; 1-1; 1-2. Home last 3: 3-2; 1-4; 1-2 (BTTS 3/3).
- St Albans City: scored in 5/5, 2+ in 3/5, conceded in 3/5, 2+ against in 1/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 1-1; 4-0; 3-3; 1-0; 3-1. Away last 3: 1-1; 3-3; 1-0 (BTTS 2/3).
- Evidence score: 23. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.581). Whitehawk scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5; St Albans City scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5.

### Whyteleafe v Dulwich Hamlet  (Isthmian Premier, Sat 31 Oct 15:00 UK)  fixture_id 1598842
- Over 2.5: High (model score 0.642). Production BTTS: NO (High, p 0.583). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.583 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Whyteleafe: scored in 4/5, 2+ in 4/5, conceded in 4/5, 2+ against in 1/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 0-1; 2-1; 5-0; 2-1; 2-3. Home last 3: 5-0; 2-1; 2-3 (BTTS 2/3).
- Dulwich Hamlet: scored in 3/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 0-2; 2-2; 0-4; 1-1; 2-1. Away last 3: 0-2; 1-1; 2-1 (BTTS 2/3).
- Evidence score: 22. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.583). Whyteleafe scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Dulwich Hamlet scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Levante v Atletico Madrid  (La Liga, Sat 31 Oct 13:00 UK)  fixture_id 1570439
- Over 2.5: Medium (model score 0.584). Production BTTS: NO (High, p 0.576). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.576 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Levante: scored in 5/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-3; 3-3; 1-1; 3-1; 1-2. Home last 3: 2-4; 3-3; 3-1 (BTTS 3/3).
- Atletico Madrid: scored in 5/5, 2+ in 3/5, conceded in 2/5, 2+ against in 0/5, BTTS 2/5, clean sheets 3/5, failed to score 0/5. Last five: 4-0; 2-1; 2-1; 1-0; 1-0. Away last 3: 3-0; 2-1; 1-0 (BTTS 1/3).
- Evidence score: 24. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.576). Levante scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Atletico Madrid scored in 5 of 5, conceded in 2 of 5, BTTS 2 of 5.

### Alfreton Town v AFC Emley  (Northern Premier League, Sat 31 Oct 15:00 UK)  fixture_id 1596518
- Over 2.5: Medium (model score 0.61). Production BTTS: NO (High, p 0.577). Pattern: Low scoring.
- Audit assessment: YES. BTTS model High band (p 0.577 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Alfreton Town: scored in 4/5, 2+ in 1/5, conceded in 3/5, 2+ against in 2/5, BTTS 3/5, clean sheets 2/5, failed to score 1/5. Last five: 1-3; 1-0; 2-3; 0-0; 1-1. Home last 3: 1-0; 2-3; 1-1 (BTTS 2/3).
- AFC Emley: scored in 5/5, 2+ in 1/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-4; 1-2; 1-1; 3-1; 1-0. Away last 3: 1-4; 1-1; 3-1 (BTTS 3/3).
- Evidence score: 24. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'Low scoring', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.577). Alfreton Town scored in 4 of 5, conceded in 3 of 5, BTTS 3 of 5; AFC Emley scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Gainsborough Trinity v Bamber Bridge  (Northern Premier League, Sat 31 Oct 15:00 UK)  fixture_id 1596524
- Over 2.5: High (model score 0.641). Production BTTS: NO (High, p 0.578). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.578 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Gainsborough Trinity: scored in 4/5, 2+ in 4/5, conceded in 4/5, 2+ against in 1/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 2-1; 3-1; 4-0; 2-1; 0-3. Home last 3: 3-1; 4-0; 0-3 (BTTS 1/3).
- Bamber Bridge: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 2/5. Last five: 2-5; 2-4; 0-0; 0-1; 1-2. Away last 3: 1-3; 2-5; 0-0 (BTTS 2/3).
- Evidence score: 21. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.578). Gainsborough Trinity scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Bamber Bridge scored in 3 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Ilkeston Town v Hyde United  (Northern Premier League, Sat 31 Oct 15:00 UK)  fixture_id 1596525
- Over 2.5: Medium (model score 0.624). Production BTTS: NO (High, p 0.580). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.580 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Ilkeston Town: scored in 3/5, 2+ in 1/5, conceded in 4/5, 2+ against in 4/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 1-2; 0-2; 0-5; 1-3; 2-0. Home last 3: 0-2; 0-5; 2-0 (BTTS 0/3).
- Hyde United: scored in 2/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 2/5, clean sheets 0/5, failed to score 3/5. Last five: 2-1; 0-1; 0-2; 2-2; 0-4. Away last 3: 0-1; 0-2; 0-4 (BTTS 0/3).
- Evidence score: 16. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.580). Ilkeston Town scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5; Hyde United scored in 2 of 5, conceded in 5 of 5, BTTS 2 of 5.

### United of Manchester v Lancaster City  (Northern Premier League, Sat 31 Oct 15:00 UK)  fixture_id 1596523
- Over 2.5: Medium (model score 0.637). Production BTTS: NO (High, p 0.585). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.585 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- United of Manchester: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 0-1; 2-2; 1-1; 4-2; 1-1. Home last 3: 1-1; 4-2; 1-1 (BTTS 3/3).
- Lancaster City: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 3-5; 2-2; 1-0; 1-2; 0-1. Away last 3: 3-5; 2-2; 0-1 (BTTS 2/3).
- Evidence score: 25. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.585). United of Manchester scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Lancaster City scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Edinburgh City v Dumbarton  (Scottish League Two, Sat 31 Oct 15:00 UK)  fixture_id 1557804
- Over 2.5: Medium (model score 0.628). Production BTTS: NO (High, p 0.590). Pattern: Low scoring.
- Audit assessment: YES. BTTS model High band (p 0.590 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Edinburgh City: scored in 3/5, 2+ in 2/5, conceded in 3/5, 2+ against in 2/5, BTTS 3/5, clean sheets 2/5, failed to score 2/5. Last five: 7-3; 3-1; 0-0; 1-3; 0-0. Home last 3: 1-1; 7-3; 1-3 (BTTS 3/3).
- Dumbarton: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-3; 3-0; 2-1; 1-2; 1-1. Away last 3: 0-2; 1-3; 1-2 (BTTS 2/3).
- Evidence score: 23. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'Low scoring', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.590). Edinburgh City scored in 3 of 5, conceded in 3 of 5, BTTS 3 of 5; Dumbarton scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Kelty Hearts v Elgin City  (Scottish League Two, Sat 31 Oct 15:00 UK)  fixture_id 1557805
- Over 2.5: High (model score 0.637). Production BTTS: NO (High, p 0.583). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.583 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Kelty Hearts: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-4; 1-3; 2-0; 1-2; 2-1. Home last 3: 2-1; 1-3; 2-1 (BTTS 3/3).
- Elgin City: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 2/5. Last five: 0-2; 1-5; 6-2; 2-1; 0-0. Away last 3: 1-2; 0-2; 2-1 (BTTS 2/3).
- Evidence score: 24. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.583). Kelty Hearts scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Elgin City scored in 3 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Spartans v Annan Athletic  (Scottish League Two, Sat 31 Oct 15:00 UK)  fixture_id 1557806
- Over 2.5: Medium (model score 0.621). Production BTTS: NO (High, p 0.579). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.579 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Spartans: scored in 2/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 2/5, clean sheets 0/5, failed to score 3/5. Last five: 5-1; 0-3; 0-2; 3-1; 0-2. Home last 3: 5-1; 0-2; 0-2 (BTTS 1/3).
- Annan Athletic: scored in 3/5, 2+ in 1/5, conceded in 4/5, 2+ against in 2/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 2-0; 0-1; 0-1; 1-6; 1-4. Away last 3: 1-2; 0-1; 1-4 (BTTS 2/3).
- Evidence score: 17. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.579). Spartans scored in 2 of 5, conceded in 5 of 5, BTTS 2 of 5; Annan Athletic scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5.

### Stirling Albion v Forfar Athletic  (Scottish League Two, Sat 31 Oct 15:00 UK)  fixture_id 1557807
- Over 2.5: High (model score 0.634). Production BTTS: NO (High, p 0.578). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.578 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Stirling Albion: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 1/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 3-7; 1-1; 1-0; 2-1; 1-1. Home last 3: 0-2; 1-1; 2-1 (BTTS 2/3).
- Forfar Athletic: scored in 5/5, 2+ in 0/5, conceded in 4/5, 2+ against in 4/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-5; 1-0; 1-2; 1-2; 1-2. Away last 3: 1-5; 1-2; 1-2 (BTTS 3/3).
- Evidence score: 27. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.578). Stirling Albion scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Forfar Athletic scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Wimborne Town v Chippenham Town  (Southern Premier South, Sat 31 Oct 15:00 UK)  fixture_id 1597441
- Over 2.5: High (model score 0.65). Production BTTS: NO (High, p 0.586). Pattern: One side dominates.
- Audit assessment: YES. BTTS model High band (p 0.586 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Wimborne Town: scored in 4/5, 2+ in 3/5, conceded in 2/5, 2+ against in 2/5, BTTS 2/5, clean sheets 3/5, failed to score 1/5. Last five: 4-0; 6-3; 1-2; 3-0; 0-0. Home last 3: 4-0; 6-3; 3-0 (BTTS 1/3).
- Chippenham Town: scored in 3/5, 2+ in 1/5, conceded in 5/5, 2+ against in 4/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 0-2; 2-2; 0-2; 1-4; 1-1. Away last 3: 0-2; 2-2; 1-1 (BTTS 2/3).
- Evidence score: 18. Flag: severe. Review status: needs review.
- Why flagged: Verdict NO comes from the goal pattern 'One side dominates', which needs an Over 2.5 route (2+ goals) for each side; BTTS only needs one goal each. The BTTS model itself is in its High band (p 0.586). Wimborne Town scored in 4 of 5, conceded in 2 of 5, BTTS 2 of 5; Chippenham Town scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

## Moderate (22)

### SCR Altach v Ried  (Austrian Bundesliga, Sat 31 Oct 16:00 UK)  fixture_id 1561954
- Over 2.5: Medium (model score 0.604). Production BTTS: NO (Medium, p 0.568). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.568) with supporting evidence (score 25, both sides BTTS at least 2 of 5); 55% to 59% historically.
- SCR Altach: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 1-2; 0-2; 3-0; 0-3; 2-1. Home last 3: 1-2; 3-0; 2-1 (BTTS 2/3).
- Ried: scored in 5/5, 2+ in 4/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-1; 4-1; 2-1; 3-2; 2-2. Away last 3: 2-3; 2-1; 2-2 (BTTS 3/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.568). SCR Altach scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5; Ried scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### Burnley v Portsmouth  (Championship, Sat 31 Oct 15:00 UK)  fixture_id 1563228
- Over 2.5: rejected (model score 0.546). Production BTTS: NO (Medium, p 0.559). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.559) with supporting evidence (score 25, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Burnley: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-1; 4-0; 2-2; 1-2; 1-4. Home last 3: 1-1; 2-2; 1-2 (BTTS 3/3).
- Portsmouth: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 1/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 0-1; 3-2; 1-0; 1-1; 2-1. Away last 3: 0-1; 1-0; 1-1 (BTTS 1/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.559). Burnley scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Portsmouth scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Millwall v Derby  (Championship, Sat 31 Oct 15:00 UK)  fixture_id 1563231
- Over 2.5: rejected (model score 0.531). Production BTTS: NO (Medium, p 0.547). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.547) with supporting evidence (score 25, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Millwall: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 2-2; 1-0; 0-1; 2-2; 1-2. Home last 3: 2-2; 0-1; 2-2 (BTTS 2/3).
- Derby: scored in 4/5, 2+ in 0/5, conceded in 5/5, 2+ against in 1/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 1-1; 1-4; 0-1; 1-1. Away last 3: 1-1; 1-4; 1-1 (BTTS 3/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.547). Millwall scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Derby scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Gornik Zabrze v Legia Warszawa  (Ekstraklasa, Fri 30 Oct 19:30 UK)  fixture_id 1553211
- Over 2.5: rejected (model score 0.548). Production BTTS: NO (Medium, p 0.544). Pattern: Low scoring.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.544) with supporting evidence (score 25, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Gornik Zabrze: scored in 4/5, 2+ in 2/5, conceded in 3/5, 2+ against in 0/5, BTTS 3/5, clean sheets 2/5, failed to score 1/5. Last five: 2-0; 0-0; 3-1; 1-1; 1-1. Home last 3: 2-3; 2-1; 1-1 (BTTS 3/3).
- Legia Warszawa: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 1/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-1; 3-1; 2-0; 1-1; 1-2. Away last 3: 3-2; 3-1; 1-1 (BTTS 3/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'Low scoring' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.544). Gornik Zabrze scored in 4 of 5, conceded in 3 of 5, BTTS 3 of 5; Legia Warszawa scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Valerenga v Tromso  (Eliteserien, Sun 01 Nov 18:15 UK)  fixture_id 1494795
- Over 2.5: Medium (model score 0.6). Production BTTS: NO (Medium, p 0.569). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.569) with supporting evidence (score 28, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Valerenga: scored in 4/5, 2+ in 1/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 0-2; 1-1; 1-2; 3-1; 1-0. Home last 3: 3-4; 1-1; 3-1 (BTTS 3/3).
- Tromso: scored in 5/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 3-5; 3-2; 1-1; 1-1; 1-3. Away last 3: 3-5; 1-1; 1-3 (BTTS 3/3).
- Evidence score: 28. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 28). Model Medium (p 0.569). Valerenga scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Tromso scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### PAOK v Asteras Tripolis  (Greek Super League, Sun 01 Nov 17:00 UK)  fixture_id 1593351
- Over 2.5: rejected (model score 0.556). Production BTTS: NO (Medium, p 0.551). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.551) with supporting evidence (score 26, both sides BTTS at least 4 of 5); 55% to 59% historically.
- PAOK: scored in 5/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-0; 3-1; 1-3; 2-1; 1-2. Home last 3: 2-0; 1-3; 2-1 (BTTS 2/3).
- Asteras Tripolis: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 1/5. Last five: 1-1; 2-2; 2-1; 1-5; 0-0. Away last 3: 1-3; 2-2; 1-5 (BTTS 3/3).
- Evidence score: 26. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 26). Model Medium (p 0.551). PAOK scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Asteras Tripolis scored in 4 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Racing Santander v Real Madrid  (La Liga, Sun 01 Nov 15:15 UK)  fixture_id 1570440
- Over 2.5: Medium (model score 0.59). Production BTTS: NO (Medium, p 0.571). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.571) with supporting evidence (score 26, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Racing Santander: scored in 3/5, 2+ in 3/5, conceded in 5/5, 2+ against in 4/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 2-7; 0-5; 2-2; 0-2; 2-1. Home last 3: 2-1; 2-2; 2-1 (BTTS 3/3).
- Real Madrid: scored in 5/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 3-2; 1-2; 1-0; 4-1; 2-1. Away last 3: 3-2; 1-2; 2-1 (BTTS 3/3).
- Evidence score: 26. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 26). Model Medium (p 0.571). Racing Santander scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5; Real Madrid scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Barnsley v Oxford United  (League One, Sat 31 Oct 15:00 UK)  fixture_id 1564391
- Over 2.5: rejected (model score 0.54). Production BTTS: NO (Medium, p 0.547). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.547) with supporting evidence (score 26, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Barnsley: scored in 5/5, 2+ in 0/5, conceded in 5/5, 2+ against in 4/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-1; 1-3; 1-2; 1-2; 1-2. Home last 3: 1-5; 1-1; 1-2 (BTTS 3/3).
- Oxford United: scored in 4/5, 2+ in 2/5, conceded in 3/5, 2+ against in 0/5, BTTS 3/5, clean sheets 2/5, failed to score 1/5. Last five: 2-1; 1-1; 2-1; 0-0; 1-0. Away last 3: 4-0; 2-1; 1-1 (BTTS 2/3).
- Evidence score: 26. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 26). Model Medium (p 0.547). Barnsley scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Oxford United scored in 4 of 5, conceded in 3 of 5, BTTS 3 of 5.

### Peterborough v Luton  (League One, Sat 31 Oct 15:00 UK)  fixture_id 1564397
- Over 2.5: rejected (model score 0.561). Production BTTS: NO (Medium, p 0.568). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.568) with supporting evidence (score 29, both sides BTTS at least 4 of 5); 55% to 59% historically.
- Peterborough: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 0-1; 3-1; 2-2; 1-4; 1-1. Home last 3: 1-2; 0-2; 2-2 (BTTS 2/3).
- Luton: scored in 5/5, 2+ in 4/5, conceded in 5/5, 2+ against in 1/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 4-1; 1-2; 2-1; 2-1; 3-1. Away last 3: 1-2; 4-1; 1-2 (BTTS 3/3).
- Evidence score: 29. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 29). Model Medium (p 0.568). Peterborough scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Luton scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### Crewe v Barnet  (League Two, Sat 31 Oct 15:00 UK)  fixture_id 1563841
- Over 2.5: rejected (model score 0.536). Production BTTS: NO (Medium, p 0.533). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.533) with supporting evidence (score 28, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Crewe: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 3-1; 1-0; 3-2; 0-2; 1-5. Home last 3: 1-1; 3-1; 3-2 (BTTS 3/3).
- Barnet: scored in 5/5, 2+ in 3/5, conceded in 5/5, 2+ against in 1/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 3-1; 2-1; 1-3; 1-1; 3-1. Away last 3: 3-3; 3-1; 2-1 (BTTS 3/3).
- Evidence score: 28. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 28). Model Medium (p 0.533). Crewe scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Barnet scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### Lille v Lens  (Ligue 1, Fri 30 Oct 20:05 UK)  fixture_id 1552802
- Over 2.5: rejected (model score 0.523). Production BTTS: NO (Medium, p 0.545). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.545) with supporting evidence (score 26, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Lille: scored in 5/5, 2+ in 1/5, conceded in 3/5, 2+ against in 1/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 2-0; 1-2; 1-0; 1-1; 1-1. Home last 3: 2-0; 1-0; 1-1 (BTTS 1/3).
- Lens: scored in 5/5, 2+ in 4/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-2; 1-2; 2-1; 3-1; 2-1. Away last 3: 2-2; 1-2; 3-1 (BTTS 3/3).
- Evidence score: 26. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 26). Model Medium (p 0.545). Lille scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5; Lens scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### Strasbourg v Auxerre  (Ligue 1, Sun 01 Nov 14:00 UK)  fixture_id 1552808
- Over 2.5: rejected (model score 0.542). Production BTTS: NO (Medium, p 0.554). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.554) with supporting evidence (score 28, both sides BTTS at least 4 of 5); 55% to 59% historically.
- Strasbourg: scored in 4/5, 2+ in 0/5, conceded in 5/5, 2+ against in 4/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 1-2; 1-2; 1-3; 0-3. Home last 3: 2-1; 1-1; 1-3 (BTTS 3/3).
- Auxerre: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 1/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-0; 2-1; 1-4; 3-1; 1-1. Away last 3: 1-3; 1-4; 3-1 (BTTS 3/3).
- Evidence score: 28. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 28). Model Medium (p 0.554). Strasbourg scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Auxerre scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Wealdstone v Southend  (National League, Sat 31 Oct 15:00 UK)  fixture_id 1585326
- Over 2.5: Medium (model score 0.613). Production BTTS: NO (Medium, p 0.572). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.572) with supporting evidence (score 27, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Wealdstone: scored in 4/5, 2+ in 1/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-1; 1-2; 0-6; 1-0; 2-3. Home last 3: 4-0; 0-6; 2-3 (BTTS 1/3).
- Southend: scored in 5/5, 2+ in 4/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-1; 3-1; 2-1; 2-2; 3-3. Away last 3: 1-1; 2-1; 3-3 (BTTS 3/3).
- Evidence score: 27. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 27). Model Medium (p 0.572). Wealdstone scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Southend scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### Braintree v Hampton & Richmond  (National League South, Sat 31 Oct 15:00 UK)  fixture_id 1588427
- Over 2.5: rejected (model score 0.545). Production BTTS: NO (Medium, p 0.561). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.561) with supporting evidence (score 25, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Braintree: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 4/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 3-4; 1-3; 1-2; 0-6; 2-1. Home last 3: 1-3; 1-2; 2-1 (BTTS 3/3).
- Hampton & Richmond: scored in 3/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 1-1; 0-1; 0-2; 3-4; 2-2. Away last 3: 1-4; 0-1; 2-2 (BTTS 2/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.561). Braintree scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Hampton & Richmond scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Maidstone Utd v Slough Town  (National League South, Sat 31 Oct 15:00 UK)  fixture_id 1588433
- Over 2.5: rejected (model score 0.547). Production BTTS: NO (Medium, p 0.554). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.554) with supporting evidence (score 31, both sides BTTS at least 5 of 5); 55% to 59% historically.
- Maidstone Utd: scored in 5/5, 2+ in 2/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-2; 2-1; 2-1; 1-1; 1-3. Home last 3: 1-2; 2-1; 1-3 (BTTS 3/3).
- Slough Town: scored in 5/5, 2+ in 0/5, conceded in 5/5, 2+ against in 4/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-1; 1-5; 1-2; 1-3; 1-3. Away last 3: 1-0; 1-5; 1-3 (BTTS 2/3).
- Evidence score: 31. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 31). Model Medium (p 0.554). Maidstone Utd scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Slough Town scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### Brentford v Nottingham Forest  (Premier League, Sat 31 Oct 15:00 UK)  fixture_id 1557449
- Over 2.5: rejected (model score 0.534). Production BTTS: NO (Medium, p 0.547). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.547) with supporting evidence (score 25, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Brentford: scored in 5/5, 2+ in 3/5, conceded in 4/5, 2+ against in 3/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-2; 3-0; 2-2; 1-2; 1-1. Home last 3: 1-1; 3-0; 1-2 (BTTS 2/3).
- Nottingham Forest: scored in 3/5, 2+ in 1/5, conceded in 5/5, 2+ against in 1/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 2-1; 0-1; 1-3; 0-1; 1-1. Away last 3: 2-1; 1-3; 1-1 (BTTS 3/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.547). Brentford scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Nottingham Forest scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Hull City v Ipswich  (Premier League, Sat 31 Oct 15:00 UK)  fixture_id 1557452
- Over 2.5: rejected (model score 0.513). Production BTTS: NO (Medium, p 0.545). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.545) with supporting evidence (score 26, both sides BTTS at least 4 of 5); 55% to 59% historically.
- Hull City: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 2-2; 1-2; 2-2; 0-1; 1-1. Home last 3: 0-0; 2-2; 1-1 (BTTS 2/3).
- Ipswich: scored in 4/5, 2+ in 3/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 3-2; 0-1; 2-1; 2-3; 1-1. Away last 3: 3-2; 0-1; 2-3 (BTTS 2/3).
- Evidence score: 26. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 26). Model Medium (p 0.545). Hull City scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Ipswich scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Leighton Town v Bromsgrove Sporting  (Southern Premier Central, Sat 31 Oct 15:00 UK)  fixture_id 1596972
- Over 2.5: rejected (model score 0.566). Production BTTS: NO (Medium, p 0.563). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.563) with supporting evidence (score 26, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Leighton Town: scored in 3/5, 2+ in 1/5, conceded in 5/5, 2+ against in 3/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 2-4; 1-2; 0-3; 0-1; 1-1. Home last 3: 2-3; 2-4; 0-3 (BTTS 2/3).
- Bromsgrove Sporting: scored in 5/5, 2+ in 2/5, conceded in 5/5, 2+ against in 1/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-1; 1-1; 2-1; 1-1; 2-2. Away last 3: 1-0; 3-2; 1-1 (BTTS 2/3).
- Evidence score: 26. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 26). Model Medium (p 0.563). Leighton Town scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5; Bromsgrove Sporting scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### Gloucester City v Berkhamsted  (Southern Premier South, Sat 31 Oct 15:00 UK)  fixture_id 1597435
- Over 2.5: Medium (model score 0.609). Production BTTS: NO (Medium, p 0.563). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.563) with supporting evidence (score 25, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Gloucester City: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 1/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 2-5; 1-1; 3-1; 0-1. Home last 3: 1-2; 1-1; 1-1 (BTTS 3/3).
- Berkhamsted: scored in 4/5, 2+ in 1/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-2; 0-2; 3-0; 1-3; 1-1. Away last 3: 0-2; 3-0; 1-3 (BTTS 1/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.563). Gloucester City scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Berkhamsted scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Gosport Borough v Hanwell Town  (Southern Premier South, Sat 31 Oct 15:00 UK)  fixture_id 1597436
- Over 2.5: Medium (model score 0.589). Production BTTS: NO (Medium, p 0.552). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.552) with supporting evidence (score 25, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Gosport Borough: scored in 4/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-3; 2-1; 4-0; 0-3; 3-1. Home last 3: 1-1; 1-3; 4-0 (BTTS 2/3).
- Hanwell Town: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 1/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 2-1; 1-1; 0-2; 6-1. Away last 3: 2-2; 1-1; 2-1 (BTTS 3/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.552). Gosport Borough scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Hanwell Town scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Hanworth Villa v Plymouth Parkway  (Southern Premier South, Sat 31 Oct 15:00 UK)  fixture_id 1597437
- Over 2.5: Medium (model score 0.585). Production BTTS: NO (Medium, p 0.560). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.560) with supporting evidence (score 27, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Hanworth Villa: scored in 5/5, 2+ in 3/5, conceded in 5/5, 2+ against in 2/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 1-3; 4-1; 2-2; 1-1; 2-1. Home last 3: 2-1; 1-3; 1-1 (BTTS 3/3).
- Plymouth Parkway: scored in 4/5, 2+ in 1/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-1; 1-3; 2-1; 0-2; 1-0. Away last 3: 1-1; 1-3; 0-2 (BTTS 2/3).
- Evidence score: 27. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 27). Model Medium (p 0.560). Hanworth Villa scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5; Plymouth Parkway scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Karpaty v Kudrivka  (Ukrainian Premier, Sat 31 Oct 16:00 UK)  fixture_id 1565514
- Over 2.5: rejected (model score 0.496). Production BTTS: NO (Medium, p 0.534). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.534) with supporting evidence (score 25, both sides BTTS at least 2 of 5); 55% to 59% historically.
- Karpaty: scored in 3/5, 2+ in 2/5, conceded in 3/5, 2+ against in 1/5, BTTS 2/5, clean sheets 2/5, failed to score 2/5. Last five: 2-0; 1-1; 0-1; 2-2; 0-0. Home last 3: 1-2; 1-1; 2-2 (BTTS 3/3).
- Kudrivka: scored in 5/5, 2+ in 2/5, conceded in 5/5, 2+ against in 4/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-3; 1-2; 1-2; 4-1; 1-3. Away last 3: 1-2; 1-2; 1-3 (BTTS 3/3).
- Evidence score: 25. Flag: moderate. Review status: needs review.
- Why flagged: Verdict NO from pattern 'One side dominates' while the card shows both sides scoring and conceding regularly (evidence score 25). Model Medium (p 0.534). Karpaty scored in 3 of 5, conceded in 3 of 5, BTTS 2 of 5; Kudrivka scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

## Mild (27)

### Sheffield Utd v Wrexham  (Championship, Fri 30 Oct 20:00 UK)  fixture_id 1563233
- Over 2.5: rejected (model score 0.526). Production BTTS: NO (Medium, p 0.551). Pattern: Low scoring.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.551) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Sheffield Utd: scored in 5/5, 2+ in 2/5, conceded in 3/5, 2+ against in 2/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 1-2; 3-0; 2-3; 1-0; 1-1. Home last 3: 0-1; 3-0; 1-1 (BTTS 1/3).
- Wrexham: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 2-1; 1-1; 1-2; 4-1; 0-2. Away last 3: 0-6; 1-1; 0-2 (BTTS 1/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'Low scoring' with evidence score 23 and model Medium (p 0.551); the NO is unsupported rather than contradicted. Sheffield Utd scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5; Wrexham scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Wolves v Cardiff  (Championship, Sat 31 Oct 15:00 UK)  fixture_id 1563238
- Over 2.5: rejected (model score 0.555). Production BTTS: NO (Medium, p 0.554). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.554) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Wolves: scored in 4/5, 2+ in 1/5, conceded in 4/5, 2+ against in 1/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 0-1; 1-3; 2-1; 1-1; 1-0. Home last 3: 1-3; 1-1; 1-0 (BTTS 2/3).
- Cardiff: scored in 5/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 3-1; 1-2; 5-1; 2-2; 1-0. Away last 3: 0-1; 1-2; 2-2 (BTTS 2/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 24 and model Medium (p 0.554); the NO is unsupported rather than contradicted. Wolves scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Cardiff scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### NK Slaven Belupo v Istra 1961  (Croatian HNL, Fri 30 Oct 17:00 UK)  fixture_id 1548556
- Over 2.5: Medium (model score 0.59). Production BTTS: NO (Medium, p 0.570). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.570) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- NK Slaven Belupo: scored in 4/5, 2+ in 3/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 0-1; 2-2; 4-1; 1-5; 2-1. Home last 3: 2-1; 4-1; 1-5 (BTTS 3/3).
- Istra 1961: scored in 3/5, 2+ in 3/5, conceded in 5/5, 2+ against in 3/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 3-2; 0-1; 3-1; 0-2; 2-2. Away last 3: 0-0; 3-1; 0-2 (BTTS 1/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 24 and model Medium (p 0.570); the NO is unsupported rather than contradicted. NK Slaven Belupo scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Istra 1961 scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Odense v Silkeborg  (Danish Superliga, Sun 01 Nov 13:00 UK)  fixture_id 1549049
- Over 2.5: rejected (model score 0.577). Production BTTS: NO (Medium, p 0.556). Pattern: Low scoring.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.556) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Odense: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 0/5, BTTS 4/5, clean sheets 1/5, failed to score 1/5. Last five: 2-1; 1-1; 0-0; 2-1; 1-1. Home last 3: 0-5; 1-1; 2-1 (BTTS 2/3).
- Silkeborg: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-1; 4-0; 3-3; 0-4; 1-1. Away last 3: 2-2; 4-0; 0-4 (BTTS 1/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'Low scoring' with evidence score 23 and model Medium (p 0.556); the NO is unsupported rather than contradicted. Odense scored in 4 of 5, conceded in 4 of 5, BTTS 4 of 5; Silkeborg scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Viborg v AC Horsens  (Danish Superliga, Sun 01 Nov 13:00 UK)  fixture_id 1549051
- Over 2.5: Medium (model score 0.608). Production BTTS: NO (Medium, p 0.571). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.571) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Viborg: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-1; 4-1; 2-0; 1-2; 1-2. Home last 3: 0-2; 4-1; 1-2 (BTTS 2/3).
- AC Horsens: scored in 3/5, 2+ in 3/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 2/5. Last five: 0-2; 2-2; 3-3; 0-0; 5-1. Away last 3: 5-2; 0-2; 3-3 (BTTS 2/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.571); the NO is unsupported rather than contradicted. Viborg scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; AC Horsens scored in 3 of 5, conceded in 4 of 5, BTTS 3 of 5.

### FC Nordsjaelland v FC Midtjylland  (Danish Superliga, Sun 01 Nov 15:00 UK)  fixture_id 1549048
- Over 2.5: rejected (model score 0.579). Production BTTS: NO (Medium, p 0.564). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.564) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- FC Nordsjaelland: scored in 4/5, 2+ in 2/5, conceded in 3/5, 2+ against in 2/5, BTTS 3/5, clean sheets 2/5, failed to score 1/5. Last five: 2-0; 1-4; 0-0; 3-3; 1-1. Home last 3: 3-1; 2-0; 0-0 (BTTS 1/3).
- FC Midtjylland: scored in 5/5, 2+ in 4/5, conceded in 5/5, 2+ against in 1/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 4-1; 1-1; 2-1; 2-1; 3-2. Away last 3: 2-0; 1-1; 2-1 (BTTS 2/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 24 and model Medium (p 0.564); the NO is unsupported rather than contradicted. FC Nordsjaelland scored in 4 of 5, conceded in 3 of 5, BTTS 3 of 5; FC Midtjylland scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### Brondby v Aarhus  (Danish Superliga, Sun 01 Nov 17:00 UK)  fixture_id 1549046
- Over 2.5: Medium (model score 0.593). Production BTTS: NO (Medium, p 0.564). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.564) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Brondby: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-4; 0-1; 5-2; 1-2; 3-1. Home last 3: 0-3; 0-1; 5-2 (BTTS 1/3).
- Aarhus: scored in 4/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 0-2; 2-2; 3-0; 1-1; 2-1. Away last 3: 0-2; 2-2; 1-1 (BTTS 2/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.564); the NO is unsupported rather than contradicted. Brondby scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Aarhus scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### GKS Katowice v Widzew Łódź  (Ekstraklasa, Sat 31 Oct 19:15 UK)  fixture_id 1553210
- Over 2.5: rejected (model score 0.57). Production BTTS: NO (Medium, p 0.559). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.559) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- GKS Katowice: scored in 3/5, 2+ in 3/5, conceded in 5/5, 2+ against in 1/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 3-2; 4-1; 2-1; 0-1; 0-1. Home last 3: 3-2; 2-1; 0-1 (BTTS 2/3).
- Widzew Łódź: scored in 4/5, 2+ in 1/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 1/5. Last five: 1-1; 2-2; 1-2; 0-0; 1-1. Away last 3: 3-3; 1-1; 1-2 (BTTS 3/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 24 and model Medium (p 0.559); the NO is unsupported rather than contradicted. GKS Katowice scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5; Widzew Łódź scored in 4 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Villarreal v Espanyol  (La Liga, Fri 30 Oct 20:00 UK)  fixture_id 1570442
- Over 2.5: rejected (model score 0.553). Production BTTS: NO (Medium, p 0.549). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.549) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Villarreal: scored in 3/5, 2+ in 3/5, conceded in 4/5, 2+ against in 0/5, BTTS 3/5, clean sheets 1/5, failed to score 2/5. Last five: 3-1; 3-1; 0-1; 0-0; 2-1. Home last 3: 1-2; 3-1; 0-0 (BTTS 2/3).
- Espanyol: scored in 4/5, 2+ in 0/5, conceded in 5/5, 2+ against in 3/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-2; 1-3; 1-1; 0-1; 1-2. Away last 3: 1-2; 1-1; 1-2 (BTTS 3/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 24 and model Medium (p 0.549); the NO is unsupported rather than contradicted. Villarreal scored in 3 of 5, conceded in 4 of 5, BTTS 3 of 5; Espanyol scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Real Betis v Malaga  (La Liga, Sat 31 Oct 17:30 UK)  fixture_id 1570435
- Over 2.5: rejected (model score 0.571). Production BTTS: NO (Medium, p 0.565). Pattern: Low scoring.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.565) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Real Betis: scored in 4/5, 2+ in 2/5, conceded in 3/5, 2+ against in 2/5, BTTS 3/5, clean sheets 2/5, failed to score 1/5. Last five: 1-0; 1-1; 5-2; 2-5; 0-0. Home last 3: 1-0; 5-2; 2-5 (BTTS 2/3).
- Malaga: scored in 4/5, 2+ in 1/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-3; 0-1; 1-1; 2-5; 1-1. Away last 3: 1-1; 0-1; 1-1 (BTTS 2/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'Low scoring' with evidence score 23 and model Medium (p 0.565); the NO is unsupported rather than contradicted. Real Betis scored in 4 of 5, conceded in 3 of 5, BTTS 3 of 5; Malaga scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Barcelona v Alaves  (La Liga, Sat 31 Oct 20:00 UK)  fixture_id 1570434
- Over 2.5: Medium (model score 0.619). Production BTTS: NO (Medium, p 0.560). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.560) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Barcelona: scored in 5/5, 2+ in 4/5, conceded in 4/5, 2+ against in 3/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 7-2; 3-1; 3-0; 5-2; 1-2. Home last 3: 7-2; 3-0; 1-2 (BTTS 2/3).
- Alaves: scored in 3/5, 2+ in 0/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 2/5. Last five: 0-1; 0-0; 1-2; 1-2; 1-1. Away last 3: 1-2; 0-0; 1-2 (BTTS 2/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.560); the NO is unsupported rather than contradicted. Barcelona scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Alaves scored in 3 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Wycombe v Burton Albion  (League One, Sat 31 Oct 15:00 UK)  fixture_id 1564402
- Over 2.5: rejected (model score 0.567). Production BTTS: NO (Medium, p 0.561). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.561) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Wycombe: scored in 5/5, 2+ in 3/5, conceded in 4/5, 2+ against in 3/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-2; 1-4; 2-0; 2-2; 1-1. Home last 3: 2-2; 1-4; 2-0 (BTTS 2/3).
- Burton Albion: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 2/5. Last five: 1-3; 0-1; 2-2; 0-0; 2-1. Away last 3: 1-0; 0-1; 2-2 (BTTS 1/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.561); the NO is unsupported rather than contradicted. Wycombe scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Burton Albion scored in 3 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Grimsby v York  (League Two, Sat 31 Oct 12:30 UK)  fixture_id 1563843
- Over 2.5: rejected (model score 0.513). Production BTTS: NO (Medium, p 0.517). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.517) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Grimsby: scored in 3/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 1-2; 0-1; 0-2; 2-2; 4-1. Home last 3: 2-0; 1-2; 0-2 (BTTS 1/3).
- York: scored in 5/5, 2+ in 1/5, conceded in 4/5, 2+ against in 1/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-1; 1-1; 1-1; 2-0; 1-3. Away last 3: 0-2; 1-1; 1-3 (BTTS 2/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 24 and model Medium (p 0.517); the NO is unsupported rather than contradicted. Grimsby scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5; York scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Oldham v Crawley Town  (League Two, Sat 31 Oct 15:00 UK)  fixture_id 1563845
- Over 2.5: rejected (model score 0.514). Production BTTS: NO (Medium, p 0.517). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.517) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Oldham: scored in 3/5, 2+ in 1/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 2/5. Last five: 1-4; 0-0; 4-1; 0-3; 1-1. Home last 3: 1-4; 0-0; 4-1 (BTTS 2/3).
- Crawley Town: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 4/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 0-2; 2-2; 1-2; 2-3; 1-1. Away last 3: 2-3; 0-2; 1-2 (BTTS 2/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.517); the NO is unsupported rather than contradicted. Oldham scored in 3 of 5, conceded in 4 of 5, BTTS 3 of 5; Crawley Town scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Shrewsbury v Gillingham  (League Two, Sat 31 Oct 15:00 UK)  fixture_id 1563848
- Over 2.5: rejected (model score 0.544). Production BTTS: NO (Medium, p 0.519). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.519) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Shrewsbury: scored in 4/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 2-1; 0-1; 1-0; 3-2; 3-3. Home last 3: 2-2; 0-1; 1-0 (BTTS 1/3).
- Gillingham: scored in 4/5, 2+ in 1/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 1/5. Last five: 0-0; 4-1; 1-3; 1-1; 1-4. Away last 3: 0-3; 4-1; 1-3 (BTTS 2/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.519); the NO is unsupported rather than contradicted. Shrewsbury scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5; Gillingham scored in 4 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Paris FC v Monaco  (Ligue 1, Sun 01 Nov 16:15 UK)  fixture_id 1552807
- Over 2.5: rejected (model score 0.543). Production BTTS: NO (Medium, p 0.559). Pattern: Low scoring.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.559) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Paris FC: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 2/5. Last five: 0-0; 2-1; 0-1; 4-3; 1-2. Home last 3: 0-0; 2-1; 4-3 (BTTS 2/3).
- Monaco: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 1/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 2-1; 2-2; 0-1; 1-1. Away last 3: 2-1; 1-1; 0-1 (BTTS 2/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'Low scoring' with evidence score 23 and model Medium (p 0.559); the NO is unsupported rather than contradicted. Paris FC scored in 3 of 5, conceded in 4 of 5, BTTS 3 of 5; Monaco scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Boreham Wood v Hartlepool  (National League, Sat 31 Oct 15:00 UK)  fixture_id 1585323
- Over 2.5: High (model score 0.636). Production BTTS: NO (Medium, p 0.561). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.561) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Boreham Wood: scored in 5/5, 2+ in 5/5, conceded in 3/5, 2+ against in 0/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 3-1; 3-1; 2-0; 4-0; 2-1. Home last 3: 3-1; 3-1; 4-0 (BTTS 2/3).
- Hartlepool: scored in 3/5, 2+ in 2/5, conceded in 5/5, 2+ against in 2/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 0-1; 0-1; 4-2; 2-1; 1-3. Away last 3: 1-4; 4-2; 1-3 (BTTS 3/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.561); the NO is unsupported rather than contradicted. Boreham Wood scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5; Hartlepool scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Boston United v Scunthorpe  (National League, Sat 31 Oct 17:30 UK)  fixture_id 1585328
- Over 2.5: Medium (model score 0.613). Production BTTS: NO (Medium, p 0.569). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.569) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Boston United: scored in 4/5, 2+ in 2/5, conceded in 5/5, 2+ against in 3/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 0-6; 1-2; 2-4; 2-1. Home last 3: 0-1; 1-2; 2-1 (BTTS 2/3).
- Scunthorpe: scored in 3/5, 2+ in 2/5, conceded in 5/5, 2+ against in 4/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 4-1; 0-3; 0-2; 2-3; 1-4. Away last 3: 0-3; 0-2; 1-4 (BTTS 1/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.569); the NO is unsupported rather than contradicted. Boston United scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Scunthorpe scored in 3 of 5, conceded in 5 of 5, BTTS 3 of 5.

### Buxton v Marine  (National League North, Sat 31 Oct 15:00 UK)  fixture_id 1587874
- Over 2.5: rejected (model score 0.55). Production BTTS: NO (Medium, p 0.548). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.548) with supporting evidence (score 23, both sides BTTS at least 2 of 5); 55% to 59% historically.
- Buxton: scored in 3/5, 2+ in 3/5, conceded in 4/5, 2+ against in 3/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 0-4; 0-1; 2-2; 3-2; 3-0. Home last 3: 3-1; 2-2; 3-0 (BTTS 2/3).
- Marine: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 1/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-1; 2-1; 1-0; 1-1; 1-2. Away last 3: 1-2; 2-1; 1-2 (BTTS 3/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.548); the NO is unsupported rather than contradicted. Buxton scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5; Marine scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Farnborough v Horsham  (National League South, Sat 31 Oct 15:00 UK)  fixture_id 1588431
- Over 2.5: rejected (model score 0.527). Production BTTS: NO (Medium, p 0.539). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.539) with supporting evidence (score 23, both sides BTTS at least 2 of 5); 55% to 59% historically.
- Farnborough: scored in 3/5, 2+ in 3/5, conceded in 4/5, 2+ against in 3/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 2-2; 0-4; 2-0; 0-2; 2-1. Home last 3: 0-1; 2-0; 2-1 (BTTS 1/3).
- Horsham: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 1-2; 2-1; 2-2; 1-0; 1-1. Away last 3: 2-1; 2-2; 1-1 (BTTS 3/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.539); the NO is unsupported rather than contradicted. Farnborough scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5; Horsham scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### FC Porto v Estoril  (Primeira Liga, Sat 31 Oct 20:30 UK)  fixture_id 1575532
- Over 2.5: rejected (model score 0.565). Production BTTS: NO (Medium, p 0.545). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.545) with supporting evidence (score 23, both sides BTTS at least 3 of 5); 55% to 59% historically.
- FC Porto: scored in 5/5, 2+ in 4/5, conceded in 4/5, 2+ against in 0/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-1; 4-1; 3-1; 2-1; 1-0. Home last 3: 2-0; 2-1; 3-1 (BTTS 2/3).
- Estoril: scored in 3/5, 2+ in 0/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 2/5. Last five: 0-0; 0-1; 1-2; 1-2; 1-3. Away last 3: 1-2; 0-1; 1-2 (BTTS 2/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.545); the NO is unsupported rather than contradicted. FC Porto scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Estoril scored in 3 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Heart Of Midlothian v Hibernian  (Scottish League Cup, Sun 01 Nov 15:00 UK)  fixture_id 1639571
- Over 2.5: Medium (model score 0.601). Production BTTS: NO (Medium, p 0.551). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.551) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Heart Of Midlothian: scored in 5/5, 2+ in 3/5, conceded in 3/5, 2+ against in 2/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 1-1; 5-0; 1-7; 2-0; 2-2. Home last 3: 2-1; 5-0; 2-2 (BTTS 2/3).
- Hibernian: scored in 4/5, 2+ in 0/5, conceded in 5/5, 2+ against in 2/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 0-1; 1-2; 1-2; 1-1. Away last 3: 1-2; 0-1; 1-1 (BTTS 2/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 24 and model Medium (p 0.551); the NO is unsupported rather than contradicted. Heart Of Midlothian scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5; Hibernian scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5.

### Hamilton Academical v Montrose  (Scottish League One, Sat 31 Oct 15:00 UK)  fixture_id 1557069
- Over 2.5: Medium (model score 0.583). Production BTTS: NO (Medium, p 0.560). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.560) with supporting evidence (score 23, both sides BTTS at least 2 of 5); 55% to 59% historically.
- Hamilton Academical: scored in 5/5, 2+ in 4/5, conceded in 4/5, 2+ against in 0/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-1; 3-0; 2-1; 2-1; 1-1. Home last 3: 4-1; 2-1; 2-1 (BTTS 3/3).
- Montrose: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 1/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 2-1; 0-1; 0-5; 1-1; 3-0. Away last 3: 2-1; 0-1; 1-1 (BTTS 2/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.560); the NO is unsupported rather than contradicted. Hamilton Academical scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Montrose scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5.

### Kilmarnock v ST Johnstone  (Scottish Premiership, Sat 31 Oct 15:00 UK)  fixture_id 1556697
- Over 2.5: rejected (model score 0.535). Production BTTS: NO (Medium, p 0.561). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.561) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Kilmarnock: scored in 4/5, 2+ in 1/5, conceded in 5/5, 2+ against in 4/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 1-1; 1-3; 3-2; 0-3; 1-3. Home last 3: 0-1; 1-1; 3-2 (BTTS 2/3).
- ST Johnstone: scored in 4/5, 2+ in 1/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-1; 1-0; 1-1; 0-4; 2-2. Away last 3: 1-1; 1-0; 0-4 (BTTS 1/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 24 and model Medium (p 0.561); the NO is unsupported rather than contradicted. Kilmarnock scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; ST Johnstone scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

### Stourbridge v Kettering Town  (Southern Premier Central, Sat 31 Oct 15:00 UK)  fixture_id 1596977
- Over 2.5: Medium (model score 0.582). Production BTTS: NO (Medium, p 0.558). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.558) with supporting evidence (score 23, both sides BTTS at least 2 of 5); 55% to 59% historically.
- Stourbridge: scored in 3/5, 2+ in 2/5, conceded in 4/5, 2+ against in 1/5, BTTS 2/5, clean sheets 1/5, failed to score 2/5. Last five: 0-1; 2-1; 3-1; 0-2; 1-0. Home last 3: 1-4; 0-1; 2-1 (BTTS 2/3).
- Kettering Town: scored in 5/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 4-1; 1-1; 1-2; 4-0; 3-2. Away last 3: 1-1; 2-3; 1-2 (BTTS 3/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.558); the NO is unsupported rather than contradicted. Stourbridge scored in 3 of 5, conceded in 4 of 5, BTTS 2 of 5; Kettering Town scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Bath City v Poole Town  (Southern Premier South, Sat 31 Oct 15:00 UK)  fixture_id 1597431
- Over 2.5: Medium (model score 0.603). Production BTTS: NO (Medium, p 0.558). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.558) with supporting evidence (score 23, both sides BTTS at least 2 of 5); 55% to 59% historically.
- Bath City: scored in 5/5, 2+ in 3/5, conceded in 2/5, 2+ against in 1/5, BTTS 2/5, clean sheets 3/5, failed to score 0/5. Last five: 2-1; 1-2; 2-0; 2-0; 1-0. Home last 3: 2-1; 1-2; 1-0 (BTTS 2/3).
- Poole Town: scored in 5/5, 2+ in 4/5, conceded in 4/5, 2+ against in 1/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 3-1; 3-1; 1-0; 4-1; 2-2. Away last 3: 3-1; 3-1; 4-1 (BTTS 3/3).
- Evidence score: 23. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 23 and model Medium (p 0.558); the NO is unsupported rather than contradicted. Bath City scored in 5 of 5, conceded in 2 of 5, BTTS 2 of 5; Poole Town scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Sholing v Malvern Town  (Southern Premier South, Sat 31 Oct 15:00 UK)  fixture_id 1597439
- Over 2.5: Medium (model score 0.614). Production BTTS: NO (Medium, p 0.569). Pattern: One side dominates.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.569) with supporting evidence (score 24, both sides BTTS at least 3 of 5); 55% to 59% historically.
- Sholing: scored in 5/5, 2+ in 2/5, conceded in 4/5, 2+ against in 1/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 2-0; 1-1; 2-3; 1-1; 1-1. Home last 3: 1-3; 2-0; 2-3 (BTTS 2/3).
- Malvern Town: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 4/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 1-2; 1-4; 3-2; 2-0; 0-3. Away last 3: 1-2; 1-4; 0-3 (BTTS 2/3).
- Evidence score: 24. Flag: mild. Review status: note.
- Why flagged: Verdict NO from pattern 'One side dominates' with evidence score 24 and model Medium (p 0.569); the NO is unsupported rather than contradicted. Sholing scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Malvern Town scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

## Note (7)

### SK Beveren v Union St. Gilloise  (Belgian Pro League, Sat 31 Oct 19:45 UK)  fixture_id 1558663
- Over 2.5: Medium (model score 0.609). Production BTTS: YES (High, p 0.589). Pattern: Both teams contribute.
- Audit assessment: YES. BTTS model High band (p 0.589 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- SK Beveren: scored in 4/5, 2+ in 3/5, conceded in 3/5, 2+ against in 2/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 3-0; 2-0; 0-1; 1-3; 4-4. Home last 3: 3-0; 2-0; 1-3 (BTTS 1/3).
- Union St. Gilloise: scored in 5/5, 2+ in 4/5, conceded in 3/5, 2+ against in 2/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 3-2; 5-0; 2-0; 1-1; 5-2. Away last 3: 3-0; 3-2; 2-0 (BTTS 1/3).
- Evidence score: 18. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. SK Beveren scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5; Union St. Gilloise scored in 5 of 5, conceded in 3 of 5, BTTS 3 of 5.

### Start v Lillestrom  (Eliteserien, Sun 01 Nov 16:00 UK)  fixture_id 1494794
- Over 2.5: Medium (model score 0.587). Production BTTS: YES (High, p 0.581). Pattern: Both teams contribute.
- Audit assessment: YES. BTTS model High band (p 0.581 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Start: scored in 4/5, 2+ in 2/5, conceded in 3/5, 2+ against in 3/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 2-0; 0-3; 2-4; 1-6; 1-0. Home last 3: 2-0; 2-4; 1-0 (BTTS 1/3).
- Lillestrom: scored in 4/5, 2+ in 4/5, conceded in 3/5, 2+ against in 3/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 2-0; 0-3; 2-2; 2-0; 3-2. Away last 3: 2-1; 0-3; 2-0 (BTTS 1/3).
- Evidence score: 17. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Start scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5; Lillestrom scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5.

### Nice v Rennes  (Ligue 1, Fri 30 Oct 18:00 UK)  fixture_id 1552806
- Over 2.5: rejected (model score 0.562). Production BTTS: YES (Medium, p 0.560). Pattern: Both teams contribute.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.560) with supporting evidence (score 23, both sides BTTS at least 2 of 5); 55% to 59% historically.
- Nice: scored in 4/5, 2+ in 3/5, conceded in 5/5, 2+ against in 1/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 0-1; 2-1; 2-1; 1-2; 2-1. Home last 3: 1-1; 2-1; 2-1 (BTTS 3/3).
- Rennes: scored in 4/5, 2+ in 3/5, conceded in 3/5, 2+ against in 2/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 1-0; 0-4; 4-1; 3-4; 3-0. Away last 3: 2-1; 0-4; 3-4 (BTTS 2/3).
- Evidence score: 23. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Nice scored in 4 of 5, conceded in 5 of 5, BTTS 4 of 5; Rennes scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5.

### Dover v Farnham Town  (National League South, Sat 31 Oct 15:00 UK)  fixture_id 1588430
- Over 2.5: rejected (model score 0.531). Production BTTS: YES (Medium, p 0.545). Pattern: Both teams contribute.
- Audit assessment: LEAN YES. BTTS model Medium band (p 0.545) with supporting evidence (score 23, both sides BTTS at least 2 of 5); 55% to 59% historically.
- Dover: scored in 4/5, 2+ in 1/5, conceded in 3/5, 2+ against in 0/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 1-0; 2-0; 1-1; 1-1; 0-1. Home last 3: 2-0; 1-1; 0-1 (BTTS 1/3).
- Farnham Town: scored in 5/5, 2+ in 4/5, conceded in 4/5, 2+ against in 4/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 3-2; 2-2; 1-2; 6-0; 4-2. Away last 3: 1-1; 2-1; 4-2 (BTTS 3/3).
- Evidence score: 23. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Dover scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5; Farnham Town scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5.

### Curzon Ashton v Leek Town  (Northern Premier League, Sat 31 Oct 15:00 UK)  fixture_id 1596522
- Over 2.5: High (model score 0.647). Production BTTS: YES (High, p 0.587). Pattern: Both teams contribute.
- Audit assessment: YES. BTTS model High band (p 0.587 at or above 0.575); validated 61% on 2025-26, 67% out of sample 2026-27.
- Curzon Ashton: scored in 4/5, 2+ in 3/5, conceded in 3/5, 2+ against in 1/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 3-1; 2-0; 1-5; 0-1; 3-0. Home last 3: 2-0; 3-1; 2-0 (BTTS 1/3).
- Leek Town: scored in 5/5, 2+ in 5/5, conceded in 5/5, 2+ against in 3/5, BTTS 5/5, clean sheets 0/5, failed to score 0/5. Last five: 2-1; 3-3; 2-2; 2-1; 3-5. Away last 3: 2-3; 2-1; 3-5 (BTTS 3/3).
- Evidence score: 24. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Curzon Ashton scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5; Leek Town scored in 5 of 5, conceded in 5 of 5, BTTS 5 of 5.

### Redcar Athletic v Guiseley AFC  (Northern Premier League, Sat 31 Oct 15:00 UK)  fixture_id 1596526
- Over 2.5: Medium (model score 0.637). Production BTTS: YES (Medium, p 0.570). Pattern: Both teams contribute.
- Audit assessment: NO LEAN. BTTS model Medium band (p 0.570) without strong card evidence (score 22); 55% historically, no lean either way.
- Redcar Athletic: scored in 5/5, 2+ in 4/5, conceded in 4/5, 2+ against in 1/5, BTTS 4/5, clean sheets 1/5, failed to score 0/5. Last five: 3-1; 1-3; 5-0; 3-1; 2-1. Home last 3: 3-2; 3-1; 3-1 (BTTS 3/3).
- Guiseley AFC: scored in 4/5, 2+ in 3/5, conceded in 3/5, 2+ against in 0/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 4-1; 0-1; 2-0; 1-0; 2-1. Away last 3: 0-1; 2-0; 1-0 (BTTS 0/3).
- Evidence score: 22. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Redcar Athletic scored in 5 of 5, conceded in 4 of 5, BTTS 4 of 5; Guiseley AFC scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5.

### Bury Town v Banbury United  (Southern Premier Central, Sat 31 Oct 15:00 UK)  fixture_id 1596970
- Over 2.5: rejected (model score 0.579). Production BTTS: YES (Medium, p 0.567). Pattern: Both teams contribute.
- Audit assessment: NO LEAN. BTTS model Medium band (p 0.567) without strong card evidence (score 19); 55% historically, no lean either way.
- Bury Town: scored in 4/5, 2+ in 2/5, conceded in 3/5, 2+ against in 3/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 1-0; 0-5; 2-0; 2-2; 1-5. Home last 3: 1-0; 0-5; 2-0 (BTTS 0/3).
- Banbury United: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 3-2; 2-4; 1-1; 1-0; 0-3. Away last 3: 0-0; 2-4; 1-1 (BTTS 2/3).
- Evidence score: 19. Flag: note. Review status: note.
- Why flagged: Verdict YES with one side having BTTS in only 2 of 5; historically this group still went BTTS 64% of the time, so informational only. Bury Town scored in 4 of 5, conceded in 3 of 5, BTTS 2 of 5; Banbury United scored in 4 of 5, conceded in 4 of 5, BTTS 3 of 5.

## Data (8)

### Rayo Vallecano v Celta Vigo  (La Liga, Sat 31 Oct 15:15 UK)  fixture_id 1570441
- Over 2.5: rejected (model score 0.537). Production BTTS: NO (Medium, p 0.560). Pattern: Low scoring.
- Audit assessment: NO LEAN. BTTS model Medium band (p 0.560) without strong card evidence (score 15); 55% historically, no lean either way.
- Rayo Vallecano: scored in 3/5, 2+ in 1/5, conceded in 4/5, 2+ against in 1/5, BTTS 3/5, clean sheets 1/5, failed to score 2/5. Last five: 2-1; 1-1; 0-0; 1-1; 0-3. Home last 3: 2-1; 0-0; 0-3 (BTTS 1/3).
- Celta Vigo: scored in 3/5, 2+ in 2/5, conceded in 2/5, 2+ against in 0/5, BTTS 2/5, clean sheets 3/5, failed to score 2/5. Last five: 1-1; 5-0; 0-0; 2-1; 0-0. Away last 3: 0-0; 1-1; 0-0 (BTTS 1/3).
- Evidence score: 15. Flag: data. Review status: data check.
- Why flagged: Data: home window includes ABD match of 10 Oct (0-0).

### Athletic Club v Real Sociedad  (La Liga, Sun 01 Nov 20:00 UK)  fixture_id 1570433
- Over 2.5: rejected (model score 0.566). Production BTTS: NO (Medium, p 0.547). Pattern: One side dominates.
- Audit assessment: NO LEAN. BTTS model Medium band (p 0.547) without strong card evidence (score 17); 55% historically, no lean either way.
- Athletic Club: scored in 2/5, 2+ in 1/5, conceded in 1/5, 2+ against in 1/5, BTTS 1/5, clean sheets 4/5, failed to score 3/5. Last five: 0-0; 0-0; 0-0; 1-3; 4-0. Home last 3: 1-1; 0-0; 4-0 (BTTS 1/3).
- Real Sociedad: scored in 4/5, 2+ in 4/5, conceded in 5/5, 2+ against in 4/5, BTTS 4/5, clean sheets 0/5, failed to score 1/5. Last five: 0-3; 3-2; 3-2; 5-2; 2-1. Away last 3: 3-2; 3-2; 5-2 (BTTS 3/3).
- Evidence score: 17. Flag: data. Review status: data check.
- Why flagged: Data: home window includes ABD match of 10 Oct (0-0).

### Forest Green v Harrogate Town  (National League, Sat 31 Oct 12:30 UK)  fixture_id 1585319
- Over 2.5: rejected (model score 0.58). Production BTTS: NO (Medium, p 0.559). Pattern: One side dominates.
- Audit assessment: NO LEAN. BTTS model Medium band (p 0.559) without strong card evidence (score 17); 55% historically, no lean either way.
- Forest Green: scored in 4/5, 2+ in 3/5, conceded in 4/5, 2+ against in 2/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 3-3; 1-1; 2-4; 0-1; 2-0. Home last 3: 1-1; 2-4; 2-0 (BTTS 2/3).
- Harrogate Town: scored in 4/5, 2+ in 2/5, conceded in 2/5, 2+ against in 1/5, BTTS 1/5, clean sheets 3/5, failed to score 1/5. Last five: 1-0; 3-0; 1-0; 3-1; 0-3. Away last 3: 1-0; 1-0; 0-3 (BTTS 0/3).
- Evidence score: 17. Flag: data. Review status: data check.
- Why flagged: Data: home window includes ABD match of 24 Oct (0-1).

### Barrow v Eastleigh  (National League, Sat 31 Oct 15:00 UK)  fixture_id 1585322
- Over 2.5: Medium (model score 0.62). Production BTTS: NO (Medium, p 0.569). Pattern: One side dominates.
- Audit assessment: NO LEAN. BTTS model Medium band (p 0.569) without strong card evidence (score 20); 55% historically, no lean either way.
- Barrow: scored in 5/5, 2+ in 4/5, conceded in 3/5, 2+ against in 1/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 3-0; 2-1; 2-1; 1-0; 3-2. Home last 3: 3-0; 2-1; 1-0 (BTTS 1/3).
- Eastleigh: scored in 3/5, 2+ in 1/5, conceded in 5/5, 2+ against in 4/5, BTTS 3/5, clean sheets 0/5, failed to score 2/5. Last five: 1-1; 1-3; 0-2; 4-2; 0-2. Away last 3: 1-4; 0-2; 0-2 (BTTS 1/3).
- Evidence score: 20. Flag: data. Review status: data check.
- Why flagged: Data: home window includes ABD match of 24 Oct (1-0).

### Airdrie United v Cove Rangers  (Scottish League One, Sat 31 Oct 15:00 UK)  fixture_id 1557066
- Over 2.5: rejected (model score 0.511). Production BTTS: NO (Medium, p 0.550). Pattern: One side dominates.
- Audit assessment: NO LEAN. BTTS model Medium band (p 0.550) without strong card evidence (score 19); 55% historically, no lean either way.
- Airdrie United: scored in 4/5, 2+ in 2/5, conceded in 4/5, 2+ against in 3/5, BTTS 3/5, clean sheets 1/5, failed to score 1/5. Last five: 2-1; 1-0; 2-2; 1-2; 0-4. Home last 3: 1-0; 1-0; 1-2 (BTTS 1/3).
- Cove Rangers: scored in 2/5, 2+ in 1/5, conceded in 5/5, 2+ against in 3/5, BTTS 2/5, clean sheets 0/5, failed to score 3/5. Last five: 0-2; 3-4; 1-1; 0-2; 0-1. Away last 3: 1-2; 3-4; 0-2 (BTTS 2/3).
- Evidence score: 19. Flag: data. Review status: data check.
- Why flagged: Data: away window includes ABD match of 24 Oct (0-1).

### East Kilbride v Ross County  (Scottish League One, Sat 31 Oct 15:00 UK)  fixture_id 1557068
- Over 2.5: Medium (model score 0.612). Production BTTS: YES (Medium, p 0.554). Pattern: Both teams contribute.
- Audit assessment: NO LEAN. BTTS model Medium band (p 0.554) without strong card evidence (score 22); 55% historically, no lean either way.
- East Kilbride: scored in 5/5, 2+ in 3/5, conceded in 3/5, 2+ against in 1/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 2-1; 3-0; 2-2; 1-1; 1-0. Home last 3: 3-1; 2-2; 1-1 (BTTS 3/3).
- Ross County: scored in 5/5, 2+ in 4/5, conceded in 3/5, 2+ against in 0/5, BTTS 3/5, clean sheets 2/5, failed to score 0/5. Last five: 4-1; 5-0; 7-1; 4-0; 1-1. Away last 3: 2-0; 5-0; 7-1 (BTTS 1/3).
- Evidence score: 22. Flag: data. Review status: data check.
- Why flagged: Data: home window includes ABD match of 24 Oct (1-0).

### Obolon'-Brovar v Shakhtar Donetsk  (Ukrainian Premier, Fri 30 Oct 16:00 UK)  fixture_id 1565519
- Over 2.5: rejected (model score 0.469). Production BTTS: NO (Low, p 0.513). Pattern: One side dominates.
- Audit assessment: NO LEAN. BTTS model Low band (p 0.513 below 0.514); 50% on 2025-26 but 56% out of sample, so no NO call is supportable.
- Obolon'-Brovar: scored in 4/5, 2+ in 1/5, conceded in 3/5, 2+ against in 2/5, BTTS 2/5, clean sheets 2/5, failed to score 1/5. Last five: 1-3; 1-1; 1-0; 2-0; 0-3. Home last 2: 1-0; 2-0 (BTTS 0/2).
- Shakhtar Donetsk: scored in 4/5, 2+ in 4/5, conceded in 1/5, 2+ against in 0/5, BTTS 1/5, clean sheets 4/5, failed to score 1/5. Last five: 2-0; 3-0; 3-0; 2-1; 0-0. Away last 3: 1-0; 2-1; 3-0 (BTTS 1/3).
- Evidence score: 14. Flag: data. Review status: data check.
- Why flagged: Data: home window includes ABD match of 10 Oct (1-0).

### Kryvbas KR v Dynamo Kyiv  (Ukrainian Premier, Sat 31 Oct 16:00 UK)  fixture_id 1565516
- Over 2.5: rejected (model score 0.484). Production BTTS: NO (Medium, p 0.534). Pattern: One side dominates.
- Audit assessment: NO LEAN. BTTS model Medium band (p 0.534) without strong card evidence (score 15); 55% historically, no lean either way.
- Kryvbas KR: scored in 1/5, 2+ in 1/5, conceded in 4/5, 2+ against in 2/5, BTTS 1/5, clean sheets 1/5, failed to score 4/5. Last five: 2-2; 0-1; 0-1; 0-3; 0-0. Home last 3: 1-1; 2-2; 0-3 (BTTS 2/3).
- Dynamo Kyiv: scored in 5/5, 2+ in 3/5, conceded in 2/5, 2+ against in 1/5, BTTS 2/5, clean sheets 3/5, failed to score 0/5. Last five: 3-0; 2-0; 1-0; 1-3; 3-1. Away last 3: 0-3; 2-0; 1-3 (BTTS 1/3).
- Evidence score: 15. Flag: data. Review status: data check.
- Why flagged: Data: home window includes ABD match of 10 Oct (0-1).

## All fixtures

| fixture_id | kickoff UK | competition | fixture | Over 2.5 | BTTS (prod) | p | audit | evidence | flag | status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1494321 | Sun 01 Nov 13:00 | Allsvenskan | Djurgardens IF v Degerfors IF | rejected | NO (Medium) | 0.550 | NO LEAN | 19 | - | ok |
| 1494325 | Sun 01 Nov 13:00 | Allsvenskan | Malmo FF v Hammarby FF | rejected | NO (Medium) | 0.535 | NO LEAN | 10 | - | ok |
| 1494324 | Sun 01 Nov 15:30 | Allsvenskan | BK Hacken v IFK Goteborg | rejected | NO (Medium) | 0.535 | NO LEAN | 14 | - | ok |
| 1494322 | Sun 01 Nov 15:30 | Allsvenskan | IF Elfsborg v Orgryte IS | Medium | NO (Medium) | 0.558 | NO LEAN | 22 | - | ok |
| 1494328 | Sun 01 Nov 15:30 | Allsvenskan | Vasteras SK FK v IF Brommapojkarna | rejected | NO (Medium) | 0.547 | NO LEAN | 12 | - | ok |
| 1561956 | Fri 30 Oct 18:30 | Austrian Bundesliga | Grazer AK v TSV Hartberg | Medium | YES (Medium) | 0.568 | LEAN YES | 25 | - | ok |
| 1561954 | Sat 31 Oct 16:00 | Austrian Bundesliga | SCR Altach v Ried | Medium | NO (Medium) | 0.568 | LEAN YES | 25 | moderate | needs review |
| 1561957 | Sat 31 Oct 18:30 | Austrian Bundesliga | Lask Linz v WSG Wattens | Medium | YES (High) | 0.583 | YES | 21 | - | ok |
| 1561958 | Sun 01 Nov 13:30 | Austrian Bundesliga | Red Bull Salzburg v Austria Lustenau | Medium | NO (Medium) | 0.555 | NO LEAN | 19 | - | ok |
| 1561959 | Sun 01 Nov 13:30 | Austrian Bundesliga | Wolfsberger AC v Sturm Graz | Medium | NO (Medium) | 0.574 | NO LEAN | 17 | - | ok |
| 1561955 | Sun 01 Nov 16:00 | Austrian Bundesliga | Austria Vienna v Rapid Vienna | Medium | NO (Medium) | 0.569 | NO LEAN | 20 | - | ok |
| 1558670 | Fri 30 Oct 19:45 | Belgian Pro League | Zulte Waregem v Club Brugge KV | rejected | NO (Medium) | 0.565 | NO LEAN | 15 | - | ok |
| 1558666 | Sat 31 Oct 15:00 | Belgian Pro League | KV Mechelen v Genk | Medium | NO (Medium) | 0.570 | NO LEAN | 14 | - | ok |
| 1558668 | Sat 31 Oct 17:15 | Belgian Pro League | Standard Liege v Kortrijk | rejected | NO (Medium) | 0.534 | NO LEAN | 14 | - | ok |
| 1558662 | Sat 31 Oct 19:45 | Belgian Pro League | Anderlecht v KVC Westerlo | Medium | NO (Medium) | 0.541 | NO LEAN | 15 | - | ok |
| 1558663 | Sat 31 Oct 19:45 | Belgian Pro League | SK Beveren v Union St. Gilloise | Medium | YES (High) | 0.589 | YES | 18 | note | note |
| 1558664 | Sun 01 Nov 12:30 | Belgian Pro League | Cercle Brugge v Antwerp | Medium | NO (High) | 0.582 | YES | 21 | severe | needs review |
| 1558669 | Sun 01 Nov 15:00 | Belgian Pro League | St. Truiden v OH Leuven | rejected | NO (High) | 0.575 | YES | 18 | severe | needs review |
| 1558667 | Sun 01 Nov 17:30 | Belgian Pro League | Lommel United v Gent | rejected | NO (Medium) | 0.560 | NO LEAN | 15 | - | ok |
| 1558665 | Sun 01 Nov 18:15 | Belgian Pro League | Charleroi v RAAL La Louvière | Medium | NO (High) | 0.582 | YES | 15 | severe | needs review |
| 1575211 | Fri 30 Oct 19:30 | Bundesliga | SV Elversberg v FSV Mainz 05 | High | NO (High) | 0.591 | YES | 21 | severe | needs review |
| 1575204 | Sat 31 Oct 14:30 | Bundesliga | Bayer Leverkusen v VfB Stuttgart | High | NO (High) | 0.578 | YES | 19 | severe | needs review |
| 1575208 | Sat 31 Oct 14:30 | Bundesliga | Borussia Monchengladbach v SC Paderborn 07 | High | NO (High) | 0.606 | YES | 22 | severe | needs review |
| 1575206 | Sat 31 Oct 14:30 | Bundesliga | FC Augsburg v SC Freiburg | High | YES (High) | 0.588 | YES | 29 | - | ok |
| 1575210 | Sat 31 Oct 14:30 | Bundesliga | FC Schalke 04 v RB Leipzig | Medium | NO (Medium) | 0.566 | NO LEAN | 13 | - | ok |
| 1575209 | Sat 31 Oct 14:30 | Bundesliga | Werder Bremen v 1899 Hoffenheim | High | YES (High) | 0.588 | YES | 30 | - | ok |
| 1575203 | Sat 31 Oct 17:30 | Bundesliga | Bayern Munich v Borussia Dortmund | Medium | NO (High) | 0.576 | YES | 18 | severe | needs review |
| 1575207 | Sun 01 Nov 14:30 | Bundesliga | Union Berlin v 1. FC Köln | Medium | NO (Medium) | 0.550 | NO LEAN | 17 | - | ok |
| 1575205 | Sun 01 Nov 16:30 | Bundesliga | Eintracht Frankfurt v Hamburger SV | Medium | NO (High) | 0.584 | YES | 17 | severe | needs review |
| 1563233 | Fri 30 Oct 20:00 | Championship | Sheffield Utd v Wrexham | rejected | NO (Medium) | 0.551 | LEAN YES | 23 | mild | note |
| 1563229 | Sat 31 Oct 12:30 | Championship | Lincoln v Birmingham | rejected | NO (Medium) | 0.566 | NO LEAN | 18 | - | ok |
| 1563232 | Sat 31 Oct 12:30 | Championship | Norwich v Watford | rejected | NO (Medium) | 0.564 | NO LEAN | 16 | - | ok |
| 1563235 | Sat 31 Oct 12:30 | Championship | Stoke City v Preston | rejected | NO (Medium) | 0.565 | NO LEAN | 21 | - | ok |
| 1563227 | Sat 31 Oct 15:00 | Championship | Bolton v Bristol City | rejected | NO (Medium) | 0.559 | NO LEAN | 18 | - | ok |
| 1563228 | Sat 31 Oct 15:00 | Championship | Burnley v Portsmouth | rejected | NO (Medium) | 0.559 | LEAN YES | 25 | moderate | needs review |
| 1563230 | Sat 31 Oct 15:00 | Championship | Middlesbrough v Charlton | Medium | YES (Medium) | 0.566 | LEAN YES | 26 | - | ok |
| 1563231 | Sat 31 Oct 15:00 | Championship | Millwall v Derby | rejected | NO (Medium) | 0.547 | LEAN YES | 25 | moderate | needs review |
| 1563234 | Sat 31 Oct 15:00 | Championship | Southampton v QPR | rejected | NO (Medium) | 0.558 | NO LEAN | 18 | - | ok |
| 1563236 | Sat 31 Oct 15:00 | Championship | Swansea v Blackburn | rejected | NO (Medium) | 0.565 | NO LEAN | 20 | - | ok |
| 1563237 | Sat 31 Oct 15:00 | Championship | West Ham v West Brom | Medium | NO (Medium) | 0.549 | NO LEAN | 22 | - | ok |
| 1563238 | Sat 31 Oct 15:00 | Championship | Wolves v Cardiff | rejected | NO (Medium) | 0.554 | LEAN YES | 24 | mild | note |
| 1548556 | Fri 30 Oct 17:00 | Croatian HNL | NK Slaven Belupo v Istra 1961 | Medium | NO (Medium) | 0.570 | LEAN YES | 24 | mild | note |
| 1548552 | Sat 31 Oct 14:00 | Croatian HNL | HNK Hajduk Split v HNK Gorica | rejected | NO (Medium) | 0.530 | NO LEAN | 18 | - | ok |
| 1548555 | Sat 31 Oct 17:00 | Croatian HNL | Rudes v Dinamo Zagreb | Medium | YES (Medium) | 0.571 | LEAN YES | 29 | - | ok |
| 1548554 | Sun 01 Nov 14:00 | Croatian HNL | HNK Rijeka v NK Varazdin | rejected | NO (Medium) | 0.560 | NO LEAN | 21 | - | ok |
| 1548553 | Sun 01 Nov 17:00 | Croatian HNL | NK Lokomotiva Zagreb v NK Osijek | rejected | NO (Medium) | 0.549 | NO LEAN | 17 | - | ok |
| 1560060 | Sat 31 Oct 14:00 | Czech Liga | Artis v Zlin | rejected | NO (Medium) | 0.514 | NO LEAN | 17 | - | ok |
| 1560059 | Sat 31 Oct 14:00 | Czech Liga | FK Jablonec v Slavia Praha | rejected | NO (Medium) | 0.535 | NO LEAN | 18 | - | ok |
| 1560058 | Sat 31 Oct 14:00 | Czech Liga | Pardubice v Slovan Liberec | rejected | NO (Medium) | 0.533 | NO LEAN | 16 | - | ok |
| 1560064 | Sat 31 Oct 14:00 | Czech Liga | Slovácko v Teplice | rejected | NO (Medium) | 0.533 | NO LEAN | 17 | - | ok |
| 1560063 | Sat 31 Oct 17:00 | Czech Liga | Sigma Olomouc v Zbrojovka Brno | rejected | NO (Medium) | 0.537 | NO LEAN | 20 | - | ok |
| 1560061 | Sun 01 Nov 12:00 | Czech Liga | Mlada Boleslav v Hradec Králové | rejected | NO (Medium) | 0.535 | NO LEAN | 15 | - | ok |
| 1560062 | Sun 01 Nov 14:00 | Czech Liga | Baník Ostrava v Plzen | rejected | NO (Medium) | 0.522 | NO LEAN | 20 | - | ok |
| 1560057 | Sun 01 Nov 17:00 | Czech Liga | Bohemians 1905 v Sparta Praha | rejected | NO (Low) | 0.502 | NO LEAN | 13 | - | ok |
| 1549047 | Fri 30 Oct 18:00 | Danish Superliga | Lyngby v Randers FC | Medium | NO (Medium) | 0.566 | NO LEAN | 22 | - | ok |
| 1549049 | Sun 01 Nov 13:00 | Danish Superliga | Odense v Silkeborg | rejected | NO (Medium) | 0.556 | LEAN YES | 23 | mild | note |
| 1549051 | Sun 01 Nov 13:00 | Danish Superliga | Viborg v AC Horsens | Medium | NO (Medium) | 0.571 | LEAN YES | 23 | mild | note |
| 1549048 | Sun 01 Nov 15:00 | Danish Superliga | FC Nordsjaelland v FC Midtjylland | rejected | NO (Medium) | 0.564 | LEAN YES | 24 | mild | note |
| 1549046 | Sun 01 Nov 17:00 | Danish Superliga | Brondby v Aarhus | Medium | NO (Medium) | 0.564 | LEAN YES | 23 | mild | note |
| 1553209 | Fri 30 Oct 17:00 | Ekstraklasa | Cracovia Krakow v Motor Lublin | rejected | YES (Medium) | 0.565 | LEAN YES | 28 | - | ok |
| 1553211 | Fri 30 Oct 19:30 | Ekstraklasa | Gornik Zabrze v Legia Warszawa | rejected | NO (Medium) | 0.544 | LEAN YES | 25 | moderate | needs review |
| 1553216 | Sat 31 Oct 11:15 | Ekstraklasa | Wisla Plock v Piast Gliwice | rejected | NO (Medium) | 0.547 | NO LEAN | 19 | - | ok |
| 1553215 | Sat 31 Oct 13:45 | Ekstraklasa | Wieczysta Kraków v Jagiellonia | rejected | NO (Medium) | 0.558 | NO LEAN | 19 | - | ok |
| 1553212 | Sat 31 Oct 16:30 | Ekstraklasa | Lech Poznan v Wisla Krakow | Medium | NO (Medium) | 0.559 | NO LEAN | 22 | - | ok |
| 1553210 | Sat 31 Oct 19:15 | Ekstraklasa | GKS Katowice v Widzew Łódź | rejected | NO (Medium) | 0.559 | LEAN YES | 24 | mild | note |
| 1494789 | Fri 30 Oct 18:00 | Eliteserien | Bodo/Glimt v Viking | Medium | YES (Medium) | 0.572 | NO LEAN | 22 | - | ok |
| 1494791 | Sat 31 Oct 15:00 | Eliteserien | Fredrikstad v Rosenborg | Medium | NO (High) | 0.581 | YES | 26 | severe | needs review |
| 1494788 | Sat 31 Oct 17:00 | Eliteserien | Aalesund v Sandefjord | Medium | NO (High) | 0.586 | YES | 24 | severe | needs review |
| 1494790 | Sun 01 Nov 13:30 | Eliteserien | Brann v Molde | High | NO (High) | 0.576 | YES | 27 | severe | needs review |
| 1494792 | Sun 01 Nov 16:00 | Eliteserien | KFUM Oslo v Ham-Kam | Medium | NO (High) | 0.575 | YES | 27 | severe | needs review |
| 1494793 | Sun 01 Nov 16:00 | Eliteserien | Sarpsborg 08 FF v Kristiansund BK | Medium | YES (High) | 0.582 | YES | 29 | - | ok |
| 1494794 | Sun 01 Nov 16:00 | Eliteserien | Start v Lillestrom | Medium | YES (High) | 0.581 | YES | 17 | note | note |
| 1494795 | Sun 01 Nov 18:15 | Eliteserien | Valerenga v Tromso | Medium | NO (Medium) | 0.569 | LEAN YES | 28 | moderate | needs review |
| 1552207 | Sat 31 Oct 15:30 | Eredivisie | Feyenoord v Fortuna Sittard | Medium | NO (High) | 0.622 | YES | 19 | severe | needs review |
| 1552208 | Sat 31 Oct 17:45 | Eredivisie | Heerenveen v NEC Nijmegen | Medium | NO (High) | 0.605 | YES | 18 | severe | needs review |
| 1552209 | Sat 31 Oct 17:45 | Eredivisie | PSV Eindhoven v Willem II | High | NO (High) | 0.611 | YES | 27 | severe | needs review |
| 1552210 | Sat 31 Oct 20:00 | Eredivisie | Ajax v AZ Alkmaar | High | NO (High) | 0.576 | YES | 25 | severe | needs review |
| 1552211 | Sat 31 Oct 20:00 | Eredivisie | Cambuur v GO Ahead Eagles | High | NO (High) | 0.613 | YES | 27 | severe | needs review |
| 1552212 | Sun 01 Nov 11:15 | Eredivisie | PEC Zwolle v ADO Den Haag | Medium | NO (High) | 0.610 | YES | 21 | severe | needs review |
| 1552213 | Sun 01 Nov 13:30 | Eredivisie | Excelsior v Twente | Medium | NO (High) | 0.608 | YES | 23 | severe | needs review |
| 1552214 | Sun 01 Nov 13:30 | Eredivisie | Telstar v Utrecht | High | NO (High) | 0.604 | YES | 24 | severe | needs review |
| 1552215 | Sun 01 Nov 15:45 | Eredivisie | Groningen v Sparta Rotterdam | High | NO (High) | 0.612 | YES | 27 | severe | needs review |
| 1593347 | Sat 31 Oct 17:00 | Greek Super League | Kifisia v Olympiakos Piraeus | rejected | NO (Medium) | 0.524 | NO LEAN | 13 | - | ok |
| 1593348 | Sun 01 Nov 15:00 | Greek Super League | Levadiakos v Aris Thessalonikis | rejected | NO (Low) | 0.452 | NO LEAN | 10 | - | ok |
| 1593350 | Sun 01 Nov 16:00 | Greek Super League | Panetolikos v OFI | rejected | NO (Medium) | 0.541 | NO LEAN | 18 | - | ok |
| 1593351 | Sun 01 Nov 17:00 | Greek Super League | PAOK v Asteras Tripolis | rejected | NO (Medium) | 0.551 | LEAN YES | 26 | moderate | needs review |
| 1593349 | Sun 01 Nov 17:30 | Greek Super League | Panathinaikos v AEK Athens FC | rejected | NO (Medium) | 0.561 | NO LEAN | 17 | - | ok |
| 1598832 | Sat 31 Oct 15:00 | Isthmian Premier | Aveley v Dartford | Medium | YES (Medium) | 0.558 | LEAN YES | 24 | - | ok |
| 1598833 | Sat 31 Oct 15:00 | Isthmian Premier | Brentwood Town v Cray Wanderers | High | YES (High) | 0.589 | YES | 27 | - | ok |
| 1598834 | Sat 31 Oct 15:00 | Isthmian Premier | Burgess Hill Town v Enfield Town | Medium | YES (High) | 0.584 | YES | 25 | - | ok |
| 1598835 | Sat 31 Oct 15:00 | Isthmian Premier | Cheshunt v Chatham Town | Medium | NO (High) | 0.588 | YES | 20 | severe | needs review |
| 1598836 | Sat 31 Oct 15:00 | Isthmian Premier | Eastbourne Borough v Ramsgate | Medium | NO (Medium) | 0.572 | NO LEAN | 19 | - | ok |
| 1598837 | Sat 31 Oct 15:00 | Isthmian Premier | Leatherhead v Stanway Rovers | Medium | NO (High) | 0.585 | YES | 19 | severe | needs review |
| 1598838 | Sat 31 Oct 15:00 | Isthmian Premier | Lewes v Wingate & Finchley | Medium | YES (Medium) | 0.573 | LEAN YES | 26 | - | ok |
| 1598839 | Sat 31 Oct 15:00 | Isthmian Premier | Maldon & Tiptree v Three Bridges | Medium | YES (Medium) | 0.571 | LEAN YES | 29 | - | ok |
| 1598840 | Sat 31 Oct 15:00 | Isthmian Premier | Welling United v Carshalton Athletic | High | NO (High) | 0.583 | YES | 20 | severe | needs review |
| 1598841 | Sat 31 Oct 15:00 | Isthmian Premier | Whitehawk v St Albans City | Medium | NO (High) | 0.581 | YES | 23 | severe | needs review |
| 1598842 | Sat 31 Oct 15:00 | Isthmian Premier | Whyteleafe v Dulwich Hamlet | High | NO (High) | 0.583 | YES | 22 | severe | needs review |
| 1570442 | Fri 30 Oct 20:00 | La Liga | Villarreal v Espanyol | rejected | NO (Medium) | 0.549 | LEAN YES | 24 | mild | note |
| 1570439 | Sat 31 Oct 13:00 | La Liga | Levante v Atletico Madrid | Medium | NO (High) | 0.576 | YES | 24 | severe | needs review |
| 1570441 | Sat 31 Oct 15:15 | La Liga | Rayo Vallecano v Celta Vigo | rejected | NO (Medium) | 0.560 | NO LEAN | 15 | data | data check |
| 1570435 | Sat 31 Oct 17:30 | La Liga | Real Betis v Malaga | rejected | NO (Medium) | 0.565 | LEAN YES | 23 | mild | note |
| 1570434 | Sat 31 Oct 20:00 | La Liga | Barcelona v Alaves | Medium | NO (Medium) | 0.560 | LEAN YES | 23 | mild | note |
| 1570438 | Sun 01 Nov 13:00 | La Liga | Getafe v Sevilla | rejected | NO (Medium) | 0.544 | NO LEAN | 18 | - | ok |
| 1570440 | Sun 01 Nov 15:15 | La Liga | Racing Santander v Real Madrid | Medium | NO (Medium) | 0.571 | LEAN YES | 26 | moderate | needs review |
| 1570437 | Sun 01 Nov 17:30 | La Liga | Elche v Valencia | rejected | NO (Medium) | 0.559 | NO LEAN | 17 | - | ok |
| 1570433 | Sun 01 Nov 20:00 | La Liga | Athletic Club v Real Sociedad | rejected | NO (Medium) | 0.547 | NO LEAN | 17 | data | data check |
| 1564392 | Sat 31 Oct 12:30 | League One | Bradford v Huddersfield | rejected | NO (Medium) | 0.535 | NO LEAN | 16 | - | ok |
| 1564394 | Sat 31 Oct 12:30 | League One | Leyton Orient v Cambridge United | rejected | NO (Medium) | 0.538 | NO LEAN | 19 | - | ok |
| 1564398 | Sat 31 Oct 12:30 | League One | Plymouth v Reading | rejected | NO (Medium) | 0.548 | NO LEAN | 19 | - | ok |
| 1564391 | Sat 31 Oct 15:00 | League One | Barnsley v Oxford United | rejected | NO (Medium) | 0.547 | LEAN YES | 26 | moderate | needs review |
| 1564393 | Sat 31 Oct 15:00 | League One | Leicester v Stevenage | rejected | NO (Medium) | 0.546 | NO LEAN | 15 | - | ok |
| 1564395 | Sat 31 Oct 15:00 | League One | Mansfield Town v Notts County | rejected | NO (Medium) | 0.547 | NO LEAN | 21 | - | ok |
| 1564396 | Sat 31 Oct 15:00 | League One | Milton Keynes Dons v Doncaster | rejected | NO (Medium) | 0.559 | NO LEAN | 21 | - | ok |
| 1564397 | Sat 31 Oct 15:00 | League One | Peterborough v Luton | rejected | NO (Medium) | 0.568 | LEAN YES | 29 | moderate | needs review |
| 1564400 | Sat 31 Oct 15:00 | League One | Stockport County v AFC Wimbledon | rejected | NO (Medium) | 0.549 | NO LEAN | 19 | - | ok |
| 1564401 | Sat 31 Oct 15:00 | League One | Wigan v Bromley | rejected | NO (Medium) | 0.550 | NO LEAN | 19 | - | ok |
| 1564402 | Sat 31 Oct 15:00 | League One | Wycombe v Burton Albion | rejected | NO (Medium) | 0.561 | LEAN YES | 23 | mild | note |
| 1564399 | Sun 01 Nov 14:00 | League One | Sheffield Wednesday v Blackpool | rejected | NO (Medium) | 0.565 | NO LEAN | 16 | - | ok |
| 1563844 | Fri 30 Oct 19:45 | League Two | Newport County v Chesterfield | rejected | NO (Low) | 0.507 | NO LEAN | 21 | - | ok |
| 1563843 | Sat 31 Oct 12:30 | League Two | Grimsby v York | rejected | NO (Medium) | 0.517 | LEAN YES | 24 | mild | note |
| 1563846 | Sat 31 Oct 12:30 | League Two | Port Vale v Rochdale | rejected | NO (Low) | 0.489 | NO LEAN | 18 | - | ok |
| 1563839 | Sat 31 Oct 15:00 | League Two | Accrington ST v Northampton | rejected | NO (Low) | 0.491 | NO LEAN | 14 | - | ok |
| 1563840 | Sat 31 Oct 15:00 | League Two | Colchester v Walsall | rejected | NO (Low) | 0.510 | NO LEAN | 22 | - | ok |
| 1563841 | Sat 31 Oct 15:00 | League Two | Crewe v Barnet | rejected | NO (Medium) | 0.533 | LEAN YES | 28 | moderate | needs review |
| 1563842 | Sat 31 Oct 15:00 | League Two | Fleetwood Town v Bristol Rovers | rejected | NO (Low) | 0.513 | NO LEAN | 20 | - | ok |
| 1563845 | Sat 31 Oct 15:00 | League Two | Oldham v Crawley Town | rejected | NO (Medium) | 0.517 | LEAN YES | 23 | mild | note |
| 1563847 | Sat 31 Oct 15:00 | League Two | Salford City v Exeter City | rejected | NO (Low) | 0.497 | NO LEAN | 15 | - | ok |
| 1563848 | Sat 31 Oct 15:00 | League Two | Shrewsbury v Gillingham | rejected | NO (Medium) | 0.519 | LEAN YES | 23 | mild | note |
| 1563849 | Sat 31 Oct 15:00 | League Two | Swindon Town v Rotherham | rejected | NO (Low) | 0.503 | NO LEAN | 18 | - | ok |
| 1563850 | Sat 31 Oct 15:00 | League Two | Tranmere v Cheltenham | rejected | NO (Low) | 0.513 | NO LEAN | 23 | - | ok |
| 1552801 | Fri 30 Oct 18:00 | Ligue 1 | Le Havre v Paris Saint Germain | rejected | NO (Medium) | 0.567 | NO LEAN | 21 | - | ok |
| 1552806 | Fri 30 Oct 18:00 | Ligue 1 | Nice v Rennes | rejected | YES (Medium) | 0.560 | LEAN YES | 23 | note | note |
| 1552802 | Fri 30 Oct 20:05 | Ligue 1 | Lille v Lens | rejected | NO (Medium) | 0.545 | LEAN YES | 26 | moderate | needs review |
| 1552809 | Sat 31 Oct 19:45 | Ligue 1 | Estac Troyes v Le Mans | rejected | NO (Medium) | 0.544 | NO LEAN | 20 | - | ok |
| 1552803 | Sat 31 Oct 19:45 | Ligue 1 | Lorient v Stade Brestois 29 | rejected | NO (Medium) | 0.534 | NO LEAN | 21 | - | ok |
| 1552808 | Sun 01 Nov 14:00 | Ligue 1 | Strasbourg v Auxerre | rejected | NO (Medium) | 0.554 | LEAN YES | 28 | moderate | needs review |
| 1552804 | Sun 01 Nov 16:15 | Ligue 1 | Lyon v Angers | rejected | NO (Medium) | 0.556 | NO LEAN | 15 | - | ok |
| 1552807 | Sun 01 Nov 16:15 | Ligue 1 | Paris FC v Monaco | rejected | NO (Medium) | 0.559 | LEAN YES | 23 | mild | note |
| 1552805 | Sun 01 Nov 19:45 | Ligue 1 | Marseille v Toulouse | Medium | YES (Medium) | 0.569 | NO LEAN | 22 | - | ok |
| 1585317 | Fri 30 Oct 19:45 | National League | AFC Fylde v AFC Hornchurch | Medium | NO (Medium) | 0.552 | NO LEAN | 19 | - | ok |
| 1585318 | Sat 31 Oct 12:30 | National League | FC Halifax Town v Yeovil Town | Medium | YES (Medium) | 0.572 | LEAN YES | 24 | - | ok |
| 1585319 | Sat 31 Oct 12:30 | National League | Forest Green v Harrogate Town | rejected | NO (Medium) | 0.559 | NO LEAN | 17 | data | data check |
| 1585320 | Sat 31 Oct 15:00 | National League | Aldershot Town v Gateshead | Medium | NO (Medium) | 0.566 | NO LEAN | 22 | - | ok |
| 1585321 | Sat 31 Oct 15:00 | National League | Altrincham v Carlisle | rejected | NO (Medium) | 0.541 | NO LEAN | 17 | - | ok |
| 1585322 | Sat 31 Oct 15:00 | National League | Barrow v Eastleigh | Medium | NO (Medium) | 0.569 | NO LEAN | 20 | data | data check |
| 1585323 | Sat 31 Oct 15:00 | National League | Boreham Wood v Hartlepool | High | NO (Medium) | 0.561 | LEAN YES | 23 | mild | note |
| 1585324 | Sat 31 Oct 15:00 | National League | Solihull Moors v Kidderminster Harriers | rejected | NO (Medium) | 0.551 | NO LEAN | 18 | - | ok |
| 1585325 | Sat 31 Oct 15:00 | National League | Tamworth v Woking | Medium | YES (Medium) | 0.569 | LEAN YES | 25 | - | ok |
| 1585326 | Sat 31 Oct 15:00 | National League | Wealdstone v Southend | Medium | NO (Medium) | 0.572 | LEAN YES | 27 | moderate | needs review |
| 1585327 | Sat 31 Oct 15:00 | National League | Worthing v Sutton Utd | Medium | NO (Medium) | 0.560 | NO LEAN | 22 | - | ok |
| 1585328 | Sat 31 Oct 17:30 | National League | Boston United v Scunthorpe | Medium | NO (Medium) | 0.569 | LEAN YES | 23 | mild | note |
| 1587873 | Sat 31 Oct 15:00 | National League North | Bedford Town v Macclesfield | rejected | NO (Medium) | 0.532 | NO LEAN | 21 | - | ok |
| 1587874 | Sat 31 Oct 15:00 | National League North | Buxton v Marine | rejected | NO (Medium) | 0.548 | LEAN YES | 23 | mild | note |
| 1587875 | Sat 31 Oct 15:00 | National League North | Chester v Hednesford Town | rejected | NO (Medium) | 0.553 | NO LEAN | 22 | - | ok |
| 1587876 | Sat 31 Oct 15:00 | National League North | Hebburn Town v Harborough Town | rejected | NO (Medium) | 0.540 | NO LEAN | 15 | - | ok |
| 1587877 | Sat 31 Oct 15:00 | National League North | Hereford v King's Lynn Town | rejected | NO (Medium) | 0.548 | NO LEAN | 14 | - | ok |
| 1587878 | Sat 31 Oct 15:00 | National League North | Morecambe v Scarborough Athletic | rejected | NO (Medium) | 0.535 | NO LEAN | 20 | - | ok |
| 1587879 | Sat 31 Oct 15:00 | National League North | Oxford City v South Shields | rejected | NO (Medium) | 0.553 | NO LEAN | 19 | - | ok |
| 1587880 | Sat 31 Oct 15:00 | National League North | Radcliffe v Merthyr Town | rejected | NO (Medium) | 0.546 | NO LEAN | 20 | - | ok |
| 1587881 | Sat 31 Oct 15:00 | National League North | Southport v AFC Telford United | rejected | NO (Medium) | 0.550 | NO LEAN | 16 | - | ok |
| 1587882 | Sat 31 Oct 15:00 | National League North | Spalding United v Darlington 1883 | rejected | NO (Medium) | 0.546 | NO LEAN | 22 | - | ok |
| 1587883 | Sat 31 Oct 15:00 | National League North | Spennymoor Town v Chorley | rejected | NO (Medium) | 0.543 | NO LEAN | 21 | - | ok |
| 1587884 | Sat 31 Oct 15:00 | National League North | Worksop Town v Brackley Town | Medium | YES (Medium) | 0.555 | LEAN YES | 25 | - | ok |
| 1588425 | Sat 31 Oct 15:00 | National League South | AFC Totton v Chelmsford City | rejected | NO (Medium) | 0.555 | NO LEAN | 15 | - | ok |
| 1588426 | Sat 31 Oct 15:00 | National League South | Billericay Town v Hemel Hempstead Town | rejected | NO (Medium) | 0.551 | NO LEAN | 17 | - | ok |
| 1588427 | Sat 31 Oct 15:00 | National League South | Braintree v Hampton & Richmond | rejected | NO (Medium) | 0.561 | LEAN YES | 25 | moderate | needs review |
| 1588428 | Sat 31 Oct 15:00 | National League South | Chesham United v Folkestone Invicta | rejected | NO (Medium) | 0.555 | NO LEAN | 16 | - | ok |
| 1588429 | Sat 31 Oct 15:00 | National League South | Dorking Wanderers v Weston-super-Mare | Medium | YES (High) | 0.593 | YES | 30 | - | ok |
| 1588430 | Sat 31 Oct 15:00 | National League South | Dover v Farnham Town | rejected | YES (Medium) | 0.545 | LEAN YES | 23 | note | note |
| 1588431 | Sat 31 Oct 15:00 | National League South | Farnborough v Horsham | rejected | NO (Medium) | 0.539 | LEAN YES | 23 | mild | note |
| 1588432 | Sat 31 Oct 15:00 | National League South | Maidenhead v Dagenham & Redbridge | rejected | NO (Medium) | 0.550 | NO LEAN | 14 | - | ok |
| 1588433 | Sat 31 Oct 15:00 | National League South | Maidstone Utd v Slough Town | rejected | NO (Medium) | 0.554 | LEAN YES | 31 | moderate | needs review |
| 1588434 | Sat 31 Oct 15:00 | National League South | Tonbridge Angels v Salisbury | rejected | NO (Medium) | 0.539 | NO LEAN | 16 | - | ok |
| 1588435 | Sat 31 Oct 15:00 | National League South | Truro City v Ebbsfleet United | Medium | YES (Medium) | 0.567 | LEAN YES | 26 | - | ok |
| 1588436 | Sat 31 Oct 15:00 | National League South | Walton & Hersham v Torquay | rejected | NO (Medium) | 0.558 | NO LEAN | 18 | - | ok |
| 1596518 | Sat 31 Oct 15:00 | Northern Premier League | Alfreton Town v AFC Emley | Medium | NO (High) | 0.577 | YES | 24 | severe | needs review |
| 1596519 | Sat 31 Oct 15:00 | Northern Premier League | Ashton United v Rylands | Medium | YES (Medium) | 0.572 | NO LEAN | 22 | - | ok |
| 1596520 | Sat 31 Oct 15:00 | Northern Premier League | Bury v Workington | High | YES (High) | 0.586 | YES | 23 | - | ok |
| 1596521 | Sat 31 Oct 15:00 | Northern Premier League | Cleethorpes Town v Avro | Medium | NO (Medium) | 0.565 | NO LEAN | 21 | - | ok |
| 1596522 | Sat 31 Oct 15:00 | Northern Premier League | Curzon Ashton v Leek Town | High | YES (High) | 0.587 | YES | 24 | note | note |
| 1596524 | Sat 31 Oct 15:00 | Northern Premier League | Gainsborough Trinity v Bamber Bridge | High | NO (High) | 0.578 | YES | 21 | severe | needs review |
| 1596525 | Sat 31 Oct 15:00 | Northern Premier League | Ilkeston Town v Hyde United | Medium | NO (High) | 0.580 | YES | 16 | severe | needs review |
| 1596526 | Sat 31 Oct 15:00 | Northern Premier League | Redcar Athletic v Guiseley AFC | Medium | YES (Medium) | 0.570 | NO LEAN | 22 | note | note |
| 1596523 | Sat 31 Oct 15:00 | Northern Premier League | United of Manchester v Lancaster City | Medium | NO (High) | 0.585 | YES | 25 | severe | needs review |
| 1596527 | Sat 31 Oct 15:00 | Northern Premier League | Warrington Town v Quorn | Medium | YES (Medium) | 0.569 | LEAN YES | 28 | - | ok |
| 1596528 | Sat 31 Oct 15:00 | Northern Premier League | Whitby Town v Stockton Town | Medium | NO (Medium) | 0.573 | NO LEAN | 20 | - | ok |
| 1557450 | Sat 31 Oct 12:30 | Premier League | Chelsea v Manchester United | rejected | NO (Medium) | 0.550 | NO LEAN | 21 | - | ok |
| 1557448 | Sat 31 Oct 15:00 | Premier League | Bournemouth v Leeds | rejected | NO (Medium) | 0.538 | NO LEAN | 18 | - | ok |
| 1557449 | Sat 31 Oct 15:00 | Premier League | Brentford v Nottingham Forest | rejected | NO (Medium) | 0.547 | LEAN YES | 25 | moderate | needs review |
| 1557451 | Sat 31 Oct 15:00 | Premier League | Coventry v Sunderland | rejected | NO (Medium) | 0.532 | NO LEAN | 14 | - | ok |
| 1557452 | Sat 31 Oct 15:00 | Premier League | Hull City v Ipswich | rejected | NO (Medium) | 0.545 | LEAN YES | 26 | moderate | needs review |
| 1557454 | Sat 31 Oct 15:00 | Premier League | Manchester City v Brighton | rejected | NO (Medium) | 0.560 | NO LEAN | 15 | - | ok |
| 1557456 | Sat 31 Oct 17:30 | Premier League | Tottenham v Crystal Palace | rejected | NO (Medium) | 0.552 | NO LEAN | 17 | - | ok |
| 1557447 | Sat 31 Oct 20:00 | Premier League | Aston Villa v Fulham | rejected | NO (Medium) | 0.553 | NO LEAN | 21 | - | ok |
| 1557453 | Sun 01 Nov 16:30 | Premier League | Liverpool v Arsenal | rejected | NO (Medium) | 0.522 | NO LEAN | 11 | - | ok |
| 1575531 | Fri 30 Oct 20:15 | Primeira Liga | Casa Pia v Sporting CP | rejected | NO (Medium) | 0.548 | NO LEAN | 20 | - | ok |
| 1575535 | Sat 31 Oct 15:30 | Primeira Liga | Moreirense v Estrela | rejected | NO (Medium) | 0.548 | NO LEAN | 19 | - | ok |
| 1575532 | Sat 31 Oct 20:30 | Primeira Liga | FC Porto v Estoril | rejected | NO (Medium) | 0.545 | LEAN YES | 23 | mild | note |
| 1575528 | Sun 01 Nov 15:30 | Primeira Liga | Arouca v Nacional | rejected | NO (Medium) | 0.543 | NO LEAN | 16 | - | ok |
| 1575527 | Sun 01 Nov 18:00 | Primeira Liga | Academico Viseu v Rio Ave | Medium | NO (Medium) | 0.544 | NO LEAN | 19 | - | ok |
| 1575534 | Sun 01 Nov 18:00 | Primeira Liga | Maritimo v Santa Clara | rejected | NO (Medium) | 0.545 | NO LEAN | 19 | - | ok |
| 1575530 | Sun 01 Nov 20:30 | Primeira Liga | SC Braga v Famalicao | rejected | NO (Medium) | 0.550 | NO LEAN | 18 | - | ok |
| 1556890 | Fri 30 Oct 19:30 | Scottish Championship | Stenhousemuir v Livingston | rejected | NO (Low) | 0.485 | NO LEAN | 14 | - | ok |
| 1556886 | Sat 31 Oct 15:00 | Scottish Championship | Arbroath v Raith Rovers | rejected | NO (Low) | 0.512 | NO LEAN | 19 | - | ok |
| 1556887 | Sat 31 Oct 15:00 | Scottish Championship | Ayr Utd v Queen's Park | rejected | NO (Low) | 0.497 | NO LEAN | 16 | - | ok |
| 1556888 | Sat 31 Oct 15:00 | Scottish Championship | Dunfermline v Inverness CT | rejected | NO (Low) | 0.480 | NO LEAN | 14 | - | ok |
| 1556889 | Sat 31 Oct 15:00 | Scottish Championship | Partick v Morton | rejected | NO (Low) | 0.495 | NO LEAN | 17 | - | ok |
| 1644191 | Sat 31 Oct 15:00 | Scottish Cup |  Johnstone Burgh v Formartine United | rejected | NO (Medium) | 0.552 | NO LEAN | 0 | - | ok |
| 1644185 | Sat 31 Oct 15:00 | Scottish Cup | Cumbernauld Colts v Banks O' Dee | rejected | NO (Medium) | 0.552 | NO LEAN | 0 | - | ok |
| 1644189 | Sat 31 Oct 15:00 | Scottish Cup | Hill Of Beath Hawthorn v Musselburgh Athletic | rejected | NO (Medium) | 0.552 | NO LEAN | 0 | - | ok |
| 1644198 | Sat 31 Oct 15:00 | Scottish Cup | Threave Rovers v Pollok | rejected | NO (Medium) | 0.552 | NO LEAN | 0 | - | ok |
| 1639572 | Sat 31 Oct 17:30 | Scottish League Cup | Rangers v Aberdeen | Medium | NO (Medium) | 0.560 | NO LEAN | 21 | - | ok |
| 1639571 | Sun 01 Nov 15:00 | Scottish League Cup | Heart Of Midlothian v Hibernian | Medium | NO (Medium) | 0.551 | LEAN YES | 24 | mild | note |
| 1557066 | Sat 31 Oct 15:00 | Scottish League One | Airdrie United v Cove Rangers | rejected | NO (Medium) | 0.550 | NO LEAN | 19 | data | data check |
| 1557067 | Sat 31 Oct 15:00 | Scottish League One | East Fife v Queen of the South | rejected | NO (Medium) | 0.550 | NO LEAN | 20 | - | ok |
| 1557068 | Sat 31 Oct 15:00 | Scottish League One | East Kilbride v Ross County | Medium | YES (Medium) | 0.554 | NO LEAN | 22 | data | data check |
| 1557069 | Sat 31 Oct 15:00 | Scottish League One | Hamilton Academical v Montrose | Medium | NO (Medium) | 0.560 | LEAN YES | 23 | mild | note |
| 1557070 | Sat 31 Oct 15:00 | Scottish League One | Peterhead v Alloa Athletic | rejected | NO (Medium) | 0.546 | NO LEAN | 18 | - | ok |
| 1557804 | Sat 31 Oct 15:00 | Scottish League Two | Edinburgh City v Dumbarton | Medium | NO (High) | 0.590 | YES | 23 | severe | needs review |
| 1557805 | Sat 31 Oct 15:00 | Scottish League Two | Kelty Hearts v Elgin City | High | NO (High) | 0.583 | YES | 24 | severe | needs review |
| 1557806 | Sat 31 Oct 15:00 | Scottish League Two | Spartans v Annan Athletic | Medium | NO (High) | 0.579 | YES | 17 | severe | needs review |
| 1557807 | Sat 31 Oct 15:00 | Scottish League Two | Stirling Albion v Forfar Athletic | High | NO (High) | 0.578 | YES | 27 | severe | needs review |
| 1557808 | Sat 31 Oct 15:00 | Scottish League Two | Stranraer v Clyde | Medium | YES (High) | 0.582 | YES | 25 | - | ok |
| 1556697 | Sat 31 Oct 15:00 | Scottish Premiership | Kilmarnock v ST Johnstone | rejected | NO (Medium) | 0.561 | LEAN YES | 24 | mild | note |
| 1556698 | Sat 31 Oct 15:00 | Scottish Premiership | Motherwell v ST Mirren | rejected | NO (Medium) | 0.568 | NO LEAN | 20 | - | ok |
| 1556699 | Sat 31 Oct 15:00 | Scottish Premiership | Rangers v Aberdeen | Medium | NO (Medium) | 0.551 | NO LEAN | 21 | - | ok |
| 1556695 | Sun 01 Nov 13:00 | Scottish Premiership | Falkirk v Celtic | rejected | NO (Medium) | 0.554 | NO LEAN | 21 | - | ok |
| 1550179 | Sat 31 Oct 14:00 | Serie A | Bologna v Monza | Medium | YES (Medium) | 0.573 | LEAN YES | 28 | - | ok |
| 1550186 | Sat 31 Oct 17:00 | Serie A | Udinese v AS Roma | rejected | NO (Medium) | 0.514 | NO LEAN | 14 | - | ok |
| 1550177 | Sat 31 Oct 19:45 | Serie A | AC Milan v Inter | Medium | YES (Medium) | 0.570 | NO LEAN | 22 | - | ok |
| 1550180 | Sun 01 Nov 11:30 | Serie A | Como v Venezia | rejected | NO (Medium) | 0.535 | NO LEAN | 14 | - | ok |
| 1550181 | Sun 01 Nov 14:00 | Serie A | Frosinone v Torino | Medium | YES (Medium) | 0.571 | LEAN YES | 24 | - | ok |
| 1550183 | Sun 01 Nov 14:00 | Serie A | Lazio v Cagliari | High | NO (Medium) | 0.564 | NO LEAN | 21 | - | ok |
| 1550184 | Sun 01 Nov 17:00 | Serie A | Lecce v Genoa | rejected | NO (Medium) | 0.544 | NO LEAN | 17 | - | ok |
| 1550182 | Sun 01 Nov 19:45 | Serie A | Juventus v Napoli | Medium | NO (Medium) | 0.558 | NO LEAN | 18 | - | ok |
| 1596976 | Sat 31 Oct 14:00 | Southern Premier Central | Stamford v Halesowen Town | rejected | NO (Medium) | 0.571 | NO LEAN | 21 | - | ok |
| 1596969 | Sat 31 Oct 15:00 | Southern Premier Central | Anstey Nomads v Bishop's Stortford | Medium | YES (Medium) | 0.570 | LEAN YES | 28 | - | ok |
| 1596970 | Sat 31 Oct 15:00 | Southern Premier Central | Bury Town v Banbury United | rejected | YES (Medium) | 0.567 | NO LEAN | 19 | note | note |
| 1596971 | Sat 31 Oct 15:00 | Southern Premier Central | Leamington v Peterborough Sports | Medium | YES (Medium) | 0.572 | LEAN YES | 28 | - | ok |
| 1596972 | Sat 31 Oct 15:00 | Southern Premier Central | Leighton Town v Bromsgrove Sporting | rejected | NO (Medium) | 0.563 | LEAN YES | 26 | moderate | needs review |
| 1596973 | Sat 31 Oct 15:00 | Southern Premier Central | Leiston v Alvechurch | rejected | NO (Medium) | 0.565 | NO LEAN | 19 | - | ok |
| 1596974 | Sat 31 Oct 15:00 | Southern Premier Central | Redditch United v Needham Market | Medium | YES (Medium) | 0.551 | LEAN YES | 29 | - | ok |
| 1596975 | Sat 31 Oct 15:00 | Southern Premier Central | Rushall Olympic v Racing Club Warwick | Medium | NO (Medium) | 0.570 | NO LEAN | 21 | - | ok |
| 1596977 | Sat 31 Oct 15:00 | Southern Premier Central | Stourbridge v Kettering Town | Medium | NO (Medium) | 0.558 | LEAN YES | 23 | mild | note |
| 1596978 | Sat 31 Oct 15:00 | Southern Premier Central | Stratford Town v Hitchin Town | Medium | NO (Medium) | 0.570 | NO LEAN | 21 | - | ok |
| 1596979 | Sat 31 Oct 15:00 | Southern Premier Central | Worcester City v Real Bedford | rejected | NO (Medium) | 0.542 | NO LEAN | 18 | - | ok |
| 1597431 | Sat 31 Oct 15:00 | Southern Premier South | Bath City v Poole Town | Medium | NO (Medium) | 0.558 | LEAN YES | 23 | mild | note |
| 1597432 | Sat 31 Oct 15:00 | Southern Premier South | Chertsey Town v Basingstoke Town | Medium | NO (Medium) | 0.568 | NO LEAN | 22 | - | ok |
| 1597433 | Sat 31 Oct 15:00 | Southern Premier South | Evesham United v Bracknell Town | Medium | NO (Medium) | 0.567 | NO LEAN | 17 | - | ok |
| 1597434 | Sat 31 Oct 15:00 | Southern Premier South | Frome Town v Chichester City | Medium | YES (Medium) | 0.572 | LEAN YES | 25 | - | ok |
| 1597435 | Sat 31 Oct 15:00 | Southern Premier South | Gloucester City v Berkhamsted | Medium | NO (Medium) | 0.563 | LEAN YES | 25 | moderate | needs review |
| 1597436 | Sat 31 Oct 15:00 | Southern Premier South | Gosport Borough v Hanwell Town | Medium | NO (Medium) | 0.552 | LEAN YES | 25 | moderate | needs review |
| 1597437 | Sat 31 Oct 15:00 | Southern Premier South | Hanworth Villa v Plymouth Parkway | Medium | NO (Medium) | 0.560 | LEAN YES | 27 | moderate | needs review |
| 1597438 | Sat 31 Oct 15:00 | Southern Premier South | Havant & Wville v Taunton Town | High | YES (Medium) | 0.572 | LEAN YES | 28 | - | ok |
| 1597439 | Sat 31 Oct 15:00 | Southern Premier South | Sholing v Malvern Town | Medium | NO (Medium) | 0.569 | LEAN YES | 24 | mild | note |
| 1597440 | Sat 31 Oct 15:00 | Southern Premier South | Uxbridge v Yate Town | Medium | NO (Medium) | 0.556 | NO LEAN | 16 | - | ok |
| 1597441 | Sat 31 Oct 15:00 | Southern Premier South | Wimborne Town v Chippenham Town | High | NO (High) | 0.586 | YES | 18 | severe | needs review |
| 1584455 | Fri 30 Oct 17:00 | Super Lig | Konyaspor v Galatasaray | rejected | NO (Medium) | 0.517 | NO LEAN | 11 | - | ok |
| 1584450 | Sat 31 Oct 10:30 | Super Lig | Erzurumspor FK v Çorum FK | rejected | NO (Medium) | 0.532 | NO LEAN | 16 | - | ok |
| 1584454 | Sat 31 Oct 13:00 | Super Lig | Kocaelispor v Rizespor | rejected | YES (Medium) | 0.541 | NO LEAN | 21 | - | ok |
| 1584451 | Sat 31 Oct 16:00 | Super Lig | Fenerbahçe v Göztepe | Medium | NO (Medium) | 0.565 | NO LEAN | 16 | - | ok |
| 1584448 | Sun 01 Nov 10:30 | Super Lig | Amed v Eyüpspor | Medium | NO (Medium) | 0.526 | NO LEAN | 14 | - | ok |
| 1584449 | Sun 01 Nov 13:00 | Super Lig | Başakşehir v Samsunspor | rejected | NO (Medium) | 0.559 | NO LEAN | 16 | - | ok |
| 1584456 | Sun 01 Nov 13:00 | Super Lig | Trabzonspor v Gaziantep FK | Medium | NO (Medium) | 0.544 | NO LEAN | 14 | - | ok |
| 1584453 | Sun 01 Nov 16:00 | Super Lig | Kasımpaşa v Beşiktaş | rejected | NO (Medium) | 0.559 | NO LEAN | 19 | - | ok |
| 1565519 | Fri 30 Oct 16:00 | Ukrainian Premier | Obolon'-Brovar v Shakhtar Donetsk | rejected | NO (Low) | 0.513 | NO LEAN | 14 | data | data check |
| 1565517 | Sat 31 Oct 11:00 | Ukrainian Premier | Livyi Bereh v Bukovyna | rejected | NO (Low) | 0.510 | NO LEAN | 17 | - | ok |
| 1565520 | Sat 31 Oct 11:00 | Ukrainian Premier | Veres Rivne v Chornomorets | rejected | NO (Medium) | 0.519 | NO LEAN | 17 | - | ok |
| 1565514 | Sat 31 Oct 16:00 | Ukrainian Premier | Karpaty v Kudrivka | rejected | NO (Medium) | 0.534 | LEAN YES | 25 | moderate | needs review |
| 1565516 | Sat 31 Oct 16:00 | Ukrainian Premier | Kryvbas KR v Dynamo Kyiv | rejected | NO (Medium) | 0.534 | NO LEAN | 15 | data | data check |
| 1565513 | Sat 31 Oct 16:00 | Ukrainian Premier | Zorya Luhansk v Epitsentr Dunayivtsi | rejected | NO (Medium) | 0.525 | NO LEAN | 20 | - | ok |
| 1565515 | Sun 01 Nov 11:00 | Ukrainian Premier | Kolos Kovalivka v Polessya | rejected | NO (Medium) | 0.524 | NO LEAN | 19 | - | ok |
| 1565518 | Sun 01 Nov 11:00 | Ukrainian Premier | LNZ Cherkasy v FC Kharkiv | rejected | NO (Medium) | 0.543 | NO LEAN | 19 | - | ok |