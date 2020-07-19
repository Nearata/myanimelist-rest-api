from datetime import datetime
from re import findall, match, sub
from mal.spiders.utils import get_soup


class Episodes:
    def __init__(self, base_url, mal_id, page_number) -> None:
        self.base_url = base_url
        self.mal_id = mal_id
        self.page_number = page_number

    def get(self):
        episode_title = ".episode-title > span"
        page_url = f"{self.base_url}/anime/{self.mal_id}/_/episode" if self.page_number == 1 else f"{self.base_url}/anime/{self.mal_id}/_/episode?offset={self.page_number}00"
        selector = get_soup(page_url).select("table.ascend .episode-list-data")
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

    def __title_romanji(self, string):
        regex = sub(r"\s\(.*?\)", "", string)
        if regex:
            return regex
        return None

    def __title_japanese(self, string):
        pattern = r"[^a-zA-Z!-@#$%^&*(),.?\":{}|<>\s].*[^)]"
        regex = findall(pattern, string)
        if regex:
            return "".join(regex)
        return None

    def __number(self, string):
        regex = match(r"\d+", string)
        if regex:
            return int(regex.group())
        return None

    def __aired(self, string):
        regex = match(
            r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s?(\d{1,2})?(,)\s(\d{4})",
            string
        )
        if regex:
            return str(datetime.strptime(regex.group(), "%b %d, %Y").date())
        return None

    def __filler_recap(self, string):
        regex = match(r"(filler|recap)", string.lower())
        if regex:
            return True
        return False
