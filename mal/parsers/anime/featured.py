from bs4 import BeautifulSoup


class Featured:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def __call__(self) -> dict:
        return {
            "data": [
                {
                    "image": i.select_one("a > img").get("data-src"),
                    "url": i.select_one("div > p.title > a").get("href"),
                    "title": i.select_one("div > p.title > a").get_text(),
                    "content": i.select_one("div > .text").get_text(strip=True),
                    "writer": i.select_one(
                        "div > .information > p.info > a"
                    ).get_text(),
                    "tags": [
                        {"name": tag.get_text()}
                        for tag in i.select(
                            "div > .information > .tags > .tags-inner .tag"
                        )
                    ],
                }
                for i in self.soup.select(".news-list > .news-unit")
            ]
        }
