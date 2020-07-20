from datetime import datetime
from re import match
from mal.spiders.utils import get_soup


class Search:
    def __init__(self, **kwargs) -> None:
        self.query = kwargs["query"]
        self.type = kwargs["type"]
        self.score = kwargs["score"]
        self.status = kwargs["status"]
        self.producer = kwargs["producer"]
        self.rated = kwargs["rated"]
        self.start_month = kwargs["start_month"]
        self.start_day = kwargs["start_day"]
        self.start_year = kwargs["start_year"]
        self.end_month = kwargs["end_month"]
        self.end_day = kwargs["end_day"]
        self.end_year = kwargs["end_year"]
        self.genres = kwargs["genres"]
        self.genres_exclude = kwargs["genres_exclude"]
        self.columns = kwargs["columns"]

    def get(self):
        params = {
            "q": self.query,
            "type": self.type,
            "score": self.score,
            "status": self.status,
            "p": self.producer,
            "r": self.rated,
            "sy": self.start_year,
            "sm": self.start_month,
            "sd": self.start_day,
            "ey": self.end_year,
            "em": self.end_month,
            "ed": self.end_day,
            "gx": self.genres_exclude
        }

        if self.genres:
            params.update({f"genre[{i}]":i for i in self.genres.split(",")})

        columns_lst = []
        if self.columns:
            columns_lst = self.columns.split(",")
            params.update({f"c[{i}]":i for i in self.columns.split(",")})
        else:
            params.update({"c":0})

        selector = get_soup("https://myanimelist.net/anime.php", params=params).select_one(".js-categories-seasonal")

        columns_enabled = {}
        for index, i in enumerate(selector.select_one("tr:first-child").select("td"), 1):
            columns_enabled.update({"type": index} if "a" in columns_lst and i.find(string="Type") else {})
            columns_enabled.update({"episodes": index} if "b" in columns_lst and i.find(string="Eps.") else {})
            columns_enabled.update({"score": index} if "c" in columns_lst and i.find(string="Score") else {})
            columns_enabled.update({"start_date": index} if "d" in columns_lst and i.find(string="Start Date") else {})
            columns_enabled.update({"end_date": index} if "e" in columns_lst and i.find(string="End Date") else {})
            columns_enabled.update({"members": index} if "f" in columns_lst and i.find(string="Members") else {})
            columns_enabled.update({"rated": index} if "g" in columns_lst and i.find(string="Rated") else {})

        results = []
        for i in selector.select("tr:not(:first-child)"):
            anime = {
                "mal_id": int(i.select_one("td:nth-child(2)>div>div").get("rel").replace("a", "")),
                "url": i.select_one("td:nth-child(1)>.picSurround>a").get("href"),
                "image_url": i.select_one("td:nth-child(1)>.picSurround>a>img").get("data-src").replace("r/50x70/", ""),
                "title": i.select_one("td:nth-child(2)>a>strong").get_text()
            }

            for k in columns_enabled.keys():
                if k == "type":
                    anime.update({"type": i.select_one(f"td:nth-child({columns_enabled[k]})").get_text(strip=True)})
                if k == "episodes":
                    anime.update({"episodes": self.__episodes(i.select_one(f"td:nth-child({columns_enabled[k]})").get_text(strip=True))})
                if k == "score":
                    anime.update({"score": self.__score(i.select_one(f"td:nth-child({columns_enabled[k]})").get_text(strip=True))})
                if k == "start_date":
                    date = i.select_one(f"td:nth-child({columns_enabled[k]})").get_text(strip=True).replace("??", "01")
                    anime.update({"start_date": str(datetime.strptime(date, "%m-%d-%y").date())} if len(date) > 1 else {})
                if k == "end_date":
                    date = i.select_one(f"td:nth-child({columns_enabled[k]})").get_text(strip=True).replace("??", "01")
                    anime.update({"end_date": str(datetime.strptime(date, "%m-%d-%y").date())} if len(date) > 1 else {})
                if k == "members":
                    anime.update({"members": int(i.select_one(f"td:nth-child({columns_enabled[k]})").get_text(strip=True).replace(",", ""))})
                if k == "rated":
                    anime.update({"rated": i.select_one(f"td:nth-child({columns_enabled[k]})").get_text(strip=True)})

            results.append(anime)

        return {
            "results": results
        }

    def __episodes(self, string):
        regex = match(r"\d+", string)
        if regex:
            return int(regex.group())
        return None

    def __score(self, string):
        regex = match(r"\d\.\d+", string)
        if regex:
            return float(regex.group())
        return None
