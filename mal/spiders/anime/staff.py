from mal.spiders.utils import get_soup


def get_staff(mal_id):
    soup = get_soup(f"https://myanimelist.net/anime/{mal_id}/_/characters")
    selector = soup.select_one("a[name=staff]").find_next_siblings("table")

    staff = [
        {
            "url": i.select_one(
                "td:first-child > .picSurround > a"
            ).get("href"),
            "image": i.select_one(
                "td:first-child > .picSurround > a > img"
            ).get("data-src"),
            "name": i.select_one("td:last-child > a").text,
            "role": i.select_one("td:last-child > div").text.strip()
        } for i in selector
    ]

    return {
        "staff": staff
    }
