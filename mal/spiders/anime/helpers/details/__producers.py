from bs4 import BeautifulSoup
from mal.spiders.anime.helpers.details.__str_to_int import str_to_int


def producers_helper(soup: BeautifulSoup, none_found: str, base_url: str) -> list:
    producers = soup.find("span", string="Producers:")
    if none_found in producers.next_sibling.strip().lower():
        return []
    return [
        {
            "name": i.get_text(),
            "url": f"{base_url}{i.get('href')}",
            "mal_id": str_to_int(i.get("href").split("/"))
        } for i in producers.find_next_siblings("a")
    ]
