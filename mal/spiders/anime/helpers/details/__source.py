def source_helper(soup):
    source = soup.find("span", string="Source:")
    if source:
        return source.next_sibling.strip()
    return None
