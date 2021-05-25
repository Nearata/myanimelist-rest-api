from json import loads
from typing import Optional

from httpx import AsyncClient, TimeoutException
from starlette.responses import JSONResponse
from starlette.requests import Request

from .config import CACHE, USER_AGENT
from .responses import HTTPErrorResponse
from .utils import CacheUtil
from .scrapers import AnimeScrapers


async def cached_response(
    cache_util: CacheUtil,
    cache_key: str,
    page_number: Optional[int] = None,
) -> Optional[JSONResponse]:
    if not CACHE:
        return None

    if page_number:
        cache_key += str(page_number)

    query = cache_util.query(cache_key)

    exists = await query.exists()
    if not exists:
        return None

    cache = await query.get()
    if cache_util.is_expired(cache):
        await cache.delete()
        return None

    return JSONResponse(loads(cache.json))

async def mal_response(
    session: AsyncClient, path: str, mal_id: Optional[int] = None
) -> Optional[HTTPErrorResponse]:
    excluded_routes = ("/search", "/top")
    url = f"https://myanimelist.net"

    if path not in excluded_routes:
        url += f"{path}/{mal_id}"

    try:
        response = await session.head(
            url,
            timeout=15,
            headers={"User-Agent": USER_AGENT},
        )
        status_code = response.status_code
    except TimeoutException:
        return HTTPErrorResponse(504)

    if path in excluded_routes:
        return None

    if status_code == 404:
        return HTTPErrorResponse(404)

    if not str(status_code).startswith("2"):
        return HTTPErrorResponse(status_code)

    return None

def get_cache(request: Request) -> CacheUtil:
    return request.app.state.cache


def get_anime(request: Request) -> AnimeScrapers:
    return request.app.state.animescrapers


def get_session(request: Request) -> AsyncClient:
    return request.app.state.session
