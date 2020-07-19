from mal.spiders.anime.characters import Characters
from mal.spiders.anime.clubs import Clubs
from mal.spiders.anime.details import Details
from mal.spiders.anime.episodes import Episodes
from mal.spiders.anime.featured import Featured
from mal.spiders.anime.moreinfo import MoreInfo
from mal.spiders.anime.news import News
from mal.spiders.anime.pictures import Pictures
from mal.spiders.anime.recommendations import Recommendations
from mal.spiders.anime.reviews import Reviews
from mal.spiders.anime.staff import Staff
from mal.spiders.anime.stats import Stats


class AnimeSpiders:
    def __init__(self) -> None:
        self.base_url = 'https://myanimelist.net'

    def characters(self, mal_id):
        characters = Characters(self.base_url, mal_id)
        return characters.get()

    def clubs(self, mal_id):
        clubs = Clubs(self.base_url, mal_id)
        return clubs.get()

    def details(self, mal_id):
        details = Details(self.base_url, mal_id)
        return details.get()

    def episodes(self, mal_id, page_number):
        episodes = Episodes(self.base_url, mal_id, page_number)
        return episodes.get()

    def featured(self, mal_id):
        featured = Featured(self.base_url, mal_id)
        return featured.get()

    def moreinfo(self, mal_id):
        more_info = MoreInfo(self.base_url, mal_id)
        return more_info.get()

    def news(self, mal_id):
        news = News(self.base_url, mal_id)
        return news.get()

    def pictures(self, mal_id):
        pictures = Pictures(self.base_url, mal_id)
        return pictures.get()

    def recommendations(self, mal_id):
        recommendations = Recommendations(self.base_url, mal_id)
        return recommendations.get()

    def reviews(self, mal_id, page_number):
        reviews = Reviews(self.base_url, mal_id, page_number)
        return reviews.get()

    def staff(self, mal_id):
        staff = Staff(self.base_url, mal_id)
        return staff.get()

    def stats(self, mal_id):
        stats = Stats(self.base_url, mal_id)
        return stats.get()
