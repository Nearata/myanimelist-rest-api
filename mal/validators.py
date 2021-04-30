from typing import Union

from fastapi import Path, Query
from pydantic import BaseModel, validator

from .exceptions import MissingParameter, ParameterNotValid
from .scrapers.anime_scrapers import AnimeScrapers


class TopPathValidator(BaseModel):
    request: str = Path(...)
    ttype: str = Path(...)
    page_number: int = Path(..., gt=0)

    @validator("request")
    def validate_request(cls, v: str) -> Union[str, ParameterNotValid]:
        if not any(i == v for i in ["anime"]):
            raise ParameterNotValid("request")

        return v

    @validator("ttype")
    def validate_ttype(cls, v: str) -> Union[str, ParameterNotValid]:
        if v not in (
            "all",
            "airing",
            "upcoming",
            "tv",
            "movie",
            "ova",
            "ona",
            "special",
            "bypopularity",
            "favorite",
        ):
            raise ParameterNotValid("type")

        return v


class AnimeParameters(BaseModel):
    mal_id: int = Path(..., gt=0)
    mal_request: str = Path(...)

    @validator("mal_request")
    def validate_mal_request(
        cls, v: str
    ) -> Union[str, MissingParameter, ParameterNotValid]:
        if v not in (
            "characters",
            "clubs",
            "details",
            "episodes",
            "featured",
            "moreinfo",
            "news",
            "pictures",
            "recommendations",
            "reviews",
            "staff",
            "stats",
        ):
            raise ParameterNotValid("mal_request")

        if v in ("episodes", "reviews"):
            raise MissingParameter("page_number")

        return v


class Anime2Parameters(BaseModel):
    mal_id: int = Path(..., gt=0)
    mal_request: str = Path(...)
    page_number: int = Path(..., gt=0)

    @validator("mal_request")
    def validate_mal_request(cls, v: str) -> Union[str, ParameterNotValid]:
        if v not in ("episodes", "reviews"):
            raise ParameterNotValid("mal_request")

        return v


class SearchParameters(BaseModel):
    request: str = Path(...)

    @validator("request")
    def validate_request(cls, v: str) -> Union[str, ParameterNotValid]:
        if not any(i == v for i in ["anime"]):
            raise ParameterNotValid("request")

        return v

    query: str = Query(..., min_length=3)
    type: int = Query(None, gt=0, lt=7)
    score: int = Query(None, gt=0, lt=11)
    status: int = Query(None, gt=0, lt=4)
    producer: int = Query(None)
    rated: int = Query(None, gt=0, lt=7)
    start_day: int = Query(None, gt=0, lt=32)
    start_month: int = Query(None, gt=0, lt=13)
    start_year: int = Query(None, gt=999, lt=10000)
    end_day: int = Query(None, gt=0, lt=32)
    end_month: int = Query(None, gt=0, lt=13)
    end_year: int = Query(None, gt=999, lt=10000)
    genres: str = Query(None)
    genres_exclude: int = Query(None, gt=0, lt=2)
    columns: str = Query(None)
