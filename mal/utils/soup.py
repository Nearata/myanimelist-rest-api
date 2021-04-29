from bs4 import BeautifulSoup
from requests import Session

from mal.utils import RequestsUtil


class SoupUtil:
    @staticmethod
    def get_soup(url: str, params: dict = None) -> BeautifulSoup:
        with Session() as s:
            response = s.get(url, params=params, headers=RequestsUtil.HEADERS)

        return BeautifulSoup(response.content, "html5lib")
