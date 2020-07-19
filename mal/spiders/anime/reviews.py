from datetime import datetime
from mal.spiders.utils import get_soup


class Reviews:
    def __init__(self, base_url, mal_id, page_number) -> None:
        self.base_url = base_url
        self.mal_id = mal_id
        self.page_number = page_number

    def get(self):
        selector = get_soup(f"{self.base_url}/anime/{self.mal_id}/_/reviews?p={self.page_number}").select(".js-scrollfix-bottom-rel > .borderDark")
        return {
            "reviews": [
                {
                    "date": str(
                        datetime.strptime(
                            i.select_one(
                                ".spaceit:first-child > div.mb8:first-child > div:first-child"
                            ).get_text(),
                            "%b %d, %Y"
                        ).date()),
                    "helpful_count": int(i.select_one(
                        ".spaceit:first-child > div:nth-child(2) td:last-child > div span"
                    ).get_text()),
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
                        ).get_text(),
                        "scores": {
                            "overall": int(i.select_one(
                                ".textReadability tr:nth-child(1) > td:last-child > strong"
                            ).get_text()),
                            "story": int(i.select_one(
                                ".textReadability tr:nth-child(2) > td:last-child"
                            ).get_text()),
                            "animation": int(i.select_one(
                                ".textReadability tr:nth-child(3) > td:last-child"
                            ).get_text()),
                            "sound": int(i.select_one(
                                ".textReadability tr:nth-child(4) > td:last-child"
                            ).get_text()),
                            "character": int(i.select_one(
                                ".textReadability tr:nth-child(5) > td:last-child"
                            ).get_text()),
                            "enjoyment": int(i.select_one(
                                ".textReadability tr:nth-child(6) > td:last-child"
                            ).get_text())
                        }
                    }
                } for i in selector
            ]
        }
