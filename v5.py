"""
v5.py  -  "V5 short-Overs accumulator portfolio": research model, pre-registered 19 Nov 2026 (docs/research/v5_short_overs/).

Separate from V4.1: V4.1's selection model, cut points and reports are untouched. V5 uses bookmaker prices by design,
because the overnight research of 19 Nov 2026 found the profit sits in pricing, not in form data.

Rule (fixed; never tuned on live results):
  Leg pool: Over 2.5 goals, Friday to Sunday, the 12 leagues with price history (Premier League, Championship, League One,
  League Two, National League, Bundesliga, Eredivisie, Ligue 1, Super Lig, Scottish Premiership, La Liga, Primeira Liga).
  fair = average across bookmakers of the margin-free Over 2.5 chance (needs 3+ bookmakers); price = Bet365 Over 2.5 (>= 1.10).
  Bets each weekend (stakes as a share of the bank; £ for a £1,000 bank):
    3 trebles   legs 1-9   of the fair >= 0.60 pool ranked by fair x price   1.5% each (£15)
    2 five-folds legs 1-10 of the same ranking                                1.0% each (£10)
    1 eight-fold the 8 highest-fair legs with fair >= 0.60                    0.5% (£5)
    1 ten-fold   the 10 highest-fair legs with fair >= 0.55                   0.5% (£5)
  A bet is skipped when the pool is too small. Legs may appear in more than one bet; each bet is separate.

    python v5.py slip YYYY-MM-DD YYYY-MM-DD [--bank 1000] [--no-fetch]   prices (API odds) + this weekend's slip
    python v5.py review                                                 settles logged bets into data/v5/v5_tracker.md
"""
import os, sys, json, csv, sqlite3
from datetime import datetime, timezone
import numpy as np, pandas as pd

LEAGUES = ["Premier League", "Championship", "League One", "League Two", "National League", "Bundesliga", "Eredivisie",
           "Ligue 1", "Super Lig", "Scottish Premiership", "La Liga", "Primeira Liga"]
BOOST = {2: .025, 3: .05, 4: .075, 5: .10, 6: .125, 7: .15, 8: .20, 9: .25, 10: .30}   # Bet365 published tiers, for reference only
PORTFOLIO = [("treble", 3, 3, 0.015, 0.60, "value"), ("five-fold", 5, 2, 0.010, 0.60, "value"),
             ("eight-fold", 8, 1, 0.005, 0.60, "fair"), ("ten-fold", 10, 1, 0.005, 0.55, "fair")]
LOG, TRACK = "data/v5/v5_bets.csv", "data/v5/v5_tracker.md"

def build(pool, bank=1000.0):
    """pool: DataFrame with fixture_id, fair, price (+ any labels). Returns list of bets: (name, n, stake, legs DataFrame)."""
    bets = []
    for name, n, count, share, minp, rank in PORTFOLIO:
        t = pool[(pool.fair >= minp) & (pool.price >= 1.10)]
        t = t.assign(key=t.fair * t.price if rank == "value" else t.fair).sort_values(["key", "fixture_id"], ascending=[False, True])
        for i in range(count):
            legs = t.iloc[i * n:(i + 1) * n]
            if len(legs) == n: bets.append((f"{name} {i + 1}" if count > 1 else name, n, round(bank * share, 2), legs))
    return bets

def fair_from_odds(o):
    """o: rows fixture_id, bookmaker, over25, under25 -> per fixture fair (mean margin-free Over chance), books, b365."""
    o = o[(o.over25 > 1) & (o.under25 > 1)].copy()
    o["q"] = (1 / o.over25) / (1 / o.over25 + 1 / o.under25)
    g = o.groupby("fixture_id")
    out = pd.DataFrame({"fair": g.q.mean(), "books": g.q.size()})
    out["price"] = o[o.bookmaker == "Bet365"].groupby("fixture_id").over25.last()
    return out[(out.books >= 3) & out.price.notna()]

