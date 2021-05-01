from datetime import datetime
from re import findall, match, sub
from typing import Union

from bs4 import BeautifulSoup
from bs4.element import Tag


class Episodes:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def __call__(self) -> dict:
        episode_title = ".episode-title > span"
        return {
            "links": self.__links(),
            "episodes": [
                {
                    "title": i.select_one(".episode-title > a").get_text(),
                    "title_romanji": self.__title_romanji(
                        i.select_one(episode_title).get_text()
                    ),
                    "title_japanese": self.__title_japanese(
                        i.select_one(episode_title).get_text()
                    ),
                    "number": self.__number(
                        i.select_one("td.episode-number").get_text()
                    ),
                    "aired": self.__aired(i.select_one("td.episode-aired").get_text()),
                    "filler": self.__filler_recap(
                        i.select_one(episode_title).get_text()
                    ),
                    "recap": self.__filler_recap(
                        i.select_one(episode_title).get_text()
                    ),
                }
                for i in self.soup.select("table.ascend .episode-list-data")
            ],
        }

    def __title_romanji(self, string: str) -> Union[str, None]:
        regex = sub(r"\s\(.*?\)", "", string)
        return str(regex) if regex else None

    def __title_japanese(self, string: str) -> Union[str, None]:
        pattern = r"[^a-zA-Z!-@#$%^&*(),.?\":{}|<>\s].*[^)]"
        regex = findall(pattern, string)
        return "".join(regex) if regex else None

    def __number(self, string: str) -> Union[int, None]:
        regex = match(r"\d+", string)
        return int(regex.group()) if regex else None

    def __aired(self, string: str) -> Union[str, None]:
        regex = match(
            r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s?(\d{1,2})?(,)\s(\d{4})",
            string,
        )
        return (
            str(datetime.strptime(regex.group(), "%b %d, %Y").date()) if regex else None
        )

    def __filler_recap(self, string: str) -> bool:
        regex = match(r"(filler|recap)", string.lower())
        return True if regex else False

    def __links(self) -> dict:
        pagination = self.soup.select_one(".pagination")

        links = {"hasPrevious": False, "hasNext": False}

        if not pagination:
            return links

        tag: Tag = pagination.select_one(".link.current")

        if not tag:
            return {}

        if tag.previous_sibling:
            links.update({"hasPrevious": True})

        if tag.next_sibling:
            links.update({"hasNext": True})

        return links
