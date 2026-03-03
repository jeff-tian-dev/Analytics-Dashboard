from fastapi import APIRouter, Query
from ..database import get_db

router = APIRouter(prefix="/api")


@router.get("/raids")
def list_raids(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    clan_tag: str | None = None,
):
    db = get_db()
    query = db.table("capital_raids").select("*", count="exact")

    if clan_tag:
        query = query.eq("clan_tag", clan_tag)

    offset = (page - 1) * page_size
    query = query.order("start_time", desc=True).range(offset, offset + page_size - 1)
    resp = query.execute()

    return {
        "data": resp.data,
        "total": resp.count or 0,
        "page": page,
        "page_size": page_size,
    }


@router.get("/raids/{raid_id}")
def get_raid(raid_id: int):
    db = get_db()
    raid = db.table("capital_raids").select("*").eq("id", raid_id).single().execute()
    members = (
        db.table("raid_members")
        .select("*")
        .eq("raid_id", raid_id)
        .order("capital_resources_looted", desc=True)
        .execute()
    )
    result = raid.data
    result["members"] = members.data
    return result
