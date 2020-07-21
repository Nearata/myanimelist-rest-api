def japanese_helper(soup):
    japanese = soup.find("span", string="Japanese:")
    if japanese:
        return japanese.next_sibling.strip()
    return None
