def english_helper(soup):
    english = soup.find("span", string="English:")
    if english:
        return english.next_sibling.strip()
    return None
