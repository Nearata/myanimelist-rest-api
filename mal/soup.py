from bs4 import BeautifulSoup
from requests import Session
from mal.utils import Utils


class Soup:
    def __init__(self, url: str, params: dict = None, parser: str = "lxml") -> None:
        self.url = url
        self.params = params
        self.parser = parser

    def __call__(self) -> BeautifulSoup:
        with Session() as s:
            response = s.get(self.url, params=self.params, headers=Utils.REQUESTS_HEADERS)

        return BeautifulSoup(response.content, self.parser)
