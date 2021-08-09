from .const import MAL_URL
from .parsers.anime.characters import Characters
from .parsers.anime.clubs import Clubs
from .parsers.anime.details import Details
from .parsers.anime.episodes import Episodes
from .parsers.anime.featured import Featured
from .parsers.anime.moreinfo import MoreInfo
from .parsers.anime.news import News
from .parsers.anime.pictures import Pictures
from .parsers.anime.recommendations import Recommendations
from .parsers.anime.reviews import Reviews
from .parsers.anime.staff import Staff
from .parsers.anime.stats import Stats
from .parsers.top.anime import TopAnimeParser
from .utils import SoupUtil


class AnimeScrapers:
    def __init__(self, soup_util: SoupUtil) -> None:
        self.soup_util = soup_util

    async def characters(self, mal_id: int) -> dict:
        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime/{mal_id}/_/characters")
        characters = Characters(soup)
        return characters()

    async def clubs(self, mal_id: int) -> dict:
        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime/{mal_id}/_/clubs")
        clubs = Clubs(soup, MAL_URL)
        return clubs()

    async def details(self, mal_id: int) -> dict:
        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime/{mal_id}")
        details = Details(soup, MAL_URL)
        return details()

    async def episodes(self, mal_id: int, page: int) -> dict:
        page_url = (
            f"{MAL_URL}/anime/{mal_id}/_/episode"
            if page == 1
            else f"{MAL_URL}/anime/{mal_id}/_/episode?offset={100*page-100}"
        )
        soup = await self.soup_util.get_soup(page_url)
        episodes = Episodes(soup)
        return episodes()

    async def featured(self, mal_id: int) -> dict:
        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime/{mal_id}/_/featured")
        featured = Featured(soup)
        return featured()

    async def moreinfo(self, mal_id: int) -> dict:
        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime/{mal_id}/_/moreinfo")
        more_info = MoreInfo(soup)
        return more_info()

    async def news(self, mal_id: int) -> dict:
        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime/{mal_id}/_/news")
        news = News(soup, MAL_URL)
        return news()

    async def pictures(self, mal_id: int) -> dict:
        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime/{mal_id}/_/pics")
        pictures = Pictures(soup)
        return pictures()

    async def recommendations(self, mal_id: int) -> dict:
        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime/{mal_id}/_/userrecs")
        recommendations = Recommendations(soup, MAL_URL)
        return recommendations()

    async def reviews(self, mal_id: int, page: int) -> dict:
        soup = await self.soup_util.get_soup(
            f"{MAL_URL}/anime/{mal_id}/_/reviews?p={page}"
        )
        reviews = Reviews(soup)
        return reviews()

    async def staff(self, mal_id: int) -> dict:
        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime/{mal_id}/_/characters")
        staff = Staff(soup)
        return staff()

    async def stats(self, mal_id: int) -> dict:
        soup = await self.soup_util.get_soup(f"{MAL_URL}/anime/{mal_id}/_/stats")
        stats = Stats(soup)
        return stats()


class TopScrapers:
    def __init__(self, soup_util: SoupUtil) -> None:
        self.soup_util = soup_util

    @staticmethod
    def anime_types() -> list[str]:
        return [
            "all",
            "airing",
            "upcoming",
            "tv",
            "movie",
            "ova",
            "ona",
            "special",
            "bypopularity",
            "favorite",
        ]

    async def anime(self, _type: str, page: int) -> dict:
        params = {"type": "all", "limit": 0}

        if _type != "all":
            params["type"] = _type

        if page == 2:
            params["limit"] = 50
        elif page > 2:
            params["limit"] = 50 * page - 50

        soup = await self.soup_util.get_soup(f"{MAL_URL}/topanime.php", params=params)
        top = TopAnimeParser(soup)
        return top()
