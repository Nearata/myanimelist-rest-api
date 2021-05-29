from datetime import datetime, timedelta
from json import dumps

from bs4 import BeautifulSoup
from httpx import AsyncClient
from orm.models import QuerySet
from starlette.requests import Request

from .config import USER_AGENT
from .database import Cache


class CacheUtil:
    def query(self, cache_key: str) -> QuerySet:
        return Cache.objects.filter(id=cache_key)

    async def save(self, cache_key: str, json: dict) -> None:
        await Cache.objects.create(
            id=cache_key,
            json=dumps(json),
            expire=datetime.utcnow().date() + timedelta(weeks=1),
        )

    def is_expired(self, cache: Cache) -> bool:
        return datetime.utcnow().date() >= cache.expire


class SoupUtil:
    def __init__(self, session: AsyncClient) -> None:
        self.session = session

    async def get_soup(self, url: str, params: dict = None) -> BeautifulSoup:
        response = await self.session.get(
            url, params=params, headers={"User-Agent": USER_AGENT}
        )

        return BeautifulSoup(response.content, "html5lib")


def get_cache_key(request: Request) -> str:
    path = request.url.path.strip("/")
    mal_id = request.query_params.get("mal_id")
    mal_request = request.query_params.get("mal_request")
    page = request.query_params.get("page_number", "")

    return f"{path}{mal_id}{mal_request}{page}"
