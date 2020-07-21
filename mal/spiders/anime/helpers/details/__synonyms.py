def synonyms_helper(soup):
    synonyms = soup.find("span", string="Synonyms:")
    if synonyms:
        return [
            i.strip()
            for i in synonyms.next_sibling.split(",")
        ]
    return []
