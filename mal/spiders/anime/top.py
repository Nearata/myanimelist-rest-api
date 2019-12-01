from re import match
from re import search
from mal.spiders.utils import get_soup

def get_top(ttype, page):
    params = {}
    if ttype != "all":
        params["type"] = ttype

    if page == 1:
        params["limit"] = 0
    elif page == 2:
        params["limit"] = 50
    else:
        params["limit"] = 50 * page - 50

    soup = get_soup("https://myanimelist.net/topanime.php", params=params)

    selector = soup.select(".top-ranking-table tr:not(:first-child)")

    def a_type(string):
        regex = match(r"(TV|Movie|OVA|ONA|Music|Special)", string)
        if regex:
            return regex.group()
        return None

    def a_digits(string):
        regex = search(r"\d+", string.replace(",", ""))
        if regex:
            return int(regex.group())
        return None

    def a_score(string):
        regex = match(r"\d.\d+", string)
        if regex:
            return float(regex.group())
        return None

    top = [
        {
            "rank": int(i.select_one("td.rank>span").get_text()),
            "mal_id": int(i.select_one("td.title>a").get("id").replace("#area", "")),
            "url": i.select_one("td.title>a").get("href"),
            "image_url": i.select_one("td.title>a>img").get("data-src").replace("r/50x70/", ""),
            "title": i.select_one("td.title>.detail>.di-ib>a").get_text(),
            "type": a_type(i.select_one("td.title>.detail>.information>br:first-child").previous_sibling.strip()),
            "episodes": a_digits(i.select_one("td.title>.detail>.information>br:first-child").previous_sibling.strip()),
            "members": a_digits(i.select_one("td.title>.detail>.information>br:last-child").next_sibling.strip()),
            "score": a_score(i.select_one("td.score>div>span").get_text())
        } for i in selector
    ]

    return {
        "top": top
    }
