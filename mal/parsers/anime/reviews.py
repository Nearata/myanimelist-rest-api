from datetime import datetime

from bs4 import BeautifulSoup


class Reviews:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def __call__(self) -> dict:
        return {
            "data": [
                {
                    "date": str(
                        datetime.strptime(
                            i.select_one(
                                ".spaceit:first-child > div.mb8:first-child > div:first-child"
                            ).get_text(),
                            "%b %d, %Y",
                        ).date()
                    ),
                    "helpfulCount": int(
                        i.select_one(
                            ".spaceit:first-child > div:nth-child(2) td:last-child > div span"
                        ).get_text()
                    ),
                    "url": i.select_one("div:last-child > div > div > a").get("href"),
                    "reviewer": {
                        "profileUrl": i.select_one(
                            ".spaceit:first-child > div:last-child .picSurround > a"
                        ).get("href"),
                        "imageUrl": i.select_one(
                            ".spaceit:first-child > div:last-child .picSurround > a > img"
                        ).get("data-src"),
                        "username": i.select_one(
                            ".spaceit:first-child > div:last-child td:last-child > a"
                        ).get_text(),
                        "scores": {
                            "overall": self.__reviewer_scores_helper(i, 1),
                            "story": self.__reviewer_scores_helper(i, 2),
                            "animation": self.__reviewer_scores_helper(i, 3),
                            "sound": self.__reviewer_scores_helper(i, 4),
                            "character": self.__reviewer_scores_helper(i, 5),
                            "enjoyment": self.__reviewer_scores_helper(i, 6),
                        },
                    },
                }
                for i in self.soup.select(".js-scrollfix-bottom-rel > .borderDark")
            ]
        }

    def __reviewer_scores_helper(self, soup: BeautifulSoup, index: int) -> int:
        return int(
            soup.select_one(
                f".textReadability tr:nth-child({index}) > td:last-child"
            ).get_text()
        )
