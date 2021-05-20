from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from mal.config import CACHE
from mal.scrapers.anime_scrapers import AnimeScrapers
from mal.state import CacheUtil, get_anime, get_cache
from mal.validators import AnimeParameters

router = APIRouter()


@router.get("/anime")
async def anime(
    params: AnimeParameters = Depends(),
    cache: CacheUtil = Depends(get_cache),
    scrapers: AnimeScrapers = Depends(get_anime),
) -> JSONResponse:
    mal_id = params.mal_id
    mal_request = params.mal_request

    cache_key = f"anime{mal_id}{mal_request}"

    if page_number := params.page_number:
        cache_key += str(page_number)
        data = await getattr(scrapers, mal_request)(mal_id, page_number)
    else:
        data = await getattr(scrapers, mal_request)(mal_id)

    if CACHE:
        await cache.save(cache_key, data)

    return JSONResponse(data, status_code=201)
