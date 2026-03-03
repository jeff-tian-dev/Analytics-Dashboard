-- 001_core_tables.sql
-- Tables: clans, tracked_clans, players

CREATE TABLE IF NOT EXISTS clans (
    tag             TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    description     TEXT,
    badge_url       TEXT,
    clan_level      INT NOT NULL DEFAULT 0,
    members_count   INT NOT NULL DEFAULT 0,
    clan_points     INT NOT NULL DEFAULT 0,
    clan_capital_points INT NOT NULL DEFAULT 0,
    war_frequency   TEXT,
    war_win_streak  INT NOT NULL DEFAULT 0,
    war_wins        INT NOT NULL DEFAULT 0,
    war_ties        INT NOT NULL DEFAULT 0,
    war_losses      INT NOT NULL DEFAULT 0,
    war_league_id   INT,
    capital_league_id INT,
    is_war_log_public BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tracked_clans (
    clan_tag    TEXT PRIMARY KEY,
    note        TEXT,
    added_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS players (
    tag                         TEXT PRIMARY KEY,
    name                        TEXT NOT NULL,
    clan_tag                    TEXT REFERENCES clans(tag) ON DELETE SET NULL,
    town_hall_level             INT NOT NULL DEFAULT 1,
    exp_level                   INT NOT NULL DEFAULT 1,
    trophies                    INT NOT NULL DEFAULT 0,
    best_trophies               INT NOT NULL DEFAULT 0,
    war_stars                   INT NOT NULL DEFAULT 0,
    attack_wins                 INT NOT NULL DEFAULT 0,
    defense_wins                INT NOT NULL DEFAULT 0,
    role                        TEXT,
    war_preference              TEXT,
    clan_capital_contributions  INT NOT NULL DEFAULT 0,
    league_name                 TEXT,
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_players_clan_tag ON players(clan_tag);
CREATE INDEX IF NOT EXISTS idx_players_updated_at ON players(updated_at);
