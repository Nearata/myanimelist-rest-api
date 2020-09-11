from bs4 import BeautifulSoup
from requests import Session
from mal.utils import RequestsUtil


class SoupUtil:
    def __init__(self, url: str, params: dict = None, parser: str = "lxml") -> None:
        self.url = url
        self.params = params
        self.parser = parser

    def __call__(self) -> BeautifulSoup:
        with Session() as s:
            response = s.get(self.url, params=self.params, headers=RequestsUtil.HEADERS)

        return BeautifulSoup(response.content, self.parser)
