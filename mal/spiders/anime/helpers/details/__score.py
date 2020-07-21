def score_helper(soup):
    score = soup.find("span", itemprop="ratingValue")
    if score:
        return float(score.get_text())
    return None
