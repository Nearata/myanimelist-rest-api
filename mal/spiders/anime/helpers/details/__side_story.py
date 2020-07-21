def side_story_helper(soup):
    side_story = soup.find("td", string="Side story:")
    if side_story:
        return [
            {
                "title": i.get_text(),
                "type": i.get("href").split("/")[1],
                "mal_id": int(i.get("href").split("/")[2])
            } for i in side_story.next_sibling.select("a")
        ]
    return []
