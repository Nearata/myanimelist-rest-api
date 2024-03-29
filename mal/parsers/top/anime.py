from re import match, search
from typing import Optional

from bs4 import BeautifulSoup


class TopAnimeParser:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def __call__(self) -> dict:
        return {
            "data": [
                {
                    "rank": int(i.select_one("td.rank>span").get_text()),
                    "malId": int(
                        i.select_one("td.title>a").get("id").replace("#area", "")
                    ),
                    "url": i.select_one("td.title>a").get("href"),
                    "imageUrl": i.select_one("td.title>a>img")
                    .get("data-src")
                    .replace("r/50x70/", ""),
                    "title": i.select_one("td.title>.detail h3").get_text(),
                    "type": self.__type(
                        i.select_one(
                            "td.title>.detail>.information>br:first-child"
                        ).previous_sibling.strip()
                    ),
                    "episodes": self.__digits(
                        i.select_one(
                            "td.title>.detail>.information>br:first-child"
                        ).previous_sibling.strip()
                    ),
                    "members": self.__digits(
                        i.select_one(
                            "td.title>.detail>.information>br:last-child"
                        ).next_sibling.strip()
                    ),
                    "score": self.__score(i.select_one("td.score>div>span").get_text()),
                }
                for i in self.soup.select(".top-ranking-table .ranking-list")
            ]
        }

    def __type(self, string: str) -> Optional[str]:
        regex = match(r"(TV|Movie|OVA|ONA|Music|Special)", string)
        return str(regex.group()) if regex else None

    def __digits(self, string: str) -> Optional[int]:
        regex = search(r"\d+", string.replace(",", ""))
        return int(regex.group()) if regex else None

    def __score(self, string: str) -> Optional[float]:
        regex = match(r"\d.\d+", string)
        return float(regex.group()) if regex else None
