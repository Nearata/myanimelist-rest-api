from bs4 import BeautifulSoup


class Characters:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def __call__(self) -> dict:
        return {
            "characters": [
                {
                    "url": i.select_one("td:nth-of-type(1) > div.picSurround > a").get("href"),
                    "image": i.select_one("td:nth-of-type(1) > div.picSurround > a > img").get("data-src"),
                    "name": i.select_one("td:nth-of-type(2) > a").get_text(),
                    "role": i.select_one("td:nth-of-type(2) > div > small").get_text(),
                    "voice_actors": [
                        {
                            "name": actor.select_one("td:nth-of-type(1) > a").get_text(),
                            "language": actor.select_one("td:nth-of-type(1) > small").get_text(),
                            "url": actor.select_one("td:nth-of-type(2) > div.picSurround > a").get("href"),
                            "image": actor.select_one("td:nth-of-type(2) > div.picSurround > a > img").get("data-src")
                        } for actor in i.select("td:nth-of-type(3) > table tr")
                    ]
                } for i in reversed(self.soup.select_one("a[name=staff]").find_previous_siblings("table"))
            ]
        }
