from bs4 import BeautifulSoup


class AnimeHelpers:
    @staticmethod
    def background_helper(soup: BeautifulSoup) -> str:
        background = soup.select_one("[itemprop=description]").parent

        for i in background.select("div, p"):
            i.decompose()

        if background.get_text().lower().startswith("no background"):
            return None

        return background.get_text()

    @classmethod
    def duration_helper(cls, soup: BeautifulSoup) -> int:
        duration = soup.find("span", string="Duration:").next_sibling.strip()

        if duration == "Unknown":
            return None

        return cls.__str_to_int(duration)

    @staticmethod
    def episodes_helper(soup: BeautifulSoup) -> int:
        episdes = soup.find("span", string="Episodes:").next_sibling

        if episdes.strip() == "Unknown":
            return None

        return int(episdes)

    @classmethod
    def genres_helper(cls, soup: BeautifulSoup) -> list:
        genres = soup.find("span", string="Genres:")

        if not genres:
            return []

        return [
            {
                "name": i.get_text(),
                "mal_id": cls.__str_to_int(i.get("href").split("/"))
            } for i in genres.find_next_siblings("a")
        ]

    @classmethod
    def licensors_helper(cls, soup: BeautifulSoup, none_found: str, base_url: str) -> list:
        licensors = soup.find("span", string="Licensors:").next_sibling.strip().lower()

        if none_found in licensors:
            return []

        return [
            {
                "name": i.get_text(),
                "url": f"{base_url}{i.get('href')}",
                "mal_id": cls.__str_to_int(i.get("href").split("/"))
            } for i in soup.find("span", string="Licensors:").find_next_siblings("a")
        ]

    @staticmethod
    def premiered_helper(soup: BeautifulSoup) -> str:
        premiered = soup.find("span", string="Premiered:")

        if premiered.next_sibling.strip() == "?":
            return None

        return premiered.parent.find("a").get_text()

    @classmethod
    def producers_helper(cls, soup: BeautifulSoup, none_found: str, base_url: str) -> list:
        producers = soup.find("span", string="Producers:")

        if none_found in producers.next_sibling.strip().lower():
            return []

        return [
            {
                "name": i.get_text(),
                "url": f"{base_url}{i.get('href')}",
                "mal_id": cls.__str_to_int(i.get("href").split("/"))
            } for i in producers.find_next_siblings("a")
        ]

    @staticmethod
    def rating_helper(soup: BeautifulSoup) -> str:
        rating = soup.find("span", string="Rating:").next_sibling.strip()

        if rating.lower() == "none":
            return None

        return rating

    @staticmethod
    def score_helper(soup: BeautifulSoup) -> float:
        score = soup.find("span", itemprop="ratingValue")

        if not score:
            return None

        return float(score.get_text())

    @classmethod
    def studios_helper(cls, soup: BeautifulSoup, none_found: str, base_url: str) -> list:
        studios = soup.find("span", string="Studios:")

        if none_found in studios.next_sibling.strip().lower():
            return []

        return [
            {
                "name": i.get_text(),
                "url": f"{base_url}{i.get('href')}",
                "mal_id": cls.__str_to_int(i.get("href").split("/"))
            } for i in studios.find_next_siblings("a")
        ]

    @staticmethod
    def synonyms_helper(soup: BeautifulSoup) -> list:
        synonyms = soup.find("span", string="Synonyms:")

        if not synonyms:
            return []

        return [
            i.strip()
            for i in synonyms.next_sibling.split(",")
        ]

    @staticmethod
    def synopsis_helper(soup: BeautifulSoup) -> str:
        synopsis = soup.select_one("[itemprop=description]")

        if not synopsis:
            return None

        return synopsis.get_text(strip=True)

    @staticmethod
    def trailer_helper(soup: BeautifulSoup) -> str:
        trailer = soup.select_one(".video-promotion > .promotion")

        if not trailer:
            return None

        return trailer.get("href")

    @staticmethod
    def __str_to_int(string: str) -> int:
        return int("".join(filter(str.isdigit, [s for s in string])))
