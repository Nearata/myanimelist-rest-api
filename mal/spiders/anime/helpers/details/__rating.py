def rating_helper(soup):
    rating = soup.find("span", string="Rating:").next_sibling.strip()
    if rating.lower() != "none":
        return rating
    return None
