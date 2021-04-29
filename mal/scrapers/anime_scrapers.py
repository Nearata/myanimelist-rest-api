from typing import Optional

from mal.scrapers.anime import *
from mal.utils import SoupUtil


class AnimeScrapers:
    def __init__(self, mal_id: Optional[int] = None) -> None:
        self.mal_id = mal_id
        self.base_url = "https://myanimelist.net"

    def __dir__(self) -> list:
        return [
            "characters",
            "clubs",
            "details",
            "episodes",
            "featured",
            "moreinfo",
            "news",
            "pictures",
            "recommendations",
            "reviews",
            "staff",
            "stats"
        ]

    def characters(self) -> dict:
        soup = SoupUtil.get_soup(f"{self.base_url}/anime/{self.mal_id}/_/characters")
        characters = Characters(soup)
        return characters()

    def clubs(self) -> dict:
        soup = SoupUtil.get_soup(f"{self.base_url}/anime/{self.mal_id}/_/clubs")
        clubs = Clubs(soup, self.base_url)
        return clubs()

    def details(self) -> dict:
        soup = SoupUtil.get_soup(f"{self.base_url}/anime/{self.mal_id}")
        details = Details(soup, self.base_url)
        return details()

    def episodes(self, page_number: int) -> dict:
        page_url = f"{self.base_url}/anime/{self.mal_id}/_/episode" if page_number == 1 else f"{self.base_url}/anime/{self.mal_id}/_/episode?offset={page_number}00"
        soup = SoupUtil.get_soup(page_url)
        episodes = Episodes(soup)
        return episodes()

    def featured(self) -> dict:
        soup = SoupUtil.get_soup(f"{self.base_url}/anime/{self.mal_id}/_/featured")
        featured = Featured(soup)
        return featured()

    def moreinfo(self) -> dict:
        soup = SoupUtil.get_soup(f"{self.base_url}/anime/{self.mal_id}/_/moreinfo")
        more_info = MoreInfo(soup)
        return more_info()

    def news(self) -> dict:
        soup = SoupUtil.get_soup(f"{self.base_url}/anime/{self.mal_id}/_/news")
        news = News(soup, self.base_url)
        return news()

    def pictures(self) -> dict:
        soup = SoupUtil.get_soup(f"{self.base_url}/anime/{self.mal_id}/_/pics")
        pictures = Pictures(soup)
        return pictures()

    def recommendations(self) -> dict:
        soup = SoupUtil.get_soup(f"{self.base_url}/anime/{self.mal_id}/_/userrecs")
        recommendations = Recommendations(soup, self.base_url)
        return recommendations()

    def reviews(self, page_number: int) -> dict:
        soup = SoupUtil.get_soup(f"{self.base_url}/anime/{self.mal_id}/_/reviews?p={page_number}")
        reviews = Reviews(soup)
        return reviews()

    def staff(self) -> dict:
        soup = SoupUtil.get_soup(f"{self.base_url}/anime/{self.mal_id}/_/characters")
        staff = Staff(soup)
        return staff()

    def stats(self) -> dict:
        soup = SoupUtil.get_soup(f"{self.base_url}/anime/{self.mal_id}/_/stats")
        stats = Stats(soup)
        return stats()

    def top(self, _type: str, page: int) -> dict:
        params = {
            "type": "all",
            "limit": 0
        }

        if _type != "all":
            params["type"] = _type

        if page == 2:
            params["limit"] = 50
        elif page > 2:
            params["limit"] = 50 * page - 50

        soup = SoupUtil.get_soup(f"{self.base_url}/topanime.php", params=params)
        top = Top(soup)
        return top()
