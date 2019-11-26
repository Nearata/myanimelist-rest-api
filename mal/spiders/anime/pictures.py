from mal.spiders.utils import get_soup


def get_pictures(mal_id):
    soup = get_soup(f"https://myanimelist.net/anime/{mal_id}/_/pics")

    pictures = [
        {
            "large": i.select_one("a").get("href"),
            "small": i.select_one("a").get("href").replace("l.", ".")
        } for i in soup.select(".picSurround")
    ]

    return {
        "pictures": pictures
    }
