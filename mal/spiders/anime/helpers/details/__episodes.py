def episodes_helper(soup):
    episdes = soup.find("span", string="Episodes:").next_sibling
    if episdes.strip() != "Unknown":
        return int(episdes)
    return None
