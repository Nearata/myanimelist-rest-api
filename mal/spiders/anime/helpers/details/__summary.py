def summary_helper(soup):
    summary = soup.find("td", string="Summary:")
    if summary:
        return [
            {
                "title": i.get_text(),
                "type": i.get("href").split("/")[1],
                "mal_id": int(i.get("href").split("/")[2])
            } for i in summary.next_sibling.select("a")
        ]
    return []
