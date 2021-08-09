from datetime import datetime
from re import match
from typing import Optional, Union

from bs4 import BeautifulSoup

from ._helpers import AnimeHelpers


class Details:
    none_found = "none found"

    def __init__(self, soup: BeautifulSoup, base_url: str) -> None:
        self.soup = soup
        self.base_url = base_url

    def __call__(self) -> dict:
        anime_title: str = self.soup.select_one("h1.title-name").get_text()
        image = self.__get_image(anime_title)

        return {
            "data": {
                "title": anime_title,
                "image": image,
                "trailer": AnimeHelpers.trailer_helper(self.soup),
                "synopsis": AnimeHelpers.synopsis_helper(self.soup),
                "background": AnimeHelpers.background_helper(self.soup),
                "alternativeTitles": {
                    "english": self.__alternative_titles_helper("English:"),
                    "japanese": self.__alternative_titles_helper("Japanese:"),
                    "synonyms": AnimeHelpers.synonyms_helper(self.soup),
                },
                "information": {
                    "type": self.soup.find("span", string="Type:")
                    .find_next_sibling("a")
                    .get_text(),
                    "episodes": AnimeHelpers.episodes_helper(self.soup),
                    "status": self.soup.find(
                        "span", string="Status:"
                    ).next_sibling.strip(),
                    "aired": {
                        "from": self.__information_aired_helper("from"),
                        "to": self.__information_aired_helper("to"),
                    },
                    "premiered": AnimeHelpers.premiered_helper(self.soup),
                    "producers": AnimeHelpers.producers_helper(
                        self.soup, self.none_found, self.base_url
                    ),
                    "licensors": AnimeHelpers.licensors_helper(
                        self.soup, self.none_found, self.base_url
                    ),
                    "studios": AnimeHelpers.studios_helper(
                        self.soup, self.none_found, self.base_url
                    ),
                    "source": self.__alternative_titles_helper("Source:"),
                    "genres": AnimeHelpers.genres_helper(self.soup),
                    "duration": AnimeHelpers.duration_helper(self.soup),
                    "rating": AnimeHelpers.rating_helper(self.soup),
                },
                "statistics": {
                    "score": AnimeHelpers.score_helper(self.soup),
                    "ranked": self.__statistics_helper("Ranked:", "#"),
                    "popularity": self.__statistics_helper("Popularity:", "#"),
                    "members": self.__statistics_helper("Members:"),
                    "favorites": self.__statistics_helper("Favorites:"),
                },
                "related_anime": {
                    "adaptation": self.__related_anime_helper("Adaptation:"),
                    "sideStory": self.__related_anime_helper("Side story:"),
                    "summary": self.__related_anime_helper("Summary:"),
                    "spinOff": self.__related_anime_helper("Spin-off:"),
                    "other": self.__related_anime_helper("Other:"),
                    "prequel": self.__related_anime_helper("Prequel:"),
                    "character": self.__related_anime_helper("Character:"),
                    "sequel": self.__related_anime_helper("Sequel:"),
                },
                "openingTheme": self.__theme_song_helper("opnening"),
                "endingTheme": self.__theme_song_helper("ending"),
            }
        }

    def __related_anime_helper(self, string: str) -> list:
        related_anime = self.soup.find("td", string=string)
        return (
            [
                {
                    "title": i.get_text(),
                    "type": i.get("href").split("/")[1],
                    "malId": int(i.get("href").split("/")[2]),
                }
                for i in related_anime.next_sibling.select("a")
            ]
            if related_anime
            else []
        )

    def __theme_song_helper(self, string: str) -> list:
        theme_song = self.soup.select(f"div.{string} > span.theme-song")
        return (
            [{"title": str(i.get_text(strip=True))} for i in theme_song]
            if theme_song
            else []
        )

    def __statistics_helper(self, field: str, replace: str = ",") -> Union[int, None]:
        try:
            return int(
                self.soup.find("span", string=field)
                .next_sibling.replace(replace, "")
                .strip()
            )
        except ValueError:
            return None

    def __alternative_titles_helper(self, field_name: str) -> Union[str, None]:
        field = self.soup.find("span", string=field_name)
        return str(field.next_sibling.strip()) if field else None

    def __information_aired_helper(self, index: str) -> Union[str, None]:
        aired: str = self.soup.find("span", string="Aired:").next_sibling.strip()

        found = match(
            r"(?P<month1>\w+)\s(?P<day1>\d+),\s(?P<year1>\d+)\sto\s(?P<month2>\w+)\s(?P<day2>\d+),\s(?P<year2>\d+)",
            aired,
        )

        if not found:
            return None

        month1 = found.group("month1")
        day1 = found.group("day1")
        year1 = found.group("year1")
        date_from = f"{month1} {day1}, {year1}"

        month2 = found.group("month2")
        day2 = found.group("day2")
        year2 = found.group("year2")
        date_to = f"{month2} {day2}, {year2}"

        return str(
            datetime.strptime(
                date_from if index == "from" else date_to, "%b %d, %Y"
            ).date()
        )

    def __get_image(self, title: str) -> Optional[str]:
        image = self.soup.find("img", alt=title)

        if image is None:
            return None

        return image.get("data-src")
