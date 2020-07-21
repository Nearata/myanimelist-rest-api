def popularity_helper(soup):
    try:
        return int(soup.find("span", string="Popularity:").next_sibling.replace("#", "").strip())
    except ValueError:
        return None
