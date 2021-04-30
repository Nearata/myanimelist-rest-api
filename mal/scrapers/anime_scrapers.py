from requests import Session

from mal.utils.soup import SoupUtil

from .anime.characters import Characters
from .anime.clubs import Clubs
from .anime.details import Details
from .anime.episodes import Episodes
from .anime.featured import Featured
from .anime.moreinfo import MoreInfo
from .anime.news import News
from .anime.pictures import Pictures
from .anime.recommendations import Recommendations
from .anime.reviews import Reviews
from .anime.staff import Staff
from .anime.stats import Stats
from .anime.top import Top


class AnimeScrapers:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.base_url = "https://myanimelist.net"

        self.soup_util = SoupUtil(session)

    def characters(self, mal_id: int) -> dict:
        soup = self.soup_util.get_soup(f"{self.base_url}/anime/{mal_id}/_/characters")
        characters = Characters(soup)
        return characters()

    def clubs(self, mal_id: int) -> dict:
        soup = self.soup_util.get_soup(f"{self.base_url}/anime/{mal_id}/_/clubs")
        clubs = Clubs(soup, self.base_url)
        return clubs()

    def details(self, mal_id: int) -> dict:
        soup = self.soup_util.get_soup(f"{self.base_url}/anime/{mal_id}")
        details = Details(soup, self.base_url)
        return details()

    def episodes(self, mal_id: int, page_number: int) -> dict:
        page_url = (
            f"{self.base_url}/anime/{mal_id}/_/episode"
            if page_number == 1
            else f"{self.base_url}/anime/{mal_id}/_/episode?offset={page_number}00"
        )
        soup = self.soup_util.get_soup(page_url)
        episodes = Episodes(soup)
        return episodes()

    def featured(self, mal_id: int) -> dict:
        soup = self.soup_util.get_soup(f"{self.base_url}/anime/{mal_id}/_/featured")
        featured = Featured(soup)
        return featured()

    def moreinfo(self, mal_id: int) -> dict:
        soup = self.soup_util.get_soup(f"{self.base_url}/anime/{mal_id}/_/moreinfo")
        more_info = MoreInfo(soup)
        return more_info()

    def news(self, mal_id: int) -> dict:
        soup = self.soup_util.get_soup(f"{self.base_url}/anime/{mal_id}/_/news")
        news = News(soup, self.base_url)
        return news()

    def pictures(self, mal_id: int) -> dict:
        soup = self.soup_util.get_soup(f"{self.base_url}/anime/{mal_id}/_/pics")
        pictures = Pictures(soup)
        return pictures()

    def recommendations(self, mal_id: int) -> dict:
        soup = self.soup_util.get_soup(f"{self.base_url}/anime/{mal_id}/_/userrecs")
        recommendations = Recommendations(soup, self.base_url)
        return recommendations()

    def reviews(self, mal_id: int, page_number: int) -> dict:
        soup = self.soup_util.get_soup(
            f"{self.base_url}/anime/{mal_id}/_/reviews?p={page_number}"
        )
        reviews = Reviews(soup)
        return reviews()

    def staff(self, mal_id: int) -> dict:
        soup = self.soup_util.get_soup(f"{self.base_url}/anime/{mal_id}/_/characters")
        staff = Staff(soup)
        return staff()

    def stats(self, mal_id: int) -> dict:
        soup = self.soup_util.get_soup(f"{self.base_url}/anime/{mal_id}/_/stats")
        stats = Stats(soup)
        return stats()

    def top(self, _type: str, page: int) -> dict:
        params = {"type": "all", "limit": 0}

        if _type != "all":
            params["type"] = _type

        if page == 2:
            params["limit"] = 50
        elif page > 2:
            params["limit"] = 50 * page - 50

        soup = self.soup_util.get_soup(f"{self.base_url}/topanime.php", params=params)
        top = Top(soup)
        return top()
