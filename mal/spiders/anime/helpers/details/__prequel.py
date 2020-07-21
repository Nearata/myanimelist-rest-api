def prequel_helper(soup):
    prequel = soup.find("td", string="Prequel:")
    if prequel:
        return [
            {
                "title": i.get_text(),
                "type": i.get("href").split("/")[1],
                "mal_id": int(i.get("href").split("/")[2])
            } for i in prequel.next_sibling.select("a")
        ]
    return []
