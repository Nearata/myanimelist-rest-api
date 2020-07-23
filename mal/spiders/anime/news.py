from re import search
from mal.spiders.utils import get_soup


class News:
    def __init__(self, base_url, mal_id) -> None:
        self.base_url = base_url
        self.mal_id = mal_id

    def get(self):
        selector = get_soup(f"{self.base_url}/anime/{self.mal_id}/_/news").select(".js-scrollfix-bottom-rel > .clearfix")
        return {
            "news": [
                {
                    "url": f"{self.base_url}{i.select_one('a').get('href')}".strip(),
                    "image_url": i.select_one("img").get("data-src") if i.select_one("img") else None,
                    "title": i.select_one(".spaceit > a > strong").get_text(),
                    "content": i.select_one(".clearfix > .clearfix > p > a").previous_sibling.strip(),
                    "author": i.select_one(".lightLink > a:first-child").get_text(),
                    "author_profile": f"{self.base_url}{i.select_one('.lightLink > a:first-child').get('href')}".strip(),
                    "comments": self.__comments(i.select_one(".lightLink > a:last-child").get_text()),
                    "forum_url": f"{self.base_url}{i.select_one('.lightLink > a:last-child').get('href')}".strip()
                } for i in selector
            ]
        }

    def __comments(self, string):
        regex = search(r"\d+", string)
        if regex:
            return int(regex.group())
        return None
