-- 003_capital_raids.sql
-- Tables: capital_raids, raid_members

CREATE TABLE IF NOT EXISTS capital_raids (
    id                          BIGSERIAL PRIMARY KEY,
    clan_tag                    TEXT NOT NULL REFERENCES clans(tag),
    state                       TEXT NOT NULL,
    start_time                  TIMESTAMPTZ NOT NULL,
    end_time                    TIMESTAMPTZ NOT NULL,
    capital_total_loot          INT NOT NULL DEFAULT 0,
    raids_completed             INT NOT NULL DEFAULT 0,
    total_attacks               INT NOT NULL DEFAULT 0,
    enemy_districts_destroyed   INT NOT NULL DEFAULT 0,
    offensive_reward            INT NOT NULL DEFAULT 0,
    defensive_reward            INT NOT NULL DEFAULT 0,
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(clan_tag, start_time)
);

CREATE INDEX IF NOT EXISTS idx_capital_raids_clan_tag ON capital_raids(clan_tag);
CREATE INDEX IF NOT EXISTS idx_capital_raids_updated_at ON capital_raids(updated_at);

CREATE TABLE IF NOT EXISTS raid_members (
    id                          BIGSERIAL PRIMARY KEY,
    raid_id                     BIGINT NOT NULL REFERENCES capital_raids(id) ON DELETE CASCADE,
    player_tag                  TEXT NOT NULL,
    name                        TEXT NOT NULL,
    attacks                     INT NOT NULL DEFAULT 0,
    attack_limit                INT NOT NULL DEFAULT 0,
    bonus_attack_limit          INT NOT NULL DEFAULT 0,
    capital_resources_looted    INT NOT NULL DEFAULT 0,
    UNIQUE(raid_id, player_tag)
);

CREATE INDEX IF NOT EXISTS idx_raid_members_raid_id ON raid_members(raid_id);
