from mal.spiders.utils import get_soup


def get_characters(mal_id):
    soup = get_soup(f"https://myanimelist.net/anime/{mal_id}/_/characters")
    selector = soup.select_one("a[name=staff]").find_previous_siblings("table")

    characters = [
        {
            "url": i.select_one(
                "td:nth-of-type(1) > div.picSurround > a"
            ).get("href"),
            "image": i.select_one(
                "td:nth-of-type(1) > div.picSurround > a > img"
            ).get("data-src"),
            "name": i.select_one("td:nth-of-type(2) > a").text,
            "role": i.select_one("td:nth-of-type(2) > div > small").text,
            "voice_actors": [
                {
                    "name": actor.select_one("td:nth-of-type(1) > a").text,
                    "language": actor.select_one(
                        "td:nth-of-type(1) > small").text,
                    "url": actor.select_one(
                        "td:nth-of-type(2) > div.picSurround > a").get("href"),
                    "image": actor.select_one(
                        "td:nth-of-type(2) > div.picSurround > a > img"
                    ).get("data-src")
                } for actor in i.select("td:nth-of-type(3) > table tr")
            ]
        } for i in reversed(selector)
    ]

    return {
        "characters": characters
    }
