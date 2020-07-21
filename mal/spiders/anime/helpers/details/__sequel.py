def sequel_helper(soup):
    sequel = soup.find("td", string="Sequel:")
    if sequel:
        return [
            {
                "title": i.get_text(),
                "type": i.get("href").split("/")[1],
                "mal_id": int(i.get("href").split("/")[2])
            } for i in sequel.next_sibling.select("a")
        ]
    return []
