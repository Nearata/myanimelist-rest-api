from re import match
from typing import Any, Optional

from bs4 import BeautifulSoup

from ...const import MAL_URL
from ...utils import SoupUtil


class SearchAnimeParser:
    def __init__(self, soup_util: SoupUtil, **kwargs: Any) -> None:
        self.soup_util = soup_util
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

    async def __call__(self) -> dict:
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
            "gx": self.genres_exclude,
        }

        if self.genres:
            params.update({f"genre[{i}]": i for i in self.genres.split(",")})

        columns_lst = []
        if self.columns:
            columns_lst = self.columns.replace(" ", "").split(",")
            params.update({f"c[{i}]": i for i in columns_lst})
        else:
            params.update({"c": 0})

        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime.php", params=params)
        selector = soup.select_one(".js-categories-seasonal")
        if selector is None:
            return {"results": "There are no results."}

        columns_enabled = {}
        for index, i in enumerate(
            selector.select_one("tr:first-child").select("td"), 1
        ):
            columns_enabled.update(
                self.__columns_helper(
                    columns=columns_lst,
                    letter="a",
                    soup=i,
                    find_string="Type",
                    index=index,
                    dict_key="type",
                )
            )
            columns_enabled.update(
                self.__columns_helper(
                    columns=columns_lst,
                    letter="b",
                    soup=i,
                    find_string="Eps.",
                    index=index,
                    dict_key="episodes",
                )
            )
            columns_enabled.update(
                self.__columns_helper(
                    columns=columns_lst,
                    letter="c",
                    soup=i,
                    find_string="Score",
                    index=index,
                    dict_key="score",
                )
            )
            columns_enabled.update(
                self.__columns_helper(
                    columns=columns_lst,
                    letter="d",
                    soup=i,
                    find_string="Start Date",
                    index=index,
                    dict_key="start_date",
                )
            )
            columns_enabled.update(
                self.__columns_helper(
                    columns=columns_lst,
                    letter="e",
                    soup=i,
                    find_string="End Date",
                    index=index,
                    dict_key="end_date",
                )
            )
            columns_enabled.update(
                self.__columns_helper(
                    columns=columns_lst,
                    letter="f",
                    soup=i,
                    find_string="Members",
                    index=index,
                    dict_key="members",
                )
            )
            columns_enabled.update(
                self.__columns_helper(
                    columns=columns_lst,
                    letter="g",
                    soup=i,
                    find_string="Rated",
                    index=index,
                    dict_key="rated",
                )
            )

        results = []
        for i in selector.select("tr:not(:first-child)"):
            anime = {
                "mal_id": int(
                    i.select_one("td:nth-child(2)>div>div").get("rel").replace("a", "")
                ),
                "url": i.select_one("td:nth-child(1)>.picSurround>a").get("href"),
                "image_url": i.select_one("td:nth-child(1)>.picSurround>a>img")
                .get("data-src")
                .replace("r/50x70/", ""),
                "title": i.select_one("td:nth-child(2)>a>strong").get_text(),
            }

            for k in columns_enabled.keys():
                if k == "type":
                    anime.update(
                        {"type": self.__column_enabled_soup(columns_enabled, i, k)}
                    )
                if k == "episodes":
                    anime.update(
                        {
                            "episodes": self.__episodes(
                                self.__column_enabled_soup(columns_enabled, i, k)
                            )
                        }
                    )
                if k == "score":
                    anime.update(
                        {
                            "score": self.__score(
                                self.__column_enabled_soup(columns_enabled, i, k)
                            )
                        }
                    )
                if k == "start_date":
                    date = self.__column_enabled_soup(columns_enabled, i, k).replace(
                        "??", "01"
                    )
                    anime.update({"start_date": date} if len(date) > 1 else {})
                if k == "end_date":
                    date = self.__column_enabled_soup(columns_enabled, i, k).replace(
                        "??", "01"
                    )
                    anime.update({"end_date": date} if len(date) > 1 else {})
                if k == "members":
                    anime.update(
                        {
                            "members": int(
                                self.__column_enabled_soup(
                                    columns_enabled, i, k
                                ).replace(",", "")
                            )
                        }
                    )
                if k == "rated":
                    anime.update(
                        {"rated": self.__column_enabled_soup(columns_enabled, i, k)}
                    )

            results.append(anime)

        return {"data": results}

    def __columns_helper(self, **kwargs: Any) -> dict:
        return (
            {kwargs["dict_key"]: kwargs["index"]}
            if kwargs["letter"] in kwargs["columns"]
            and kwargs["soup"].find(string=kwargs["find_string"])
            else {}
        )

    def __column_enabled_soup(
        self, columns_enabled: dict, soup: BeautifulSoup, key: str
    ) -> str:
        return str(
            soup.select_one(f"td:nth-child({columns_enabled[key]})").get_text(
                strip=True
            )
        )

    def __episodes(self, string: str) -> Optional[int]:
        regex = match(r"\d+", string)
        return int(regex.group()) if regex else None

    def __score(self, string: str) -> Optional[float]:
        regex = match(r"\d\.\d+", string)
        return float(regex.group()) if regex else None
