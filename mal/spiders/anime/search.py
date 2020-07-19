from datetime import datetime
from re import match
from mal.spiders.utils import get_soup


class Search:
    def __init__(self, **kargs) -> None:
        self.query = kargs["query"]
        self.type = kargs["type"]
        self.score = kargs["score"]
        self.status = kargs["status"]
        self.producer = kargs["producer"]
        self.rated = kargs["rated"]
        self.start_month = kargs["start_month"]
        self.start_day = kargs["start_day"]
        self.start_year = kargs["start_year"]
        self.end_month = kargs["end_month"]
        self.end_day = kargs["end_day"]
        self.end_year = kargs["end_year"]
        self.genres = kargs["genres"]
        self.genres_exclude = kargs["genres_exclude"]
        self.columns = kargs["columns"]

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
            for i in self.genres.split(","):
                params[f"genre[{i}]"] = i

        columns_lst = []
        if self.columns:
            columns_lst = self.columns.split(",")
            for i in columns_lst:
                params[f"c[{i}]"] = i
        else:
            params[f"c"] = 0

        soup = get_soup("https://myanimelist.net/anime.php", params=params)
        selector = soup.select_one(".js-categories-seasonal")

        results = []

        type_index = None
        eps_index = None
        score_index = None
        s_d_index = None
        e_d_index = None
        members_index = None
        rated_index = None

        for index, i in enumerate(selector.select_one("tr:first-child").select("td"), 1):
            if "a" in columns_lst and i.find(string="Type"):
                type_index = index
            if "b" in columns_lst and i.find(string="Eps."):
                eps_index = index
            if "c" in columns_lst and i.find(string="Score"):
                score_index = index
            if "d" in columns_lst and i.find(string="Start Date"):
                s_d_index = index
            if "e" in columns_lst and i.find(string="End Date"):
                e_d_index = index
            if "f" in columns_lst and i.find(string="Members"):
                members_index = index
            if "g" in columns_lst and i.find(string="Rated"):
                rated_index = index

        for i in selector.select("tr:not(:first-child)"):
            anime = {}
            anime["mal_id"] = int(i.select_one("td:nth-child(2)>div>div").get("rel").replace("a", ""))
            anime["url"] = i.select_one("td:nth-child(1)>.picSurround>a").get("href")
            anime["image_url"] = i.select_one("td:nth-child(1)>.picSurround>a>img").get("data-src").replace("r/50x70/", "")
            anime["title"] = i.select_one("td:nth-child(2)>a>strong").get_text()
            if type_index:
                anime["type"] = i.select_one(f"td:nth-child({type_index})").get_text(strip=True)
            if eps_index:
                anime["episodes"] = self.__episodes(i.select_one(f"td:nth-child({eps_index})").get_text(strip=True))
            if score_index:
                anime["score"] = self.__score(i.select_one(f"td:nth-child({score_index})").get_text(strip=True))
            if s_d_index:
                date = i.select_one(f"td:nth-child({s_d_index})").get_text(strip=True).replace("??", "01")
                if not len(date) <= 1:
                    anime["start_date"] = str(datetime.strptime(date, "%m-%d-%y").date())
                else:
                    anime["start_date"] = None
            if e_d_index:
                date = i.select_one(f"td:nth-child({e_d_index})").get_text(strip=True).replace("??", "01")
                if not len(date) <= 1:
                    anime["end_date"] = str(datetime.strptime(date, "%m-%d-%y").date())
                else:
                    anime["end_date"] = None
            if members_index:
                anime["members"] = int(i.select_one(f"td:nth-child({members_index})").get_text(strip=True).replace(",", ""))
            if rated_index:
                anime["rated"] = i.select_one(f"td:nth-child({rated_index})").get_text(strip=True)

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
