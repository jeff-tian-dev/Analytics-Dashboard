import logging

from . import supercell_client as coc
from . import db

logger = logging.getLogger(__name__)


def run_once() -> None:
    tracked = db.get_tracked_clans()
    if not tracked:
        logger.warning("No clans in tracked_clans table — nothing to ingest")
        return

    logger.info("Starting ingestion for %d tracked clan(s)", len(tracked))
    client = coc.create_client()

    try:
        for entry in tracked:
            clan_tag = entry["clan_tag"]
            logger.info("--- Processing clan %s ---", clan_tag)
            _ingest_clan(client, clan_tag)
    finally:
        client.close()

    logger.info("Ingestion complete")


def _ingest_clan(client, clan_tag: str) -> None:
    clan_data = coc.get_clan(client, clan_tag)
    if not clan_data:
        logger.error("Could not fetch clan %s, skipping", clan_tag)
        return

    db.upsert_clan(clan_data)

    member_list = clan_data.get("memberList", [])
    logger.info("Fetching %d player(s) for clan %s", len(member_list), clan_tag)
    for member in member_list:
        player_data = coc.get_player(client, member["tag"])
        if player_data:
            db.upsert_player(player_data)

    war_data = coc.get_current_war(client, clan_tag)
    if war_data:
        war_id = db.upsert_war(war_data, clan_tag)
        if war_id:
            db.upsert_war_attacks(war_id, war_data)
    else:
        logger.info("No active war for %s", clan_tag)

    raids = coc.get_capital_raids(client, clan_tag, limit=5)
    logger.info("Got %d capital raid season(s) for %s", len(raids), clan_tag)
    for raid in raids:
        raid_id = db.upsert_capital_raid(raid, clan_tag)
        if raid_id:
            db.upsert_raid_members(raid_id, raid.get("members", []))
