def character_helper(soup):
    character = soup.find("td", string="Character:")
    if character:
        return [
            {
                "title": i.get_text(),
                "type": i.get("href").split("/")[1],
                "mal_id": int(i.get("href").split("/")[2])
            } for i in character.next_sibling.select("a")
        ]
    return []
