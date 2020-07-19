from mal.spiders.utils import get_soup


class Featured:
    def __init__(self, base_url, mal_id) -> None:
        self.base_url = base_url
        self.mal_id = mal_id

    def get(self):
        selector = get_soup(f"{self.base_url}/anime/{self.mal_id}/_/featured").select(".news-list > .news-unit")
        return {
            "featured": [
                {
                    "image": i.select_one("a > img").get("data-src"),
                    "url": i.select_one("div > p.title > a").get("href"),
                    "title": i.select_one("div > p.title > a").get_text(),
                    "content": i.select_one("div > .text").get_text(strip=True),
                    "writer": i.select_one("div > .information > p.info > a").get_text(),
                    "tags": [
                        {
                            "name": tag.get_text()
                        } for tag in i.select("div > .information > .tags > .tags-inner .tag")
                    ]
                } for i in selector
            ]
        }
