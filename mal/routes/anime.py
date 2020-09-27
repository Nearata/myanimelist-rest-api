from fastapi import APIRouter, Depends

from mal.scrapers import AnimeScrapers
from mal.utils import CacheUtil
from mal.validators import AnimeParameters, Anime2Parameters
from mal.config import Config


router = APIRouter()

@router.get("/{mal_id}/{mal_request}")
def anime(params: AnimeParameters = Depends()) -> dict:
    scrapers = AnimeScrapers(params.mal_id)
    data = getattr(scrapers, params.mal_request)()

    if Config.CACHE:
        CacheUtil.save(f"anime{params.mal_id}{params.mal_request}", data)

    return data

@router.get("/{mal_id}/{mal_request}/{page_number}")
def anime_2(params: Anime2Parameters = Depends()) -> dict:
    scrapers = AnimeScrapers(params.mal_id)
    data = getattr(scrapers, params.mal_request)(params.page_number)

    if Config.CACHE:
        CacheUtil.save(f"anime{params.mal_id}{params.mal_request}", data)

    return data