def slip(start, end, bank=1000.0, fetch=True, db="football.db"):
    from config_v5 import league_ids
    c = sqlite3.connect(db)
    lids = league_ids(LEAGUES)
    s_utc = pd.Timestamp(start, tz="Europe/London").tz_convert("UTC").isoformat()
    e_utc = (pd.Timestamp(end, tz="Europe/London") + pd.Timedelta(days=1)).tz_convert("UTC").isoformat()
    fx = pd.read_sql(f"select f.fixture_id, f.league_id, f.kickoff_utc, h.name home, a.name away from fixtures f join teams h on h.team_id=f.home_id "
                     f"join teams a on a.team_id=f.away_id where f.status='NS' and f.kickoff_utc>=? and f.kickoff_utc<? and f.league_id in ({','.join('?' * len(lids))})",
                     c, params=(s_utc, e_utc, *lids))
    if fetch and len(fx):
        from api import Client
        from log_prices import parse
        cl = Client(db); now = datetime.now(timezone.utc).isoformat(timespec="seconds"); n = 0
        for fid in fx.fixture_id:
            try: prices = parse(cl.get("odds", use_cache=False, fixture=int(fid)))
            except RuntimeError as e: print(f"  {e}"); break
            for (bid, bname), (ov, un, upd) in prices.items():
                cl.db.execute("INSERT OR REPLACE INTO fixture_odds VALUES(?,?,?,?,?,?,?,?,?)", (int(fid), bid, bname, ov, un, None, None, upd, now))
            n += 1
        cl.db.commit(); print(f"odds fetched for {n} of {len(fx)} fixtures, API calls {cl.calls_this_run}")
    o = pd.read_sql("select fixture_id, bookmaker, over25, under25 from fixture_odds", c)
    F = fair_from_odds(o[o.fixture_id.isin(fx.fixture_id)])
    pool = fx.join(F, on="fixture_id", how="inner")
    comp = dict(pd.read_sql("select league_id, name from competitions", c).values)
    pool["competition"] = pool.league_id.map(comp)
    pool["kickoff_uk"] = pd.to_datetime(pool.kickoff_utc, utc=True).dt.tz_convert("Europe/London").dt.strftime("%a %d %b %H:%M")
    bets = build(pool, bank)
    run = datetime.now(timezone.utc).strftime("v5_%Y%m%d_%H%M")
    outdir = f"reports/v5/{start}"; os.makedirs(outdir, exist_ok=True); os.makedirs(os.path.dirname(LOG), exist_ok=True)
    L = [f"# V5 short-Overs slip: {start} to {end} (research model, paper-trade until Rob decides)", "",
         f"Run {run}. Pool: {len(pool)} priced fixtures; fair 0.60+: {int((pool.fair >= .6).sum())}. Bank £{bank:.0f}. "
         "Prices are Bet365 Over 2.5 at the time of this run; check each on the betslip. Total stake £%.2f." % sum(b[2] for b in bets), ""]
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new: w.writerow(["run_id", "created_at", "bet", "n", "stake", "fixture_id", "kickoff_uk", "competition", "home", "away", "fair", "price", "window"])
        for name, n, stake, legs in bets:
            odds = float(np.prod(legs.price))
            L += [f"## {name.capitalize()}: £{stake:.2f} at {odds:.2f} (pays £{stake * odds:.2f} before any boost)", "",
                  "| Fixture | Comp | When | Bet365 Over 2.5 |", "|---|---|---|---|"]
            for r in legs.itertuples():
                L.append(f"| {r.home} v {r.away} | {r.competition} | {r.kickoff_uk} | {r.price:.2f} |")
                w.writerow([run, datetime.now(timezone.utc).isoformat(timespec="seconds"), name, n, stake, int(r.fixture_id), r.kickoff_uk, r.competition, r.home, r.away, round(float(r.fair), 4), r.price, start])
            L.append("")
    if not bets: L.append("Pool too small for any bet this window.")
    open(f"{outdir}/v5_slip.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    pool.to_csv(f"{outdir}/v5_pool.csv", index=False)
    print("\n".join(L)); return bets

def review(db="football.db"):
    if not os.path.exists(LOG): print("no V5 bets logged"); return
    b = pd.read_csv(LOG); c = sqlite3.connect(db)
    # one slip per weekend: the latest run logged for each window (a hand run on Thursday is replaced by the Friday 07:00 run)
    keep = b.groupby("window").run_id.max(); b = b[b.run_id == b.window.map(keep)]
    fx = pd.read_sql("select fixture_id, status, ft_home, ft_away from fixtures", c).set_index("fixture_id")
    b = b.join(fx, on="fixture_id"); b["hit"] = (b.ft_home + b.ft_away) >= 3
    rows = []
    for (run, bet), g in b.groupby(["run_id", "bet"]):
        void = g.status.isin(["PST", "CANC", "ABD", "AWD", "WO"]).any()
        settled = (g.status == "FT").all()
        odds = float(np.prod(g.price)); won = settled and bool(g.hit.all())
        lost = (g.status == "FT").any() and bool((~g.hit[g.status == "FT"]).any())
        rows.append(dict(run=run, bet=bet, n=int(g.n.iloc[0]), stake=float(g.stake.iloc[0]), odds=round(odds, 2),
                         state="lost" if lost else ("won" if won else ("void leg, check" if void else "open")),
                         ret=float(g.stake.iloc[0]) * odds if won else 0.0, boost_ret=float(g.stake.iloc[0]) * (1 + (odds - 1) * (1 + BOOST.get(int(g.n.iloc[0]), 0))) if won else 0.0))
    R = pd.DataFrame(rows); s = R[R.state.isin(["won", "lost"])]
    L = ["# V5 short-Overs tracker (paper trade, research only)", "",
         "Pre-registered 19 Nov 2026. Judge after 40 weekends; rules are not changed on what this shows.", "",
         f"Settled bets: {len(s)} (won {int((s.state == 'won').sum())}). Staked £{s.stake.sum():.2f}. Returned £{s.ret.sum():.2f} "
         f"(£{s.boost_ret.sum():.2f} if Bet365's Acca Boost applied). P/L £{s.ret.sum() - s.stake.sum():+.2f} (with boost £{s.boost_ret.sum() - s.stake.sum():+.2f}).",
         f"Weekends counted: {R.run.nunique()} (latest slip per weekend). Open or void-check bets: {int((~R.state.isin(['won', 'lost'])).sum())}.", "",
         "| Run | Bet | Legs | Stake | Odds | Result | Return |", "|---|---|---|---|---|---|---|"]
    L += [f"| {r.run} | {r.bet} | {r.n} | £{r.stake:.2f} | {r.odds} | {r.state} | £{r.ret:.2f} |" for r in R.itertuples()]
    os.makedirs(os.path.dirname(TRACK), exist_ok=True); open(TRACK, "w").write("\n".join(L) + "\n"); print("\n".join(L[:6]))

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "slip":
        bank = float(a[a.index("--bank") + 1]) if "--bank" in a else 1000.0
        slip(a[1], a[2], bank, fetch="--no-fetch" not in a)
    elif a[0] == "review": review()
    else: sys.exit(__doc__)
