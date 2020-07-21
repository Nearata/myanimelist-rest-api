def trailer_helper(soup):
    trailer = soup.select_one(".video-promotion > .promotion")
    if trailer:
        return trailer.get("href")
    return None
