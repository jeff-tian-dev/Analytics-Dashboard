from fastapi import APIRouter, Query
from ..database import get_db

router = APIRouter(prefix="/api")


@router.get("/wars")
def list_wars(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    clan_tag: str | None = None,
    state: str | None = None,
):
    db = get_db()
    query = db.table("wars").select("*", count="exact")

    if clan_tag:
        query = query.eq("clan_tag", clan_tag)
    if state:
        query = query.eq("state", state)

    offset = (page - 1) * page_size
    query = query.order("start_time", desc=True).range(offset, offset + page_size - 1)
    resp = query.execute()

    return {
        "data": resp.data,
        "total": resp.count or 0,
        "page": page,
        "page_size": page_size,
    }


@router.get("/wars/{war_id}")
def get_war(war_id: int):
    db = get_db()
    war = db.table("wars").select("*").eq("id", war_id).single().execute()
    attacks = (
        db.table("war_attacks")
        .select("*")
        .eq("war_id", war_id)
        .order("attack_order")
        .execute()
    )
    result = war.data
    result["attacks"] = attacks.data
    return result
