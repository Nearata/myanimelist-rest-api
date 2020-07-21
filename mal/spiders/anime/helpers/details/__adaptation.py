def adaptation_helper(soup):
    adaptation = soup.find("td", string="Adaptation:")
    if adaptation:
        return [
            {
                "title": i.get_text(),
                "type": i.get("href").split("/")[1],
                "mal_id": int(i.get("href").split("/")[2])
            } for i in adaptation.next_sibling.select("a")
        ]
    return []
