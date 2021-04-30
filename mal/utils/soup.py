from bs4 import BeautifulSoup
from httpx import Client

from .requests import RequestsUtil


class SoupUtil:
    def __init__(self, session: Client) -> None:
        self.session = session

    def get_soup(self, url: str, params: dict = None) -> BeautifulSoup:
        response = self.session.get(url, params=params, headers=RequestsUtil.HEADERS)

        return BeautifulSoup(response.content, "html5lib")
