# Profitability test with real prices (19 Nov 2026, research only, no model change)

Evaluation layer only: Bet365 Over 2.5 prices stored in fixture_odds are used to score outcomes, never to select in production.
Window: every finished league fixture in Rob's 14 leagues with a stored Bet365 price, 30 Sep to 2 Nov 2026 (578 fixtures),
season 2026-27, the model's only clean out-of-sample season. Level £1 singles. P/L in units; 90% range by bootstrap.

| Rule | Bets | Hits | Median price | P/L (units) | 90% range |
|---|---|---|---|---|---|
| All fixtures | 578 | 333 | 1.67 | -28.5 | -60.8 to 3.7 |
| Selected (High+Medium) | 164 | 110 | 1.50 | +0.7 | -14.2 to 15.9 |
| High | 64 | 44 | 1.40 | -2.6 | -11.4 to 5.7 |
| Medium | 100 | 66 | 1.57 | +3.3 | -8.7 to 15.8 |
| Rejected | 414 | 223 | 1.73 | -29.2 | -58.4 to -0.7 |
| Selected, price >= 1.51 | 73 | 42 | 1.62 | -2.8 | -14.0 to 9.0 |
| Selected, score x price >= 1.00 | 35 | 23 | 1.70 | +5.0 | -3.5 to 13.1 |
| Selected, at best price of 8 bookmakers | 164 | 110 | 1.52 | +3.4 | -12.2 to 18.8 |

Accuracy: Brier model 0.2420, Bet365 implied 0.2391 (lower is better): the market was slightly more accurate than the model.
Selected fixtures: model score 0.623 on average, Bet365 implied 0.671, actual 110 of 164.

Stability (chronological halves): selected +5.1 then -4.4; score x price >= 1.00: +7.4 (17 bets) then -2.5 (18 bets). No rule is stable.
13 rules were tried on the same 578 fixtures, so the best one is expected to look good by chance. Nothing here is proven.

Proposed for out-of-sample tracking only (pre-registered 19 Nov 2026, judged after 300 qualifying bets): "V1 value selected" =
model High or Medium AND best available price x model score >= 1.00, level stakes, singles. Needs pre-match prices logged each run.
