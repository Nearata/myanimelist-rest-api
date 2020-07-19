from re import match
from mal.spiders.utils import get_soup


class Clubs:
    def __init__(self, base_url, mal_id) -> None:
        self.base_url = base_url
        self.mal_id = mal_id

    def get(self):
        selector = get_soup(f"{self.base_url}/anime/{self.mal_id}/_/clubs").select(".js-scrollfix-bottom-rel > .borderClass")
        return {
            "clubs": [
                {
                    "name": i.select_one("a").get_text(strip=True),
                    "url": f"{self.base_url}{i.select_one('a').get('href')}",
                    "members": self.__members(i.select_one("small").get_text())
                } for i in selector
            ]
        }

    def __members(self, string):
        regex = match(r"\d+", string)
        if regex:
            return int(regex.group())
        return None
