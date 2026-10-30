"""config.py  -  the 17 leagues and the cups. Ids are verified by probe.py against the API's own names."""
SEASONS = [2023, 2024, 2025, 2026]     # 2023 = 2023-24 season, etc.
ODDS_DAYS_AHEAD = 8                    # pull pre-match odds for fixtures kicking off within this many days
FINISHED = ("FT", "AET", "PEN")
DEAD = ("CANC", "ABD", "AWD", "WO", "PST", "TBD")   # kept with status, never trained on

LEAGUES = {   # name: (league_id, country)
    "Premier League": (39, "England"), "Championship": (40, "England"), "League One": (41, "England"),
    "League Two": (42, "England"), "National League": (43, "England"),
    "National League North": (50, "England"), "National League South": (51, "England"),
    "Scottish Premiership": (179, "Scotland"), "Scottish Championship": (180, "Scotland"),
    "Scottish League One": (183, "Scotland"), "Scottish League Two": (184, "Scotland"),
    "La Liga": (140, "Spain"), "Bundesliga": (78, "Germany"), "Ligue 1": (61, "France"),
    "Eredivisie": (88, "Netherlands"), "Primeira Liga": (94, "Portugal"), "Super Lig": (203, "Turkey"),
}
CUPS = {      # loaded historically too (decision 25 Sep: train on cups), flagged is_cup=1
    "FA Cup": (45, "England"), "EFL Cup": (48, "England"), "EFL Trophy": (46, "England"), "FA Trophy": (47, "England"),
    "Scottish Cup": (181, "Scotland"), "Scottish League Cup": (185, "Scotland"), "Scottish Challenge Cup": (182, "Scotland"),  # ids verified by probe 25 Sep 2026
    # European club competitions, added 19 Oct 2026 at Rob's request. is_cup=1: form still comes from domestic league games only.
    "Champions League": (2, "World"), "Europa League": (3, "World"), "Conference League": (848, "World"),
    "DFB Pokal": (81, "Germany"), "Copa del Rey": (143, "Spain"),      # added 27 Oct 2026 at Rob's request
}
FORM_LEAGUES = {  # domestic leagues loaded ONLY so European-tie opponents have last-5 league form. Never presented on their own.
    "Serie A": (135, "Italy"), "Belgian Pro League": (144, "Belgium"), "Swiss Super League": (207, "Switzerland"),
    "Austrian Bundesliga": (218, "Austria"), "Czech Liga": (345, "Czech-Republic"), "Greek Super League": (197, "Greece"),
    "Danish Superliga": (119, "Denmark"), "Eliteserien": (103, "Norway"), "Allsvenskan": (113, "Sweden"), "Croatian HNL": (210, "Croatia"),
    "Ekstraklasa": (106, "Poland"), "Ukrainian Premier": (333, "Ukraine"), "Serbian Super Liga": (286, "Serbia"), "Cypriot Division 1": (318, "Cyprus"),
    "Israeli Premier": (383, "Israel"), "Slovak Super Liga": (332, "Slovakia"), "Hungarian NB I": (271, "Hungary"), "Romanian Liga I": (283, "Romania"),
    "Bulgarian First League": (172, "Bulgaria"), "Slovenian PrvaLiga": (373, "Slovenia"), "Kazakh Premier": (389, "Kazakhstan"),
    "Azerbaijan Premyer": (419, "Azerbaijan"), "League of Ireland": (357, "Ireland"), "Icelandic Urvalsdeild": (164, "Iceland"), "Veikkausliiga": (244, "Finland"),
}
LEAGUES.update(FORM_LEAGUES)
NONLEAGUE = {  # step 3 and 4, results only. Added 28 Sep 2026 at Rob's request. Fixture lists only; no stats/odds coverage.
    "Northern Premier League": (59, "England"), "Isthmian Premier": (58, "England"),
    "Southern Premier Central": (931, "England"), "Southern Premier South": (60, "England"),
    "NPL Div One East": (932, "England"), "NPL Div One Midlands": (55, "England"), "NPL Div One West": (54, "England"),
    "Isthmian Div One North": (52, "England"), "Isthmian Div One South Central": (53, "England"), "Isthmian Div One South East": (57, "England"),
    "Southern Div One Central": (933, "England"), "Southern Div One South": (56, "England"),
}
COUNTRIES = ["England", "Scotland", "Spain", "Germany", "France", "Netherlands", "Portugal", "Turkey"]

# Presentation order: English tiers, English cups, Scottish tiers and cups, then Europe. Fixtures alphabetical by home team within each.
ORDER = ["Premier League", "Championship", "League One", "League Two", "National League", "National League North", "National League South",
         "Northern Premier League", "Isthmian Premier", "Southern Premier Central", "Southern Premier South",
         "NPL Div One East", "NPL Div One Midlands", "NPL Div One West", "Isthmian Div One North", "Isthmian Div One South Central", "Isthmian Div One South East",
         "Southern Div One Central", "Southern Div One South",
         "FA Cup", "EFL Cup", "EFL Trophy", "FA Trophy",
         "Scottish Premiership", "Scottish Championship", "Scottish League One", "Scottish League Two", "Scottish Cup", "Scottish League Cup", "Scottish Challenge Cup",
         "Champions League", "Europa League", "Conference League",
         "Bundesliga", "DFB Pokal", "La Liga", "Copa del Rey", "Ligue 1", "Eredivisie", "Primeira Liga", "Super Lig",
         "Serie A", "Belgian Pro League", "Austrian Bundesliga", "Danish Superliga", "Eliteserien", "Allsvenskan", "Ekstraklasa", "Czech Liga",
         "Croatian HNL", "Ukrainian Premier", "Greek Super League"]
ORDER += [n for n in FORM_LEAGUES if n not in ORDER]      # remaining form-only leagues last
# V4.1 (30 Oct 2026): Rob's 14 monitored leagues come first, in his order; everything else keeps its old relative order after them.
ROB_ORDER = ["Premier League", "Championship", "League One", "League Two", "National League", "National League North", "National League South",
             "Bundesliga", "Eredivisie", "Ligue 1", "Super Lig", "Scottish Premiership", "La Liga", "Primeira Liga"]
ORDER = ROB_ORDER + [n for n in ORDER if n not in ROB_ORDER]
