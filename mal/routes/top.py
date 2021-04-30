from fastapi import APIRouter, Depends

from mal.scrapers import AnimeScrapers
from mal.state import get_anime
from mal.validators import TopPathValidator

router = APIRouter()


@router.get("/{request}/{ttype}/{page_number}")
def anime_top(
    params: TopPathValidator = Depends(),
    scrapers: AnimeScrapers = Depends(get_anime),
) -> dict:
    data = scrapers.top(params.ttype, params.page_number)
    return data
