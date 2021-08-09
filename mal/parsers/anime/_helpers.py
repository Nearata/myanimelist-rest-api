from typing import Union

from bs4 import BeautifulSoup


class AnimeHelpers:
    @staticmethod
    def background_helper(soup: BeautifulSoup) -> Union[str, None]:
        background = soup.select_one("[itemprop=description]").parent

        for i in background.select("div, p"):
            i.decompose()

        if background.get_text().lower().startswith("no background"):
            return None

        return str(background.get_text())

    @classmethod
    def duration_helper(cls, soup: BeautifulSoup) -> Union[int, None]:
        duration = soup.find("span", string="Duration:").next_sibling.strip()
        return cls.__str_to_int(duration) if duration != "Unknown" else None

    @staticmethod
    def episodes_helper(soup: BeautifulSoup) -> Union[int, None]:
        episdes = soup.find("span", string="Episodes:").next_sibling
        return int(episdes) if episdes.strip() != "Unknown" else None

    @classmethod
    def genres_helper(cls, soup: BeautifulSoup) -> list:
        genres = soup.find("span", string="Genres:")
        return (
            [
                {
                    "name": i.get_text(),
                    "malId": cls.__str_to_int(i.get("href").split("/")),
                }
                for i in genres.find_next_siblings("a")
            ]
            if genres
            else []
        )

    @classmethod
    def licensors_helper(
        cls, soup: BeautifulSoup, none_found: str, base_url: str
    ) -> list:
        licensors = soup.find("span", string="Licensors:").next_sibling.strip().lower()
        return (
            [
                {
                    "name": i.get_text(),
                    "url": f"{base_url}{i.get('href')}",
                    "malId": cls.__str_to_int(i.get("href").split("/")),
                }
                for i in soup.find("span", string="Licensors:").find_next_siblings("a")
            ]
            if none_found not in licensors
            else []
        )

    @staticmethod
    def premiered_helper(soup: BeautifulSoup) -> Union[str, None]:
        premiered = soup.find("span", string="Premiered:")

        if not premiered or premiered.next_sibling.strip() == "?":
            return None

        return str(premiered.parent.find("a").get_text())

    @classmethod
    def producers_helper(
        cls, soup: BeautifulSoup, none_found: str, base_url: str
    ) -> list:
        producers = soup.find("span", string="Producers:")
        return (
            [
                {
                    "name": i.get_text(),
                    "url": f"{base_url}{i.get('href')}",
                    "malId": cls.__str_to_int(i.get("href").split("/")),
                }
                for i in producers.find_next_siblings("a")
            ]
            if none_found not in producers.next_sibling.strip().lower()
            else []
        )

    @staticmethod
    def rating_helper(soup: BeautifulSoup) -> Union[str, None]:
        rating = soup.find("span", string="Rating:").next_sibling.strip()
        return str(rating) if rating.lower() != "none" else None

    @staticmethod
    def score_helper(soup: BeautifulSoup) -> Union[float, None]:
        score = soup.find("span", itemprop="ratingValue")
        return float(score.get_text()) if score else None

    @classmethod
    def studios_helper(
        cls, soup: BeautifulSoup, none_found: str, base_url: str
    ) -> list:
        studios = soup.find("span", string="Studios:")
        return (
            [
                {
                    "name": i.get_text(),
                    "url": f"{base_url}{i.get('href')}",
                    "malId": cls.__str_to_int(i.get("href").split("/")),
                }
                for i in studios.find_next_siblings("a")
            ]
            if none_found not in studios.next_sibling.strip().lower()
            else []
        )

    @staticmethod
    def synonyms_helper(soup: BeautifulSoup) -> list:
        synonyms = soup.find("span", string="Synonyms:")
        return (
            [str(i.strip()) for i in synonyms.next_sibling.split(",")]
            if synonyms
            else []
        )

    @staticmethod
    def synopsis_helper(soup: BeautifulSoup) -> Union[str, None]:
        synopsis = soup.select_one("[itemprop=description]")
        return str(synopsis.get_text()).strip() if synopsis else None

    @staticmethod
    def trailer_helper(soup: BeautifulSoup) -> Union[str, None]:
        trailer = soup.select_one(".video-promotion > .promotion")
        return str(trailer.get("href")) if trailer else None

    @staticmethod
    def __str_to_int(string: str) -> int:
        return int("".join(filter(str.isdigit, [s for s in string])))
