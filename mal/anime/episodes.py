from datetime import datetime
from re import findall, match, sub
from bs4 import BeautifulSoup


class Episodes:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def get(self) -> dict:
        selector = self.soup.select("table.ascend .episode-list-data")
        episode_title = ".episode-title > span"
        return {
            "episodes": [
                {
                    "title": i.select_one(".episode-title > a").get_text(),
                    "title_romanji": self.__title_romanji(i.select_one(episode_title).get_text()),
                    "title_japanese": self.__title_japanese(i.select_one(episode_title).get_text()),
                    "number": self.__number(i.select_one("td.episode-number").get_text()),
                    "aired": self.__aired(i.select_one("td.episode-aired").get_text()),
                    "filler": self.__filler_recap(i.select_one(episode_title).get_text()),
                    "recap": self.__filler_recap(i.select_one(episode_title).get_text())
                } for i in selector
            ]
        }

    def __title_romanji(self, string: str) -> str:
        regex = sub(r"\s\(.*?\)", "", string)
        if regex:
            return regex
        return None

    def __title_japanese(self, string: str) -> str:
        pattern = r"[^a-zA-Z!-@#$%^&*(),.?\":{}|<>\s].*[^)]"
        regex = findall(pattern, string)
        if regex:
            return "".join(regex)
        return None

    def __number(self, string: str) -> int:
        regex = match(r"\d+", string)
        if regex:
            return int(regex.group())
        return None

    def __aired(self, string: str) -> str:
        regex = match(
            r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s?(\d{1,2})?(,)\s(\d{4})",
            string
        )
        if regex:
            return str(datetime.strptime(regex.group(), "%b %d, %Y").date())
        return None

    def __filler_recap(self, string: str) -> bool:
        regex = match(r"(filler|recap)", string.lower())
        if regex:
            return True
        return False
