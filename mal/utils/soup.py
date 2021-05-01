from bs4 import BeautifulSoup
from httpx import AsyncClient

from .requests import RequestsUtil


class SoupUtil:
    def __init__(self, session: AsyncClient) -> None:
        self.session = session

    async def get_soup(self, url: str, params: dict = None) -> BeautifulSoup:
        response = await self.session.get(
            url, params=params, headers=RequestsUtil.HEADERS
        )

        return BeautifulSoup(response.content, "html5lib")
