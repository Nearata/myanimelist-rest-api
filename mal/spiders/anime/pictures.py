from mal.spiders.utils import get_soup


class Pictures:
    def __init__(self, base_url, mal_id) -> None:
        self.base_url = base_url
        self.mal_id = mal_id

    def get(self):
        soup = get_soup(f"{self.base_url}/anime/{self.mal_id}/_/pics")
        return {
            "pictures": [
                {
                    "large": i.select_one("a").get("href"),
                    "small": i.select_one("a").get("href").replace("l.", ".")
                } for i in soup.select(".picSurround")
            ]
        }
