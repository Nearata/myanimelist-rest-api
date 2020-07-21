def favorites_helper(soup):
    try:
        return int(soup.find("span", string="Favorites:").next_sibling.replace(",", "").strip())
    except ValueError:
        return None
