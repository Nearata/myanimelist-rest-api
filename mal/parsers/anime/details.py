from datetime import datetime
from re import findall, match, search
from typing import Any, Optional, Union

from bs4 import BeautifulSoup

from ...const import MAL_URL
from ._helpers import AnimeHelpers


class Details:
    none_found = "none found"

    def __init__(self, soup: BeautifulSoup, base_url: str) -> None:
        self.soup = soup
        self.base_url = base_url

    def __call__(self) -> dict:
        details: dict[str, Any] = {
            "title": None,
            "pictureUrl": None,
            "synopsis": None,
            "background": None,
            "titleJapanese": None,
            "titleEnglish": None,
            "titleSynonyms": [],
            "type": None,
            "episodes": None,
            "status": None,
            "aired": {"from": None, "to": None},
            "premiered": None,
            "producers": [],
            "licensors": [],
            "studios": [],
            "source": None,
            "genres": [],
            "themes": [],
            "duration": None,
            "rating": None,
            "score": None,
            "ranked": None,
            "popularity": None,
            "members": None,
            "favorites": None,
            "externalLinks": [],
            "streamingPlatforms": [],
            "sequel": None,
            "prequel": None,
            "alternativeSetting": None,
            "alternativeVersion": None,
            "sideStory": None,
            "summary": None,
            "fullStory": None,
            "parentStory": None,
            "spinOff": None,
            "adaptation": None,
            "character": None,
            "other": None,
            "openingTheme": [],
            "endingTheme": [],
            "trailerUrl": [],
        }

        details.update({"title": self.soup.select_one("h1").get_text().strip()})

        picture = self.soup.find("img", attrs={"alt": details["title"]})
        if picture:
            details.update({"pictureUrl": picture.get("data-src")})

        title_japanese = self.soup.find("span", string="Japanese:")
        if title_japanese and (sibling := title_japanese.next_sibling):
            details.update({"titleJapanese": sibling.get_text().strip()})

        title_english = self.soup.find("span", string="English:")
        if title_english and (sibling := title_english.next_sibling):
            details.update({"titleEnglish": sibling.get_text().strip()})

        title_synonyms = self.soup.find("span", string="Synonyms:")
        if title_synonyms and (sibling := title_synonyms.next_sibling):
            details.update(
                {"titleSynonyms": [i.strip() for i in sibling.get_text().split(",")]}
            )

        _type = self.soup.find("span", string="Type:")
        if _type and (sibling := _type.find_next_sibling("a")):
            details.update({"type": sibling.get_text().strip()})

        episodes = self.soup.find("span", string="Episodes:")
        if (
            episodes
            and (sibling := episodes.next_sibling)
            and (found := match(r"\d+", sibling.get_text().strip()))
        ):
            details.update({"episodes": int(found.group())})

        status = self.soup.find("span", string="Status:")
        if status and (sibling := status.next_sibling):
            details.update({"status": sibling.get_text().strip()})

        aired = self.soup.find("span", string="Aired:")
        if aired and (sibling := aired.next_sibling):
            details.update({"aired": self.__get_aired(sibling.get_text().strip())})

        premiered = self.soup.find("span", string="Premiered:")
        if premiered and (sibling := premiered.find_next_sibling("a")):
            details.update({"premiered": sibling.get_text().strip()})

        producers = self.soup.find("span", string="Producers:")
        if (
            producers
            and (sibling := producers.find_next_siblings("a"))
            and sibling[0].get("href").startswith("/anime/producer")
        ):
            details.update({"producers": [i.get_text().strip() for i in sibling]})

        licensors = self.soup.find("span", string="Licensors:")
        if (
            licensors
            and (sibling := licensors.find_next_siblings("a"))
            and sibling[0].get("href").startswith("/anime/producer")
        ):
            details.update({"licensors": [i.get_text().strip() for i in sibling]})

        studios = self.soup.find("span", string="Studios:")
        if (
            studios
            and (sibling := studios.find_next_siblings("a"))
            and sibling[0].get("href").startswith("/anime/producer")
        ):
            details.update({"studios": [i.get_text().strip() for i in sibling]})

        source = self.soup.find("span", string="Source:")
        if source and (sibling := source.next_sibling):
            details.update({"source": sibling.get_text().strip()})

        genres = self.soup.find("span", string="Genres:")
        if genres and (sibling := genres.find_next_siblings("a")):
            details.update({"genres": [i.get_text().strip() for i in sibling]})

        themes = self.soup.find("span", string="Themes:")
        if themes and (sibling := themes.find_next_siblings("a")):
            details.update({"themes": [i.get_text().strip() for i in sibling]})

        duration = self.soup.find("span", string="Duration:")
        if duration and (sibling := duration.next_sibling):
            details.update(
                {"duration": self.__get_duration(sibling.get_text().strip())}
            )

        rating = self.soup.find("span", string="Rating:")
        if rating and (sibling := rating.next_sibling):
            details.update({"rating": sibling.get_text().strip()})

        score = self.soup.find("span", attrs={"itemprop": "ratingValue"})
        if score and (found := match(r"\d\.\d+", score.get_text().strip())):
            details.update({"score": float(found.group())})

        trailer = self.soup.find("div", attrs={"class": "video-promotion"})
        if trailer and (child := trailer.find("a")):
            details.update({"trailerUrl": child.get("href")})

        ranked = self.soup.find("span", string="Ranked:")
        if ranked and (sibling := ranked.next_sibling) and "#" in sibling.get_text():
            details.update({"ranked": sibling.get_text().strip()})

        popularity = self.soup.find("span", string="Popularity:")
        if (
            popularity
            and (sibling := popularity.next_sibling)
            and "#" in sibling.get_text()
        ):
            details.update({"popularity": sibling.get_text().strip()})

        members = self.soup.find("span", string="Members:")
        if (
            members
            and (sibling := members.next_sibling)
            and search(r"\d", sibling.get_text())
        ):
            details.update(
                {"members": int("".join(sibling.get_text().strip().split(",")))}
            )

        favorites = self.soup.find("span", string="Favorites:")
        if (
            favorites
            and (sibling := favorites.next_sibling)
            and search(r"\d", sibling.get_text())
        ):
            details.update(
                {"favorites": int("".join(sibling.get_text().strip().split(",")))}
            )

        external_links = self.soup.find("h2", string="External Links")
        if external_links and (sibling := external_links.find_next_sibling("div")):
            details.update(
                {
                    "externalLinks": [
                        {"name": i.get_text().strip(), "url": i.get("href")}
                        for i in sibling.find_all("a")
                    ]
                }
            )

        if streaming_platforms := self.soup.find_all(
            "a", attrs={"class": "broadcast-item"}
        ):
            details.update(
                {
                    "streamingPlatforms": [
                        {"name": i.get_text().strip(), "url": i.get("href")}
                        for i in streaming_platforms
                    ]
                }
            )

        synopsis = self.soup.find("p", attrs={"itemprop": "description"})
        if synopsis and "no synopsis" not in synopsis.get_text().lower():
            details.update({"synopsis": synopsis.get_text().strip()})

        background = self.soup.find("p", attrs={"itemprop": "description"})
        if (
            background
            and (parent := background.parent)
            and "no background" not in parent.get_text().lower()
        ):
            for i in parent.select("div, p"):
                i.decompose()

            details.update({"background": parent.get_text().strip()})

        related_anime = self.soup.find(
            "table", attrs={"class": "anime_detail_related_anime"}
        )
        if related_anime:
            for i in related_anime.select("tr"):
                related1 = i.select_one("td:first-child")
                related2 = i.select_one("td:last-child")

                if related1 and related2:
                    related1_text = (
                        related1.get_text()
                        .strip()
                        .removesuffix(":")
                        .lower()
                        .replace("-", " ")
                        .split(" ")
                    )
                    related1_camel = related1_text[0] + "".join(
                        i.capitalize() for i in related1_text[1:]
                    )
                    details.update(
                        {
                            f"{related1_camel}": [
                                {
                                    "name": related_item.get_text().strip(),
                                    "url": MAL_URL + related_item.get("href"),
                                    "id": int(id_found.group())
                                    if (
                                        id_found := search(
                                            r"\d+", related_item.get("href")
                                        )
                                    )
                                    else None,
                                }
                                for related_item in related2.find_all("a")
                            ]
                        }
                    )

        opening_theme = self.soup.find("h2", string="Opening Theme")
        if (
            opening_theme
            and (parent := opening_theme.parent)
            and (sibling := parent.next_sibling)
        ):
            songs = []
            for i in sibling.find_all_next("tr"):
                s = {}

                if found := i.find("span", attrs={"class": "theme-song-title"}):
                    s.update({"title": found.get_text().strip().replace('"', "")})

                if found := i.find("span", attrs={"class": "theme-song-artist"}):
                    s.update({"name": found.get_text().strip().replace("by ", "")})

                if (
                    found := i.find("span", attrs={"class": "theme-song-episode"})
                ) and (found_episodes := findall(r"\d+", found.get_text().strip())):
                    s.update({"episodes": "-".join(found_episodes)})

                if s:
                    songs.append(s)

            details.update({"openingTheme": songs})

        ending_theme = self.soup.find("h2", string="Ending Theme")
        if (
            ending_theme
            and (parent := ending_theme.parent)
            and (sibling := parent.next_sibling)
        ):
            songs = []
            for i in sibling.find_all_next("tr"):
                s = {}

                if found := i.find("span", attrs={"class": "theme-song-title"}):
                    s.update({"title": found.get_text().strip().replace('"', "")})

                if found := i.find("span", attrs={"class": "theme-song-artist"}):
                    s.update({"name": found.get_text().strip().replace("by ", "")})

                if (
                    found := i.find("span", attrs={"class": "theme-song-episode"})
                ) and (found_episodes := findall(r"\d+", found.get_text().strip())):
                    s.update({"episodes": "-".join(found_episodes)})

                if s:
                    songs.append(s)

            details.update({"endingTheme": songs})

        return {"data": dict(sorted(details.items()))}

    def __get_aired(self, string: str) -> dict[str, Any]:
        found = findall(r"(\w+)\s(\d{1,2}),\s(\d{4,})", string)

        if not found:
            return {"from": None, "to": None}

        fmt = lambda i: str(datetime.strptime(i, "%b %d %Y").date())

        if len(found) == 2:
            return {"from": fmt(" ".join(found[0])), "to": fmt(" ".join(found[1]))}

        return {"from": fmt(" ".join(found[0])), "to": None}

    def __get_duration(self, string: str) -> Optional[str]:
        found = findall(r"\d+", string)

        if not found:
            return None

        if len(found) == 2:
            return f"{found[0]}h{found[1]}m"

        return f"{found[0]}m"
