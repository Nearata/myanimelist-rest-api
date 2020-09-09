from mal.anime.characters import Characters
from mal.anime.clubs import Clubs
from mal.anime.details import Details
from mal.anime.episodes import Episodes
from mal.anime.featured import Featured
from mal.anime.moreinfo import MoreInfo
from mal.anime.news import News
from mal.anime.pictures import Pictures
from mal.anime.recommendations import Recommendations
from mal.anime.reviews import Reviews
from mal.anime.search import Search
from mal.anime.staff import Staff
from mal.anime.stats import Stats
from mal.anime.top import Top
from mal.soup import Soup


class AnimeSpiders:
    base_url = "https://myanimelist.net"

    def __init__(self, mal_id: int = None) -> None:
        self.mal_id = mal_id

    def characters(self) -> dict:
        soup = Soup(f"{self.base_url}/anime/{self.mal_id}/_/characters")
        characters = Characters(soup.get())
        return characters.get()

    def clubs(self) -> dict:
        soup = Soup(f"{self.base_url}/anime/{self.mal_id}/_/clubs", parser="html.parser")
        clubs = Clubs(soup.get(), self.base_url)
        return clubs.get()

    def details(self) -> dict:
        soup = Soup(f"{self.base_url}/anime/{self.mal_id}")
        details = Details(soup.get(), self.base_url)
        return details.get()

    def episodes(self, page_number: int) -> dict:
        page_url = f"{self.base_url}/anime/{self.mal_id}/_/episode" if page_number == 1 else f"{self.base_url}/anime/{self.mal_id}/_/episode?offset={page_number}00"
        soup = Soup(page_url)
        episodes = Episodes(soup.get())
        return episodes.get()

    def featured(self) -> dict:
        soup = Soup(f"{self.base_url}/anime/{self.mal_id}/_/featured")
        featured = Featured(soup.get())
        return featured.get()

    def moreinfo(self) -> dict:
        soup = Soup(f"{self.base_url}/anime/{self.mal_id}/_/moreinfo")
        more_info = MoreInfo(soup.get())
        return more_info.get()

    def news(self) -> dict:
        soup = Soup(f"{self.base_url}/anime/{self.mal_id}/_/news")
        news = News(soup.get(), self.base_url)
        return news.get()

    def pictures(self) -> dict:
        soup = Soup(f"{self.base_url}/anime/{self.mal_id}/_/pics")
        pictures = Pictures(soup.get())
        return pictures.get()

    def recommendations(self) -> dict:
        soup = Soup(f"{self.base_url}/anime/{self.mal_id}/_/userrecs")
        recommendations = Recommendations(soup.get(), self.base_url)
        return recommendations.get()

    def reviews(self, page_number: int) -> dict:
        soup = Soup(f"{self.base_url}/anime/{self.mal_id}/_/reviews?p={page_number}")
        reviews = Reviews(soup.get())
        return reviews.get()

    def staff(self) -> dict:
        soup = Soup(f"{self.base_url}/anime/{self.mal_id}/_/characters")
        staff = Staff(soup.get())
        return staff.get()

    def stats(self) -> dict:
        soup = Soup(f"{self.base_url}/anime/{self.mal_id}/_/stats")
        stats = Stats(soup.get())
        return stats.get()

    def top(self, _type: str, page: int) -> dict:
        params = {}

        if _type != "all":
            params["type"] = _type

        if page == 1:
            params["limit"] = 0
        elif page == 2:
            params["limit"] = 50
        else:
            params["limit"] = 50 * page - 50

        soup = Soup(f"{self.base_url}/topanime.php", params=params)
        top = Top(soup.get())
        return top.get()
