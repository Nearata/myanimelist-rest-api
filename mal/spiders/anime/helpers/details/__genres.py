from bs4 import BeautifulSoup
from mal.spiders.anime.helpers.details.__str_to_int import str_to_int


def genres_helper(soup: BeautifulSoup) -> list:
    genres = soup.find("span", string="Genres:")
    if not genres:
        return []
    return [
        {
            "name": i.get_text(),
            "mal_id": str_to_int(i.get("href").split("/"))
        } for i in genres.find_next_siblings("a")
    ]
