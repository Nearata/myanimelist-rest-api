from datetime import datetime
from mal.spiders.utils import get_soup


def get_reviews(mal_id, page_number):
    soup = get_soup(
        f"https://myanimelist.net/anime/{mal_id}/_/reviews?p={page_number}"
    )
    selector = soup.select(".js-scrollfix-bottom-rel > .borderDark")

    reviews = [
        {
            "date": str(
                datetime.strptime(
                    i.select_one(
                        ".spaceit:first-child > div.mb8:first-child > div:first-child"
                    ).text,
                    "%b %d, %Y"
                ).date()),
            "helpful_count": int(i.select_one(
                ".spaceit:first-child > div:nth-child(2) td:last-child > div span"
            ).text),
            "url": i.select_one(
                "div:last-child > div > div > a"
            ).get("href"),
            "reviewer": {
                "profile_url": i.select_one(
                    ".spaceit:first-child > div:last-child .picSurround > a"
                ).get("href"),
                "image_url": i.select_one(
                    ".spaceit:first-child > div:last-child .picSurround > a > img"
                ).get("data-src"),
                "username": i.select_one(
                    ".spaceit:first-child > div:last-child td:last-child > a"
                ).text,
                "scores": {
                    "overall": int(i.select_one(
                        ".textReadability tr:nth-child(1) > td:last-child > strong"
                    ).text),
                    "story": int(i.select_one(
                        ".textReadability tr:nth-child(2) > td:last-child"
                    ).text),
                    "animation": int(i.select_one(
                        ".textReadability tr:nth-child(3) > td:last-child"
                    ).text),
                    "sound": int(i.select_one(
                        ".textReadability tr:nth-child(4) > td:last-child"
                    ).text),
                    "character": int(i.select_one(
                        ".textReadability tr:nth-child(5) > td:last-child"
                    ).text),
                    "enjoyment": int(i.select_one(
                        ".textReadability tr:nth-child(6) > td:last-child"
                    ).text)
                }
            }
        } for i in selector
    ]

    return {
        "reviews": reviews
    }
