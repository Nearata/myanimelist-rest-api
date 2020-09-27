from fastapi import APIRouter, Depends

from mal.scrapers import AnimeScrapers
from mal.utils import CacheUtil
from mal.validators import AnimeParameters, Anime2Parameters


router = APIRouter()

@router.get("/{mal_id}/{mal_request}")
def anime(params: AnimeParameters = Depends()) -> dict:
    scrapers = AnimeScrapers(params.mal_id)
    data = getattr(scrapers, params.mal_request)()

    CacheUtil.save(f"anime{params.mal_id}{params.mal_request}", data)

    return data

@router.get("/{mal_id}/{mal_request}/{page_number}")
def anime_2(params: Anime2Parameters = Depends()) -> dict:
    scrapers = AnimeScrapers(params.mal_id)
    data = getattr(scrapers, params.mal_request)(params.page_number)

    CacheUtil.save(f"anime{params.mal_id}{params.mal_request}", data)

    return data
