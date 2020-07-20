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
from mal.spiders.anime.top import Top


class AnimeSpiders:
    base_url = 'https://myanimelist.net'

    def __init__(self, mal_id) -> None:
        self.mal_id = mal_id

    def characters(self):
        characters = Characters(self.base_url, self.mal_id)
        return characters.get()

    def clubs(self):
        clubs = Clubs(self.base_url, self.mal_id)
        return clubs.get()

    def details(self):
        details = Details(self.base_url, self.mal_id)
        return details.get()

    def episodes(self, page_number):
        episodes = Episodes(self.base_url, self.mal_id, page_number)
        return episodes.get()

    def featured(self):
        featured = Featured(self.base_url, self.mal_id)
        return featured.get()

    def moreinfo(self):
        more_info = MoreInfo(self.base_url, self.mal_id)
        return more_info.get()

    def news(self):
        news = News(self.base_url, self.mal_id)
        return news.get()

    def pictures(self):
        pictures = Pictures(self.base_url, self.mal_id)
        return pictures.get()

    def recommendations(self):
        recommendations = Recommendations(self.base_url, self.mal_id)
        return recommendations.get()

    def reviews(self, page_number):
        reviews = Reviews(self.base_url, self.mal_id, page_number)
        return reviews.get()

    def staff(self):
        staff = Staff(self.base_url, self.mal_id)
        return staff.get()

    def stats(self):
        stats = Stats(self.base_url, self.mal_id)
        return stats.get()

    def top(self, _type, page):
        top = Top(self.base_url, _type, page)
        return top.get()
