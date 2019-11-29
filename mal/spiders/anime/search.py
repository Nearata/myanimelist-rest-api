from datetime import datetime
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
            end_year=0,
            genres=0,
            genres_exclude=0,
            columns=0
        ):

    params = {
        "q": query,
        "type": ttype,
        "score": sscore,
        "status": status,
        "p": producer,
        "r": rated,
        "sy": start_year,
        "sm": start_month,
        "sd": start_day,
        "ey": end_year,
        "em": end_month,
        "ed": end_day,
        "gx": genres_exclude
    }

    if genres:
        for i in genres.split(","):
            params[f"genre[{i}]"] = i

    columns_lst = []
    if columns:
        columns_lst = columns.split(",")
        for i in columns_lst:
            params[f"c[{i}]"] = i
    else:
        params[f"c"] = 0

    soup = get_soup("https://myanimelist.net/anime.php", params=params)
    selector = soup.select_one(".js-categories-seasonal")

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

    results = []

    type_index = None
    eps_index = None
    score_index = None
    s_d_index = None
    e_d_index = None
    members_index = None
    rated_index = None

    for idx, i in enumerate(selector.select_one("tr:first-child").select("td"), 1):
        if "a" in columns_lst:
            if i.find(string="Type"):
                type_index = idx
        if "b" in columns_lst:
            if i.find(string="Eps."):
                eps_index = idx
        if "c" in columns_lst:
            if i.find(string="Score"):
                score_index = idx
        if "d" in columns_lst:
            if i.find(string="Start Date"):
                s_d_index = idx
        if "e" in columns_lst:
            if i.find(string="End Date"):
                e_d_index = idx
        if "f" in columns_lst:
            if i.find(string="Members"):
                members_index = idx
        if "g" in columns_lst:
            if i.find(string="Rated"):
                rated_index = idx

    for i in selector.select("tr:not(:first-child)"):
        anime = {}
        anime["mal_id"] = int(
            i.select_one(
                "td:nth-child(2)>div>div"
            ).get("rel").replace("a", "")
        )
        anime["url"] = i.select_one(
            "td:nth-child(1)>.picSurround>a"
        ).get("href")
        anime["image_url"] = i.select_one(
            "td:nth-child(1)>.picSurround>a>img"
        ).get("data-src").replace("r/50x70/", "")
        anime["title"] = i.select_one("td:nth-child(2)>a>strong").get_text()
        if type_index:
            anime["type"] = i.select_one(
                f"td:nth-child({type_index})"
            ).get_text(strip=True)
        if eps_index:
            anime["episodes"] = episodes(
                i.select_one(
                    f"td:nth-child({eps_index})"
                ).get_text(strip=True)
            )
        if score_index:
            anime["score"] = score(
                i.select_one(
                    f"td:nth-child({score_index})"
                ).get_text(strip=True)
            )
        if s_d_index:
            date = i.select_one(
                f"td:nth-child({s_d_index})"
            ).get_text(strip=True).replace("??", "01")
            if not len(date) <= 1:
                anime["start_date"] = str(
                    datetime.strptime(date, "%m-%d-%y").date()
                )
            else:
                anime["start_date"] = None
        if e_d_index:
            date = i.select_one(
                f"td:nth-child({e_d_index})"
            ).get_text(strip=True).replace("??", "01")
            if not len(date) <= 1:
                anime["end_date"] = str(
                    datetime.strptime(date, "%m-%d-%y").date()
                )
            else:
                anime["end_date"] = None
        if members_index:
            anime["members"] = int(
                i.select_one(
                    f"td:nth-child({members_index})"
                ).get_text(strip=True).replace(",", "")
            )
        if rated_index:
            anime["rated"] = i.select_one(
                f"td:nth-child({rated_index})"
            ).get_text(strip=True)

        results.append(anime)

    return {
        "results": results
    }
