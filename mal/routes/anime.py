from fastapi import APIRouter, Depends
from httpx import AsyncClient
from starlette.responses import JSONResponse

from ..config import CACHE
from ..dependencies import cached_response, mal_response
from ..scrapers import AnimeScrapers
from ..state import CacheUtil, get_anime, get_cache, get_session
from ..validators import AnimeParameters

router = APIRouter(prefix="/anime")


@router.get("")
async def anime(
    params: AnimeParameters = Depends(),
    cache: CacheUtil = Depends(get_cache),
    scrapers: AnimeScrapers = Depends(get_anime),
    session: AsyncClient = Depends(get_session),
) -> JSONResponse:
    mal_id = params.mal_id
    mal_request = params.mal_request

    cache_key = f"anime{mal_id}{mal_request}"

    if cached := await cached_response(params, cache, cache_key):
        return cached

    if response := await mal_response(
        mal_id=mal_id, session=session, path=router.prefix
    ):
        return response

    if page_number := params.page_number:
        cache_key += str(page_number)
        data = await getattr(scrapers, mal_request)(mal_id, page_number)
    else:
        data = await getattr(scrapers, mal_request)(mal_id)

    if CACHE:
        await cache.save(cache_key, data)

    return JSONResponse(data, status_code=201)
