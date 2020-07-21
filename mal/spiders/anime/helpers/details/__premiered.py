def premiered_helper(soup):
    premiered = soup.find("span", string="Premiered:")
    if premiered.next_sibling.strip() != "?":
        return premiered.parent.find("a").get_text()
    return None
