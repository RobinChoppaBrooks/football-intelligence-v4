# V5 short-Overs accumulator portfolio: overnight research, 19 Nov 2026 (research only)

Rob's brief: reverse engineer a weekly model that makes a profit, using the data we have. V4.1 is unchanged.

## Data
- Real bookmaker prices: football-data.co.uk results-and-odds files for 12 of Rob's 14 leagues (no National League North or
  South), seasons 2023-24 to 2026-27 (to 19 Nov), fetched by the "fetch-odds" hand run into data/research_odds/.
- 15,764 of 15,775 priced matches linked to football.db fixtures (date, score and team names): data/research_odds/matched_prices.csv.
- Prices used: Bet365 pre-match Over/Under 2.5 (the snapshot football-data takes before the weekend), Bet365 closing, market
  average and best price; "fair" = margin-free Over chance from the market average.

## What the data says (counts and units; P/L is per £1 level stake unless stated)
1. The market is close to efficient. Betting every Over at Bet365 lost every season (-144.8, -285.3, -129.8, -32.1 units).
   Unders were worse.
2. V4.1 adds nothing beyond the price. On its two out-of-training seasons (2025-26, 2026-27) the market alone predicted results
   better (log loss 0.6767 v 0.6876; 0.6654 v 0.6773) and adding the V4.1 score did not improve on the market.
3. New form models trained walk-forward with the market as an input did not beat the market either, and no edge threshold
   stayed positive across 2024-25, 2025-26 and 2026-27 (r4, r5).
4. A scan of 184 segments (league, price band, midweek, early/late season, Scored 2+ / Let in 2+ sums, V4.1 selected) found none
   positive in all of 2023-24, 2024-25 and 2025-26 (r8).
5. Late price moves carry the information: Overs whose Bet365 price shortened before kick-off made +200.1 units on 6,166;
   drifters lost -616.0 on 6,497. Friday information predicts the move only weakly (AUC about 0.58) and not profitably (r7).
6. Short Overs are underpriced. Where the market's fair Over chance was 0.60+, 1,696 of 2,462 landed against 1,612 expected by
   the market: at Bet365's price that is break-even as singles (about -0.4p per £1).
7. Same-weekend legs land together more than independent pricing assumes: 438 five-folds of 0.60+ legs won 81 times, against
   71.2 expected from the legs' own hit rate and 57.1 from market prices. Bookmakers price accumulators as independent.
8. Points 6 and 7 together make short-Over accumulators profitable: 55 of 66 portfolio settings were positive with Bet365's
   published Acca Boost and 46 of 66 without it (r13, grid.csv).

## V5 rule (pre-registered 19 Nov 2026, v5.py; not to be tuned on live results)
Leg pool: Over 2.5, Friday to Sunday, the 12 priced leagues; fair = mean margin-free Over chance across 3+ bookmakers; Bet365
Over price 1.10+. Weekly bets (share of bank; £ for £1,000): 3 trebles from legs 1-9 of the fair 0.60+ pool ranked by fair x
price (1.5% each); 2 five-folds from legs 1-10 of that ranking (1.0% each); an eight-fold of the 8 highest-fair 0.60+ legs
(0.5%); a ten-fold of the 10 highest-fair 0.55+ legs (0.5%). About £75 a weekend on £1,000.

## Backtest of the V5 rule (£1,000 bank, flat stakes, Bet365 pre-match prices)
| Season | Bets | Won | Staked | P/L no boost | P/L with Bet365 boost tiers |
|---|---|---|---|---|---|
| 2023-24 | 262 | 52 | £2,815 | +£89 | +£351 |
| 2024-25 | 266 | 59 | £2,860 | +£176 | +£396 |
| 2025-26 | 256 | 70 | £2,750 | +£1,157 | +£1,485 |
| 2026-27 to date | 93 | 21 | £990 | +£105 | +£191 |
| Total | 877 | 202 | £9,415 | +£1,526 | +£2,423 |

136 weekends; 56 in profit; worst run -£452; best weekend +£463; without the best two weekends still +£1,573 (with boost).
Weekly P/L: mean £17.80, standard deviation £99.10 (about 2 standard errors above zero over 136 weekends).
Stress tests (with boost): at Bet365 closing prices +£1,225; at the worse of pre-match and closing on every leg +£42.
Live reproduction: the API's 8-bookmaker fair chance matches football-data's (correlation 0.991; same side of 0.60 for 435 of 446).
Independent check: weekend of 17 Oct 2025 rebuilt from the raw CSV files matched the backtest legs, odds and results exactly.

## Caveats
- The weekly portfolio was assembled after seeing the grid, so the backtest flatters it; the broad grid result (55 of 66
  positive) is the stronger evidence. Only live results settle it: judge after 40 weekends.
- Bet365's Acca Boost tiers are from published guides; whether Over/Under goals qualifies on Bet365 is not confirmed.
- Bet365 restricts accounts that win; prices taken later than the pre-match snapshot were tested (closing) but not every time.
- Prices in the historical files are snapshots; the live slip uses prices at the Friday 07:00 run.

## Running it
- Automatic: the Friday weekend run writes reports/v5/<Friday>/v5_slip.md and logs bets in data/v5/v5_bets.csv;
  the Monday review settles them into data/v5/v5_tracker.md.
- By hand: "v5 YYYY-MM-DD YYYY-MM-DD" (about one API call per fixture in the window).
