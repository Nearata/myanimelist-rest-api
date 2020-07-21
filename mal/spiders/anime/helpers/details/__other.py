def other_helper(soup):
    other = soup.find("td", string="Other:")
    if other:
        return [
            {
                "title": i.get_text(),
                "type": i.get("href").split("/")[1],
                "mal_id": int(i.get("href").split("/")[2])
            } for i in other.next_sibling.select("a")
        ]
    return []
