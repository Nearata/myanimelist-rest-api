from bs4 import BeautifulSoup


class Pictures:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def __call__(self) -> dict:
        return {
            "data": [
                {
                    "large": i.select_one("img")
                    .get("data-src")
                    .replace(".jpg", "l.jpg"),
                    "small": i.select_one("img").get("data-src"),
                }
                for i in self.soup.find_all("div", {"class": "picSurround"})
            ]
        }
