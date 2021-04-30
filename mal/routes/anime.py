from fastapi import APIRouter, Depends

from mal.config import CACHE
from mal.scrapers import AnimeScrapers
from mal.state import CacheUtil, get_anime, get_cache
from mal.validators import Anime2Parameters, AnimeParameters

router = APIRouter()


@router.get("/{mal_id}/{mal_request}")
def anime(
    params: AnimeParameters = Depends(),
    cache: CacheUtil = Depends(get_cache),
    scrapers: AnimeScrapers = Depends(get_anime),
) -> dict:
    request = params.mal_request
    mal_id = params.mal_id
    data = getattr(scrapers, request)(mal_id)

    if CACHE:
        cache.save(f"anime{mal_id}{request}", data)

    return data


@router.get("/{mal_id}/{mal_request}/{page_number}")
def anime_2(
    params: Anime2Parameters = Depends(),
    cache: CacheUtil = Depends(get_cache),
    scrapers: AnimeScrapers = Depends(get_anime),
) -> dict:
    request = params.mal_request
    mal_id = params.mal_id
    page = params.page_number
    data = getattr(scrapers, request)(mal_id, page)

    if CACHE:
        cache.save(f"anime{params.mal_id}{params.mal_request}", data)

    return data
