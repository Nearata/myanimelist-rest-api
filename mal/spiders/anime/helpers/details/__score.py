from bs4 import BeautifulSoup


def score_helper(soup: BeautifulSoup) -> float:
    score = soup.find("span", itemprop="ratingValue")
    if not score:
        return None
    return float(score.get_text())
