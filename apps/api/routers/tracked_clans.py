from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database import get_db

router = APIRouter(prefix="/api")


class TrackedClanCreate(BaseModel):
    clan_tag: str
    note: str | None = None


@router.get("/tracked-clans")
def list_tracked_clans():
    db = get_db()
    tracked = (
        db.table("tracked_clans")
        .select("*")
        .order("added_at", desc=True)
        .execute()
    )
    clan_tags = [r["clan_tag"] for r in tracked.data]
    clans_map: dict = {}
    if clan_tags:
        clans_resp = (
            db.table("clans")
            .select("tag, name, badge_url, clan_level, members_count")
            .in_("tag", clan_tags)
            .execute()
        )
        clans_map = {c["tag"]: c for c in clans_resp.data}

    for row in tracked.data:
        row["clans"] = clans_map.get(row["clan_tag"])

    return {"data": tracked.data}


@router.post("/tracked-clans", status_code=201)
def add_tracked_clan(body: TrackedClanCreate):
    db = get_db()
    tag = body.clan_tag.strip().upper()
    if not tag.startswith("#"):
        tag = f"#{tag}"

    row = {"clan_tag": tag, "note": body.note}
    try:
        resp = db.table("tracked_clans").insert(row).execute()
    except Exception as exc:
        if "duplicate" in str(exc).lower() or "unique" in str(exc).lower():
            raise HTTPException(status_code=409, detail=f"Clan {tag} is already tracked")
        raise
    return resp.data[0] if resp.data else row


@router.delete("/tracked-clans/{tag:path}", status_code=204)
def remove_tracked_clan(tag: str):
    db = get_db()
    db.table("tracked_clans").delete().eq("clan_tag", tag).execute()
    return None
