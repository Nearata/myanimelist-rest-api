def synopsis_helper(soup):
    synopsis = soup.select_one("span[itemprop=description]")
    if synopsis:
        return synopsis.get_text(strip=True)
    return None
