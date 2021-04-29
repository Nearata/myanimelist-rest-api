from fastapi import APIRouter, Depends

from mal.scrapers import AnimeScrapers
from mal.validators import TopPathValidator

router = APIRouter()

@router.get("/{request}/{ttype}/{page_number}")
def anime_top(params: TopPathValidator = Depends()) -> dict:
    scrapers = AnimeScrapers()
    data = scrapers.top(params.ttype, params.page_number)
    return data
