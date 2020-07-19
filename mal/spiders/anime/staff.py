from mal.spiders.utils import get_soup


class Staff:
    def __init__(self, base_url, mal_id) -> None:
        self.base_url = base_url
        self.mal_id = mal_id

    def get(self):
        selector = get_soup(f"{self.base_url}/anime/{self.mal_id}/_/characters").select_one("a[name=staff]").find_next_siblings("table")
        return {
            "staff": [
                {
                    "url": i.select_one("td:first-child > .picSurround > a").get("href"),
                    "image": i.select_one("td:first-child > .picSurround > a > img" ).get("data-src"),
                    "name": i.select_one("td:last-child > a").get_text(),
                    "role": i.select_one("td:last-child > div").get_text(strip=True)
                } for i in selector
            ]
        }
