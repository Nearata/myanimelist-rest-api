from bs4 import BeautifulSoup


def trailer_helper(soup: BeautifulSoup) -> str:
    trailer = soup.select_one(".video-promotion > .promotion")
    if not trailer:
        return None
    return trailer.get("href")
