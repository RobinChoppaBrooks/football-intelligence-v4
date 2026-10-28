"""store.py  -  SQLite schema for the historical store. Import ensure_schema(conn)."""
SCHEMA = """
CREATE TABLE IF NOT EXISTS api_cache (
  key TEXT PRIMARY KEY, endpoint TEXT, params TEXT, fetched_at TEXT, http_status INTEGER, result_count INTEGER, response TEXT);
CREATE TABLE IF NOT EXISTS api_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, endpoint TEXT, params TEXT, http_status INTEGER, result_count INTEGER, remaining INTEGER, error TEXT);
CREATE TABLE IF NOT EXISTS competitions (
  league_id INTEGER PRIMARY KEY, name TEXT, country TEXT, type TEXT, is_cup INTEGER, tier TEXT, seasons_loaded TEXT);
CREATE TABLE IF NOT EXISTS coverage (
  league_id INTEGER, season INTEGER, start TEXT, end TEXT, current INTEGER,
  cov_events INTEGER, cov_lineups INTEGER, cov_stats_fixtures INTEGER, cov_stats_players INTEGER,
  cov_standings INTEGER, cov_players INTEGER, cov_injuries INTEGER, cov_predictions INTEGER, cov_odds INTEGER,
  PRIMARY KEY(league_id, season));
CREATE TABLE IF NOT EXISTS teams (team_id INTEGER PRIMARY KEY, name TEXT, country TEXT);
CREATE TABLE IF NOT EXISTS fixtures (
  fixture_id INTEGER PRIMARY KEY, league_id INTEGER, season INTEGER, round TEXT, kickoff_utc TEXT,
  home_id INTEGER, away_id INTEGER, status TEXT, ht_home INTEGER, ht_away INTEGER, ft_home INTEGER, ft_away INTEGER,
  stats_fetched INTEGER DEFAULT 0, odds_fetched INTEGER DEFAULT 0, events_fetched INTEGER DEFAULT 0, updated_at TEXT);
CREATE INDEX IF NOT EXISTS ix_fixtures_league_season ON fixtures(league_id, season);
CREATE INDEX IF NOT EXISTS ix_fixtures_kickoff ON fixtures(kickoff_utc);
CREATE TABLE IF NOT EXISTS fixture_stats (
  fixture_id INTEGER, team_id INTEGER, shots INTEGER, shots_on_target INTEGER, shots_off_target INTEGER, blocked INTEGER,
  shots_inside_box INTEGER, shots_outside_box INTEGER, corners INTEGER, possession REAL, fouls INTEGER, offsides INTEGER,
  saves INTEGER, passes INTEGER, pass_accuracy REAL, xg REAL, fetched_at TEXT, PRIMARY KEY(fixture_id, team_id));
CREATE TABLE IF NOT EXISTS fixture_odds (
  fixture_id INTEGER, bookmaker_id INTEGER, bookmaker TEXT, over25 REAL, under25 REAL, btts_yes REAL, btts_no REAL,
  odds_update TEXT, fetched_at TEXT, PRIMARY KEY(fixture_id, bookmaker_id));
CREATE TABLE IF NOT EXISTS fixture_events (
  fixture_id INTEGER, seq INTEGER, minute INTEGER, extra INTEGER, team_id INTEGER, type TEXT, detail TEXT, PRIMARY KEY(fixture_id, seq));
CREATE TABLE IF NOT EXISTS injuries (
  fixture_id INTEGER, team_id INTEGER, player_id INTEGER, player TEXT, type TEXT, reason TEXT, fetched_at TEXT, PRIMARY KEY(fixture_id, team_id, player_id));
CREATE TABLE IF NOT EXISTS market_odds (
  fixture_id INTEGER, bookmaker TEXT, bet TEXT, value TEXT, odd REAL, fetched_at TEXT, PRIMARY KEY(fixture_id, bookmaker, bet, value));
CREATE TABLE IF NOT EXISTS predictions_log (
  fixture_id INTEGER, model_version TEXT, made_at TEXT, p_over25 REAL, exp_home REAL, exp_away REAL, p_btts REAL,
  market_p_over25 REAL, tier TEXT, features TEXT, PRIMARY KEY(fixture_id, model_version, made_at));
"""
def ensure_schema(conn):
    conn.executescript(SCHEMA); conn.commit()
