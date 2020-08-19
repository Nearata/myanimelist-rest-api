from bs4 import BeautifulSoup


def synonyms_helper(soup: BeautifulSoup) -> list:
    synonyms = soup.find("span", string="Synonyms:")
    if not synonyms:
        return []
    return [
        i.strip()
        for i in synonyms.next_sibling.split(",")
    ]
