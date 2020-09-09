from bs4 import BeautifulSoup


class Staff:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def get(self) -> dict:
        selector = self.soup.select_one("a[name=staff]").find_next_siblings("table")
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
