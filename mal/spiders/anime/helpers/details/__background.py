from bs4 import BeautifulSoup


def background_helper(soup: BeautifulSoup) -> str:
    background = soup.select_one("[itemprop=description]").parent

    for i in background.select("div, p"):
        i.decompose()

    if background.get_text().lower().startswith("no background"):
        return None

    return background.get_text()
