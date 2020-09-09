from re import match
from bs4 import BeautifulSoup


class Clubs:
    def __init__(self, soup: BeautifulSoup, base_url: str) -> None:
        self.soup = soup
        self.base_url = base_url

    def __call__(self) -> dict:
        selector = self.soup.find_all("div", {"class": "borderClass"})
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
