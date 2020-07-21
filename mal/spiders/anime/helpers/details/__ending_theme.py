def ending_theme_helper(soup):
    ending_theme = soup.select("div.ending > span.theme-song")
    if ending_theme:
        return [
            {
                "title": ending.get_text(strip=True)
            } for ending in ending_theme
        ]
    return []
