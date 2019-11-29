from mal.spiders.utils import get_soup


def get_recommendations(mal_id):
    soup = get_soup(f"https://myanimelist.net/anime/{mal_id}/_/userrecs")
    selector = soup.select(".js-scrollfix-bottom-rel > .borderClass")

    userrecs = [
        {
            "image_url": i.select_one(
                "td:first-child > .picSurround > a > img"
            ).get("data-src"),
            "title": i.select_one(
                "td:last-child > div:nth-child(2) > a > strong"
            ).get_text(),
            "url": i.select_one(
                "td:last-child > div:nth-child(2) > a"
            ).get("href"),
            "recommendation_url": f"""
            https://myanimelist.net{
                i.select_one(
                    'td:last-child > div:nth-child(2) > span > a'
                ).get('href')
            }
            """.strip(),
            "mal_id": int(i.select_one(
                "td:last-child > div > div"
            ).get("rel").replace("a", ""))
        } for i in selector
    ]

    return {
        "userrecs": userrecs
    }
