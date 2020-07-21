from re import match
from re import search
from mal.spiders.utils import get_soup


class Top:
    def __init__(self, base_url, _type, page) -> None:
        self.base_url = base_url
        self.type = _type
        self.page = page

    def get(self):
        params = {}
        if self.type != "all":
            params["type"] = self.type

        if self.page == 1:
            params["limit"] = 0
        elif self.page == 2:
            params["limit"] = 50
        else:
            params["limit"] = 50 * self.page - 50

        selector = get_soup(f"{self.base_url}/topanime.php", params=params).select(".top-ranking-table tr:not(:first-child)")
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

    def __type(self, string):
        regex = match(r"(TV|Movie|OVA|ONA|Music|Special)", string)
        if regex:
            return regex.group()
        return None

    def __digits(self, string):
        regex = search(r"\d+", string.replace(",", ""))
        if regex:
            return int(regex.group())
        return None

    def __score(self, string):
        regex = match(r"\d.\d+", string)
        if regex:
            return float(regex.group())
        return None