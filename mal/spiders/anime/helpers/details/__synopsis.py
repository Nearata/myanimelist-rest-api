from bs4 import BeautifulSoup


def synopsis_helper(soup: BeautifulSoup) -> str:
    synopsis = soup.select_one("[itemprop=description]")

    if not synopsis:
        return None

    return synopsis.get_text(strip=True)
