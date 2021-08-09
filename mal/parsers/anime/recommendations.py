from bs4 import BeautifulSoup


class Recommendations:
    def __init__(self, soup: BeautifulSoup, base_url: str) -> None:
        self.soup = soup
        self.base_url = base_url

    def __call__(self) -> dict:
        return {
            "data": [
                {
                    "imageUrl": i.select_one(
                        "td:first-child > .picSurround > a > img"
                    ).get("data-src"),
                    "title": i.select_one(
                        "td:last-child > div:nth-child(2) > a > strong"
                    ).get_text(),
                    "url": i.select_one("td:last-child > div:nth-child(2) > a").get(
                        "href"
                    ),
                    "recommendationUrl": f"{self.base_url}{i.select_one('td:last-child > div:nth-child(2) > span > a').get('href')}".strip(),
                    "malId": int(
                        i.select_one("td:last-child > div > div")
                        .get("rel")
                        .replace("a", "")
                    ),
                }
                for i in self.soup.select(".js-scrollfix-bottom-rel > .borderClass")
            ]
        }
