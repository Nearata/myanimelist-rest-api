from inspect import getmembers, iscoroutinefunction

from fastapi import Query
from pydantic import BaseModel, validator
from pydantic.class_validators import root_validator

from .exceptions import InvalidParameter, MissingParameter
from .scrapers import AnimeScrapers, TopScrapers


class TopParameters(BaseModel):
    type: str = Query(...)
    page_number: int = Query(..., gt=0)

    @validator("type")
    def validate_type(cls, v: str) -> str:
        if v not in TopScrapers.anime_types():
            raise InvalidParameter("type")

        return v


class AnimeParameters(BaseModel):
    mal_id: int = Query(..., gt=0)
    mal_request: str = Query(...)
    page_number: int = Query(None, gt=0)

    @root_validator
    def validate_root(cls, values: dict) -> dict:
        mal_request = values.get("mal_request", "")
        methods = getmembers(AnimeScrapers, iscoroutinefunction)

        if not any(
            (method_name, method)
            for method_name, method in methods
            if method_name == mal_request
        ):
            raise InvalidParameter("mal_request")

        page_number = values.get("page_number")

        if mal_request not in ("episodes", "reviews") and page_number:
            raise InvalidParameter("page_number")
        elif mal_request in ("episodes", "reviews") and not page_number:
            raise MissingParameter("page_number")

        return values


class AnimeSearchParameters(BaseModel):
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

    @root_validator
    def validate_root(cls, values: dict) -> dict:
        for k, v in values.items():
            if k in ["query", "genres", "columns"]:
                continue

            if v is None:
                values[k] = 0

        return values
