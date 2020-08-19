from bs4 import BeautifulSoup


def premiered_helper(soup: BeautifulSoup) -> str:
    premiered = soup.find("span", string="Premiered:")
    if premiered.next_sibling.strip() == "?":
        return None
    return premiered.parent.find("a").get_text()
