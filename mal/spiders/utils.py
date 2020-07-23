from bs4 import BeautifulSoup
from falcon import HTTPNotFound
from requests import Session

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
}


def get_soup(url, params=None, parser="lxml"):
    with Session() as s:
        result = s.get(url, params=params, headers=headers)
    page_source = result.content

    return BeautifulSoup(page_source, parser)
