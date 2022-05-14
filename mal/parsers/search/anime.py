from datetime import datetime
from re import findall, match, search
from typing import Any, Optional

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

        if self.columns:
            columns_lst = self.columns.replace(" ", "").split(",")
            params.update({f"c[{i}]": i for i in columns_lst})
        else:
            params.update({"c": 0})

        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime.php", params=params)

        data: list[dict[str, Any]] = []

        elements = soup.find(string="Search Results")
        if (
            elements
            and (parent := elements.parent)
            and (sibling := parent.find_next_sibling())
            and (rows := sibling.select("table tr"))
        ):
            mappings: dict[str, str] = {}

            for index, r in enumerate(rows[0].select("td")):
                mappings.update({f"{index}": r.get_text().strip()})

            for r in rows[1:]:
                obj: dict[str, Any] = {}

                for index, c in enumerate(r.select("td")):
                    if mappings.get(f"{index}", "") == "" and (
                        picture := c.find_next("img")
                    ):
                        obj.update(
                            {
                                "pictureUrl": self.__format_picture(
                                    picture.get("data-src")
                                ),
                                "id": int(malid.group())
                                if (
                                    (picture_parent := picture.find_parent("a"))
                                    and (
                                        malid := search(
                                            r"\d+", picture_parent.get("href")
                                        )
                                    )
                                )
                                else None,
                            }
                        )

                    if mappings.get(f"{index}", "") == "Title" and (
                        title := c.find_next(attrs={"class", "title"})
                    ):
                        obj.update(
                            {
                                "title": title_found.get_text().strip()
                                if (title_found := title.find_next("strong"))
                                else None
                            }
                        )

                    if mappings.get(f"{index}", "") == "Type":
                        obj.update({"type": c.get_text().strip()})

                    if mappings.get(f"{index}", "") == "Eps.":
                        obj.update(
                            {
                                "episodes": int(episodes.group())
                                if (episodes := match(r"\d+", c.get_text().strip()))
                                else None
                            }
                        )

                    if mappings.get(f"{index}", "") == "Score":
                        obj.update(
                            {
                                "score": float(score.group())
                                if (score := match(r"\d\.\d+", c.get_text().strip()))
                                else None
                            }
                        )

                    if mappings.get(f"{index}", "") == "Start Date":
                        obj.update(
                            {
                                "startDate": str(
                                    datetime.strptime(
                                        start_date.group(), "%m-%d-%y"
                                    ).date()
                                )
                                if (
                                    start_date := match(
                                        r"\d+\-\d+\-\d+", c.get_text().strip()
                                    )
                                )
                                else None
                            }
                        )

                    if mappings.get(f"{index}", "") == "End Date":
                        obj.update(
                            {
                                "endDate": str(
                                    datetime.strptime(
                                        end_date.group(), "%m-%d-%y"
                                    ).date()
                                )
                                if (
                                    end_date := match(
                                        r"\d+\-\d+\-\d+", c.get_text().strip()
                                    )
                                )
                                else None
                            }
                        )

                    if mappings.get(f"{index}", "") == "Members":
                        obj.update(
                            {
                                "members": int("".join(members))
                                if (members := findall(r"\d+", c.get_text().strip()))
                                else None
                            }
                        )

                    if mappings.get(f"{index}", "") == "Rated":
                        obj.update({"rated": c.get_text().strip()})

                data.append(obj)

        return {"data": data}

    def __format_picture(self, string: str) -> Optional[str]:
        if not string:
            return None

        l: list[str] = findall(
            r"(https:\/\/cdn.myanimelist.net)|(\/images\/anime\/\d+\/\d+.\w+)", string
        )

        if not l:
            return None

        if not isinstance(l[0], tuple):
            return None

        return "".join(i for sub in l for i in sub if not i.isspace())
