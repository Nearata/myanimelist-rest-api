from bs4 import BeautifulSoup
from requests import Session

from mal.utils import RequestsUtil


class SoupUtil:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_soup(self, url: str, params: dict = None) -> BeautifulSoup:
        response = self.session.get(url, params=params, headers=RequestsUtil.HEADERS)

        return BeautifulSoup(response.content, "html5lib")
