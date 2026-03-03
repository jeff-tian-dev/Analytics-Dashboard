from fastapi import APIRouter, Query
from ..database import get_db

router = APIRouter(prefix="/api")


@router.get("/players")
def list_players(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    clan_tag: str | None = None,
    search: str | None = None,
):
    db = get_db()
    query = db.table("players").select("*", count="exact")

    if clan_tag:
        query = query.eq("clan_tag", clan_tag)
    if search:
        query = query.ilike("name", f"%{search}%")

    offset = (page - 1) * page_size
    query = query.order("name").range(offset, offset + page_size - 1)
    resp = query.execute()

    return {
        "data": resp.data,
        "total": resp.count or 0,
        "page": page,
        "page_size": page_size,
    }


@router.get("/players/{tag:path}")
def get_player(tag: str):
    db = get_db()
    resp = db.table("players").select("*").eq("tag", tag).single().execute()
    return resp.data
