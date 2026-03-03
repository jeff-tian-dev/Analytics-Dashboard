import logging
from urllib.parse import quote

import httpx

from .config import COC_API_TOKEN, COC_BASE_URL

logger = logging.getLogger(__name__)

_HEADERS = {"Authorization": f"Bearer {COC_API_TOKEN}", "Accept": "application/json"}
_TIMEOUT = httpx.Timeout(30.0)


def _encode_tag(tag: str) -> str:
    return quote(tag, safe="")


def _client() -> httpx.Client:
    return httpx.Client(base_url=COC_BASE_URL, headers=_HEADERS, timeout=_TIMEOUT)


def get_clan(client: httpx.Client, tag: str) -> dict | None:
    resp = client.get(f"/clans/{_encode_tag(tag)}")
    if resp.status_code == 404:
        logger.warning("Clan %s not found", tag)
        return None
    resp.raise_for_status()
    return resp.json()


def get_current_war(client: httpx.Client, tag: str) -> dict | None:
    resp = client.get(f"/clans/{_encode_tag(tag)}/currentwar")
    if resp.status_code in (404, 403):
        logger.info("War data unavailable for %s (status %d)", tag, resp.status_code)
        return None
    resp.raise_for_status()
    data = resp.json()
    if data.get("state") == "notInWar":
        return None
    return data


def get_capital_raids(client: httpx.Client, tag: str, limit: int = 5) -> list[dict]:
    resp = client.get(f"/clans/{_encode_tag(tag)}/capitalraidseasons", params={"limit": limit})
    if resp.status_code in (404, 403):
        logger.info("Capital raid data unavailable for %s", tag)
        return []
    resp.raise_for_status()
    return resp.json().get("items", [])


def get_player(client: httpx.Client, tag: str) -> dict | None:
    resp = client.get(f"/players/{_encode_tag(tag)}")
    if resp.status_code == 404:
        logger.warning("Player %s not found", tag)
        return None
    resp.raise_for_status()
    return resp.json()


def create_client() -> httpx.Client:
    return _client()
