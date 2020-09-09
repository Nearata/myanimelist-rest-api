from re import match, search
from bs4 import BeautifulSoup


class Top:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def get(self) -> dict:
        selector = self.soup.select(".top-ranking-table tr:not(:first-child)")
        return {
            "top": [
                {
                    "rank": int(i.select_one("td.rank>span").get_text()),
                    "mal_id": int(i.select_one("td.title>a").get("id").replace("#area", "")),
                    "url": i.select_one("td.title>a").get("href"),
                    "image_url": i.select_one("td.title>a>img").get("data-src").replace("r/50x70/", ""),
                    "title": i.select_one("td.title>.detail>.di-ib>a").get_text(),
                    "type": self.__type(i.select_one("td.title>.detail>.information>br:first-child").previous_sibling.strip()),
                    "episodes": self.__digits(i.select_one("td.title>.detail>.information>br:first-child").previous_sibling.strip()),
                    "members": self.__digits(i.select_one("td.title>.detail>.information>br:last-child").next_sibling.strip()),
                    "score": self.__score(i.select_one("td.score>div>span").get_text())
                } for i in selector
            ]
        }

    def __type(self, string: str) -> str:
        regex = match(r"(TV|Movie|OVA|ONA|Music|Special)", string)
        if not regex:
            return None
        return regex.group()

    def __digits(self, string: str) -> int:
        regex = search(r"\d+", string.replace(",", ""))
        if not regex:
            return None
        return int(regex.group())

    def __score(self, string: str) -> float:
        regex = match(r"\d.\d+", string)
        if not regex:
            return None
        return float(regex.group())
