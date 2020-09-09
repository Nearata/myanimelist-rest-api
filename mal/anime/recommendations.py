from bs4 import BeautifulSoup


class Recommendations:
    def __init__(self, soup: BeautifulSoup, base_url: str) -> None:
        self.soup = soup
        self.base_url = base_url

    def __call__(self) -> dict:
        selector = self.soup.select(".js-scrollfix-bottom-rel > .borderClass")
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
