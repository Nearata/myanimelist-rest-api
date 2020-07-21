def spin_off_helper(soup):
    spin_off = soup.find("td", string="Spin-off:")
    if spin_off:
        return [
            {
                "title": i.get_text(),
                "type": i.get("href").split("/")[1],
                "mal_id": int(i.get("href").split("/")[2])
            } for i in spin_off.next_sibling.select("a")
        ]
    return []
