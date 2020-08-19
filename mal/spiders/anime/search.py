from datetime import datetime
from re import match
from mal.spiders.soup import Soup


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

        soup = Soup("https://myanimelist.net/anime.php", params=params)
        selector = soup.get().select_one(".js-categories-seasonal")

        columns_enabled = {}
        check_columns_helper = lambda **kwargs: {kwargs["dict_key"]: kwargs["index"]} if kwargs["letter"] in columns_lst and kwargs["soup"].find(string=kwargs["find_string"]) else {}
        for index, i in enumerate(selector.select_one("tr:first-child").select("td"), 1):
            columns_enabled.update(check_columns_helper(letter="a", soup=i, find_string="Type", index=index, dict_key="type"))
            columns_enabled.update(check_columns_helper(letter="b", soup=i, find_string="Eps.", index=index, dict_key="episodes"))
            columns_enabled.update(check_columns_helper(letter="c", soup=i, find_string="Score", index=index, dict_key="score"))
            columns_enabled.update(check_columns_helper(letter="d", soup=i, find_string="Start Date", index=index, dict_key="start_date"))
            columns_enabled.update(check_columns_helper(letter="e", soup=i, find_string="End Date", index=index, dict_key="end_date"))
            columns_enabled.update(check_columns_helper(letter="f", soup=i, find_string="Members", index=index, dict_key="members"))
            columns_enabled.update(check_columns_helper(letter="g", soup=i, find_string="Rated", index=index, dict_key="rated"))

        results = []
        for i in selector.select("tr:not(:first-child)"):
            anime = {
                "mal_id": int(i.select_one("td:nth-child(2)>div>div").get("rel").replace("a", "")),
                "url": i.select_one("td:nth-child(1)>.picSurround>a").get("href"),
                "image_url": i.select_one("td:nth-child(1)>.picSurround>a>img").get("data-src").replace("r/50x70/", ""),
                "title": i.select_one("td:nth-child(2)>a>strong").get_text()
            }

            column_enabled_soup = lambda soup, key: soup.select_one(f"td:nth-child({columns_enabled[key]})").get_text(strip=True)
            for k in columns_enabled.keys():
                if k == "type":
                    anime.update({"type": column_enabled_soup(i, k)})
                if k == "episodes":
                    anime.update({"episodes": self.__episodes(column_enabled_soup(i, k))})
                if k == "score":
                    anime.update({"score": self.__score(column_enabled_soup(i, k))})
                if k == "start_date":
                    date = column_enabled_soup(i, k).replace("??", "01")
                    anime.update({"start_date": str(datetime.strptime(date, "%m-%d-%y").date())} if len(date) > 1 else {})
                if k == "end_date":
                    date = column_enabled_soup(i, k).replace("??", "01")
                    anime.update({"end_date": str(datetime.strptime(date, "%m-%d-%y").date())} if len(date) > 1 else {})
                if k == "members":
                    anime.update({"members": int(column_enabled_soup(i, k).replace(",", ""))})
                if k == "rated":
                    anime.update({"rated": column_enabled_soup(i, k)})

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
