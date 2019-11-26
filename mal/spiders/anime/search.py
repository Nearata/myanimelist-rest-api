from re import match
from mal.spiders.utils import get_soup


def search(
            query,
            ttype=0,
            sscore=0,
            status=0,
            producer=0,
            rated=0,
            start_month=0,
            start_day=0,
            start_year=0,
            end_month=0,
            end_day=0,
            end_year=0
        ):
    soup = get_soup("https://myanimelist.net/anime.php", params={
        "q": query,
        "type": ttype,
        "score": sscore,
        "status": status,
        "p": producer,
        "r": rated,
        "sm": start_month,
        "sd": start_day,
        "sy": start_year,
        "em": end_month,
        "ed": end_day,
        "ey": end_year
    })
    selector = soup.select(".js-categories-seasonal tr:not(:first-child)")

    def episodes(string):
        regex = match(r"\d+", string)
        if regex:
            return int(regex.group())
        return None

    def score(string):
        regex = match(r"\d\.\d+", string)
        if regex:
            return float(regex.group())
        return None

    results = [
        {
            "mal_id": int(
                i.select_one(
                    "td:nth-child(2)>div>div"
                ).get("rel").replace("a", "")
            ),
            "title": i.select_one("td:nth-child(2)>a>strong").text,
            "type": i.select_one("td:nth-child(3)").text.strip(),
            "episodes": episodes(i.select_one("td:nth-child(4)").text.strip()),
            "score": score(i.select_one("td:nth-child(5)").text.strip())
        } for i in selector
    ]

    return {
        "results": results
    }
