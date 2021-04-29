from fastapi import APIRouter, Depends, Request
from requests import Session

from mal.config import CACHE
from mal.scrapers import AnimeScrapers
from mal.session import get_session
from mal.utils import CacheUtil
from mal.validators import Anime2Parameters, AnimeParameters

router = APIRouter()


@router.get("/{mal_id}/{mal_request}")
def anime(
    params: AnimeParameters = Depends(), session: Session = Depends(get_session)
) -> dict:
    scrapers = AnimeScrapers(session, params.mal_id)
    data = getattr(scrapers, params.mal_request)()

    if CACHE:
        CacheUtil.save(f"anime{params.mal_id}{params.mal_request}", data)

    return data


@router.get("/{mal_id}/{mal_request}/{page_number}")
def anime_2(
    params: Anime2Parameters = Depends(), session: Session = Depends(get_session)
) -> dict:
    scrapers = AnimeScrapers(session, params.mal_id)
    data = getattr(scrapers, params.mal_request)(params.page_number)

    if CACHE:
        CacheUtil.save(f"anime{params.mal_id}{params.mal_request}", data)

    return data
