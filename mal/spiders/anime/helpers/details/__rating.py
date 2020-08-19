from bs4 import BeautifulSoup


def rating_helper(soup: BeautifulSoup) -> str:
    rating = soup.find("span", string="Rating:").next_sibling.strip()
    if rating.lower() == "none":
        return None
    return rating
