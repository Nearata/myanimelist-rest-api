from mal.spiders.utils import get_soup


class Recommendations:
    def __init__(self, base_url, mal_id) -> None:
        self.base_url = base_url
        self.mal_id = mal_id

    def get(self):
        selector = get_soup(f"{self.base_url}/anime/{self.mal_id}/_/userrecs").select(".js-scrollfix-bottom-rel > .borderClass")
        return {
            "recommendations": [
                {
                    "image_url": i.select_one("td:first-child > .picSurround > a > img").get("data-src"),
                    "title": i.select_one("td:last-child > div:nth-child(2) > a > strong").get_text(),
                    "url": i.select_one("td:last-child > div:nth-child(2) > a").get("href"),
                    "recommendation_url": f"{self.base_url}{i.select_one('td:last-child > div:nth-child(2) > span > a').get('href')}".strip(),
                    "mal_id": int(i.select_one("td:last-child > div > div").get("rel").replace("a", ""))
                } for i in selector
            ]
        }
