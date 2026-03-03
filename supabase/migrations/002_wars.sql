-- 002_wars.sql
-- Tables: wars, war_attacks

CREATE TABLE IF NOT EXISTS wars (
    id                          BIGSERIAL PRIMARY KEY,
    clan_tag                    TEXT NOT NULL REFERENCES clans(tag),
    opponent_tag                TEXT,
    opponent_name               TEXT,
    state                       TEXT NOT NULL,
    team_size                   INT,
    attacks_per_member          INT,
    preparation_start_time      TIMESTAMPTZ,
    start_time                  TIMESTAMPTZ,
    end_time                    TIMESTAMPTZ,
    clan_stars                  INT NOT NULL DEFAULT 0,
    clan_destruction_pct        NUMERIC(5,2) NOT NULL DEFAULT 0,
    opponent_stars              INT NOT NULL DEFAULT 0,
    opponent_destruction_pct    NUMERIC(5,2) NOT NULL DEFAULT 0,
    result                      TEXT,
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(clan_tag, preparation_start_time)
);

CREATE INDEX IF NOT EXISTS idx_wars_clan_tag ON wars(clan_tag);
CREATE INDEX IF NOT EXISTS idx_wars_state ON wars(state);
CREATE INDEX IF NOT EXISTS idx_wars_updated_at ON wars(updated_at);

CREATE TABLE IF NOT EXISTS war_attacks (
    id                      BIGSERIAL PRIMARY KEY,
    war_id                  BIGINT NOT NULL REFERENCES wars(id) ON DELETE CASCADE,
    attacker_tag            TEXT NOT NULL,
    defender_tag            TEXT NOT NULL,
    stars                   INT NOT NULL DEFAULT 0,
    destruction_percentage  NUMERIC(5,2) NOT NULL DEFAULT 0,
    attack_order            INT NOT NULL,
    duration                INT,
    UNIQUE(war_id, attacker_tag, attack_order)
);

CREATE INDEX IF NOT EXISTS idx_war_attacks_war_id ON war_attacks(war_id);
