from bs4 import BeautifulSoup
from mal.spiders.anime.helpers.details.__str_to_int import str_to_int


def studios_helper(soup: BeautifulSoup, none_found: str, base_url: str) -> list:
    studios = soup.find("span", string="Studios:")
    if none_found in studios.next_sibling.strip().lower():
        return []
    return [
        {
            "name": i.get_text(),
            "url": f"{base_url}{i.get('href')}",
            "mal_id": str_to_int(i.get("href").split("/"))
        } for i in studios.find_next_siblings("a")
    ]
