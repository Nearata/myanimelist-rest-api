def ranked_helper(soup):
    try:
        return int(soup.find("span", string="Ranked:").next_sibling.replace("#", "").strip())
    except ValueError:
        return None
