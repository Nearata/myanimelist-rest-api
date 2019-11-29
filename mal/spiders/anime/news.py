from re import search
from mal.spiders.utils import get_soup


def get_news(mal_id):
    soup = get_soup(f"https://myanimelist.net/anime/{mal_id}/_/news")
    selector = soup.select(".js-scrollfix-bottom-rel > .clearfix")

    def comments(string):
        regex = search(r"\d+", string)
        if regex:
            return int(regex.group())
        return None

    news = [
        {
            "url": f"""
            https://myanimelist.net{
                i.select_one('.picSurround > a').get('href')
            }
            """.strip(),
            "image_url": i.select_one(
                ".picSurround > a > img"
            ).get("data-src"),
            "title": i.select_one(".spaceit > a > strong").get_text(),
            "content": i.select_one(
                ".clearfix > .clearfix > p > a"
            ).previous_sibling.strip(),
            "author": i.select_one(".lightLink > a:first-child").get_text(),
            "author_profile": f"""
            https://myanimelist.net{
                i.select_one('.lightLink > a:first-child').get('href')
            }
            """.strip(),
            "comments": comments(i.select_one(".lightLink > a:last-child").get_text()),
            "forum_url": f"""
            https://myanimelist.net{
                i.select_one('.lightLink > a:last-child').get('href')
            }
            """.strip(),
        } for i in selector
    ]

    return {
        "news": news
    }
