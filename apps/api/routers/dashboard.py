from fastapi import APIRouter
from ..database import get_db

router = APIRouter(prefix="/api")


@router.get("/dashboard")
def dashboard_summary():
    db = get_db()

    clans = db.table("clans").select("*", count="exact").execute()
    players = db.table("players").select("*", count="exact").execute()
    wars = db.table("wars").select("*", count="exact").execute()
    active_wars = db.table("wars").select("*", count="exact").in_("state", ["preparation", "inWar"]).execute()
    raids = db.table("capital_raids").select("*", count="exact").execute()

    recent_wars = (
        db.table("wars")
        .select("id, clan_tag, opponent_name, state, result, start_time, clan_stars, opponent_stars")
        .order("start_time", desc=True)
        .limit(5)
        .execute()
    )
    recent_raids = (
        db.table("capital_raids")
        .select("id, clan_tag, state, start_time, capital_total_loot, raids_completed")
        .order("start_time", desc=True)
        .limit(5)
        .execute()
    )

    return {
        "total_clans": clans.count or 0,
        "total_players": players.count or 0,
        "total_wars": wars.count or 0,
        "active_wars": active_wars.count or 0,
        "total_raids": raids.count or 0,
        "recent_wars": recent_wars.data,
        "recent_raids": recent_raids.data,
    }
