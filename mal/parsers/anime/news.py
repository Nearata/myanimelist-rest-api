from re import search
from typing import Optional

from bs4 import BeautifulSoup


class News:
    def __init__(self, soup: BeautifulSoup, base_url: str) -> None:
        self.soup = soup
        self.base_url = base_url

    def __call__(self) -> dict:
        return {
            "data": [
                {
                    "url": f"{self.base_url}{i.select_one('a').get('href')}".strip(),
                    "imageUrl": i.select_one("img").get("data-src")
                    if i.select_one("img")
                    else None,
                    "title": i.select_one(".spaceit > a > strong").get_text(),
                    "content": i.select_one(
                        ".clearfix > .clearfix > p > a"
                    ).previous_sibling.strip(),
                    "author": i.select_one(".lightLink > a:first-child").get_text(),
                    "authorProfile": f"{self.base_url}{i.select_one('.lightLink > a:first-child').get('href')}".strip(),
                    "comments": self.__comments(
                        i.select_one(".lightLink > a:last-child").get_text()
                    ),
                    "forumUrl": f"{self.base_url}{i.select_one('.lightLink > a:last-child').get('href')}".strip(),
                }
                for i in self.soup.select(".js-scrollfix-bottom-rel > .clearfix")
            ]
        }

    def __comments(self, string: str) -> Optional[int]:
        regex = search(r"\d+", string)
        return int(regex.group()) if regex else None
