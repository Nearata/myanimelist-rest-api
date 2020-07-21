def background_helper(soup):
    background = soup.select_one("span[itemprop=description]").parent
    for i in background.select("h2, span, div"):
        i.decompose()

    if not background.get_text().lower().startswith("no background"):
        return background.get_text()
    return None
