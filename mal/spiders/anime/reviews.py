from datetime import datetime
from bs4 import BeautifulSoup


class Reviews:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def get(self) -> dict:
        selector = self.soup.select(".js-scrollfix-bottom-rel > .borderDark")
        reviewer_scores_helper = lambda soup, index: int(soup.select_one(f".textReadability tr:nth-child({index}) > td:last-child").get_text())
        return {
            "reviews": [
                {
                    "date": str(datetime.strptime(i.select_one(".spaceit:first-child > div.mb8:first-child > div:first-child").get_text(), "%b %d, %Y").date()),
                    "helpful_count": int(i.select_one(".spaceit:first-child > div:nth-child(2) td:last-child > div span").get_text()),
                    "url": i.select_one("div:last-child > div > div > a").get("href"),
                    "reviewer": {
                        "profile_url": i.select_one(".spaceit:first-child > div:last-child .picSurround > a").get("href"),
                        "image_url": i.select_one(".spaceit:first-child > div:last-child .picSurround > a > img").get("data-src"),
                        "username": i.select_one(".spaceit:first-child > div:last-child td:last-child > a").get_text(),
                        "scores": {
                            "overall": reviewer_scores_helper(i, 1),
                            "story": reviewer_scores_helper(i, 2),
                            "animation": reviewer_scores_helper(i, 3),
                            "sound": reviewer_scores_helper(i, 4),
                            "character": reviewer_scores_helper(i, 5),
                            "enjoyment": reviewer_scores_helper(i, 6)
                        }
                    }
                } for i in selector
            ]
        }
