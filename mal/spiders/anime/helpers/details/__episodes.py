from bs4 import BeautifulSoup


def episodes_helper(soup: BeautifulSoup) -> int:
    episdes = soup.find("span", string="Episodes:").next_sibling
    if episdes.strip() == "Unknown":
        return None
    return int(episdes)
