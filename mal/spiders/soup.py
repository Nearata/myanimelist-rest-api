from bs4 import BeautifulSoup
from requests import Session


class Soup:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
    }

    def __init__(self, url: str, params: dict = None, parser: str = "lxml") -> None:
        self.url = url
        self.params = params
        self.parser = parser

    def get(self) -> BeautifulSoup:
        with Session() as s:
            response = s.get(self.url, params=self.params, headers=self.headers)

        return BeautifulSoup(response.content, self.parser)
