from mal.spiders.utils import get_soup


def get_featured(mal_id):
    soup = get_soup(f"https://myanimelist.net/anime/{mal_id}/_/featured")
    selector = soup.select(".news-list > .news-unit")

    featured = [
        {
            "image": i.select_one("a > img").get("data-src"),
            "url": i.select_one("div > p.title > a").get("href"),
            "title": i.select_one("div > p.title > a").text,
            "content": i.select_one("div > .text").text.strip(),
            "writer": i.select_one("div > .information > p.info > a").text,
            "tags": [
                {
                    "name": tag.text
                } for tag in i.select(
                    "div > .information > .tags > .tags-inner .tag"
                )
            ]
        } for i in selector
    ]

    return {
        "featured": featured
    }
