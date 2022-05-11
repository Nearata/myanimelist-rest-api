from re import compile as re_compile
from typing import Any

from bs4 import BeautifulSoup

from ...const import MAL_CDN_URL


class Characters:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def __call__(self) -> dict:
        characters: list[dict[str, Any]] = []

        for i in self.soup.select(".js-anime-character-container table"):
            data: dict[str, Any] = {
                "url": None,
                "pictureUrl": None,
                "name": None,
                "role": None,
                "voiceActors": [],
            }

            classes = i.get("class", [])

            if "js-anime-character-table" not in classes:
                continue

            url = i.select_one("td:nth-of-type(1) a")
            if url:
                data.update({"url": url.get("href")})

            picture = i.select_one("td:nth-of-type(1) a img")
            if picture and not self.__has_questionmark(picture.get("data-src")):
                data.update(
                    {"pictureUrl": self.__character_image_url(picture.get("data-src"))}
                )

            name = i.select_one("td:nth-of-type(2) .h3_character_name")
            if name:
                data.update({"name": name.get_text().strip()})

            role = i.select_one("td:nth-of-type(2) div:nth-last-child(2)")
            if role:
                data.update({"role": role.get_text().strip()})

            voice_actors: list[dict[str, Any]] = []

            for i in i.select(".js-anime-character-va-lang"):
                actor_data: dict[str, Any] = {
                    "name": None,
                    "language": None,
                    "url": None,
                    "pictureUrl": None,
                }

                actor_name = i.select_one("td:nth-of-type(1) div:first-of-type")
                if actor_name:
                    actor_data.update({"name": actor_name.get_text().strip()})

                actor_language = i.select_one("td:nth-of-type(1) div:last-of-type")
                if actor_language:
                    actor_data.update({"language": actor_language.get_text().strip()})

                actor_url = i.select_one("td:last-of-type a")
                if actor_url:
                    actor_data.update({"url": actor_url.get("href")})

                actor_picture = i.select_one("td:last-of-type a img")
                if actor_picture and not self.__has_questionmark(
                    actor_picture.get("data-src")
                ):
                    actor_data.update(
                        {
                            "pictureUrl": self.__voiceactor_image_url(
                                actor_picture.get("data-src")
                            )
                        }
                    )

                voice_actors.append(dict(sorted(actor_data.items())))

            data.update({"voiceActors": voice_actors})

            characters.append(dict(sorted(data.items())))

        return {"data": characters}

    def __character_image_url(self, string: str) -> str:
        regex = re_compile(r"\b\/images\/characters\/\d{1,}\/\d{1,}.jpg\b")
        return f"{MAL_CDN_URL}{''.join(regex.findall(string))}"

    def __voiceactor_image_url(self, string: str) -> str:
        regex = re_compile(r"\b\/images\/voiceactors\/\d{1,}\/\d{1,}.jpg\b")
        return f"{MAL_CDN_URL}{''.join(regex.findall(string))}"

    def __has_questionmark(self, string: str) -> bool:
        return "questionmark_23.gif" in string
