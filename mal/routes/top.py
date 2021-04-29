from fastapi import APIRouter, Depends
from requests import Session

from mal.scrapers import AnimeScrapers
from mal.session import get_session
from mal.validators import TopPathValidator

router = APIRouter()

@router.get("/{request}/{ttype}/{page_number}")
def anime_top(params: TopPathValidator = Depends(), session: Session = Depends(get_session)) -> dict:
    scrapers = AnimeScrapers(session)
    data = scrapers.top(params.ttype, params.page_number)
    return data
