def members_helper(soup):
    try:
        return int(soup.find("span", string="Members:").next_sibling.replace(",", "").strip())
    except ValueError:
        return None
