def opening_theme_helper(soup):
    opening_theme = soup.select("div.opnening > span.theme-song")
    if opening_theme:
        return [
            {
                "title": opening.get_text(strip=True)
            } for opening in opening_theme
        ]
    return []
