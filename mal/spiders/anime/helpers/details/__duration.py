from bs4 import BeautifulSoup
from mal.spiders.anime.helpers.details.__str_to_int import str_to_int


def duration_helper(soup: BeautifulSoup) -> int:
    duration = soup.find("span", string="Duration:").next_sibling.strip()
    if duration == "Unknown":
        return None
    return str_to_int(duration)
