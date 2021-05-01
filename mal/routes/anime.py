from fastapi import APIRouter, Depends

from mal.config import CACHE
from mal.scrapers.anime_scrapers import AnimeScrapers
from mal.state import CacheUtil, get_anime, get_cache
from mal.validators import Anime2Parameters, AnimeParameters

router = APIRouter()


@router.get("/{mal_id}/{mal_request}")
async def anime(
    params: AnimeParameters = Depends(),
    cache: CacheUtil = Depends(get_cache),
    scrapers: AnimeScrapers = Depends(get_anime),
) -> dict:
    request = params.mal_request
    mal_id = params.mal_id
    data = await getattr(scrapers, request)(mal_id)

    if CACHE:
        await cache.save(f"anime{mal_id}{request}", data)

    return data


@router.get("/{mal_id}/{mal_request}/{page_number}")
async def anime_2(
    params: Anime2Parameters = Depends(),
    cache: CacheUtil = Depends(get_cache),
    scrapers: AnimeScrapers = Depends(get_anime),
) -> dict:
    request = params.mal_request
    mal_id = params.mal_id
    page_number = params.page_number
    data = await getattr(scrapers, request)(mal_id, page_number)

    if CACHE:
        await cache.save(f"anime{mal_id}{request}{page_number}", data)

    return data
