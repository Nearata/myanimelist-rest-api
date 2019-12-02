from mal.spiders.anime.characters import get_characters
from mal.spiders.anime.clubs import get_clubs
from mal.spiders.anime.details import get_details
from mal.spiders.anime.episodes import get_episodes
from mal.spiders.anime.featured import get_featured
from mal.spiders.anime.moreinfo import get_moreinfo
from mal.spiders.anime.news import get_news
from mal.spiders.anime.pictures import get_pictures
from mal.spiders.anime.recommendations import get_recommendations
from mal.spiders.anime.reviews import get_reviews
from mal.spiders.anime.staff import get_staff
from mal.spiders.anime.stats import get_stats


class AnimeSpiders:
    def characters(self, mal_id):
        return get_characters(mal_id)

    def clubs(self, mal_id):
        return get_clubs(mal_id)

    def details(self, mal_id):
        return get_details(mal_id)

    def episodes(self, mal_id, page_number):
        return get_episodes(mal_id, page_number)

    def featured(self, mal_id):
        return get_featured(mal_id)

    def moreinfo(self, mal_id):
        return get_moreinfo(mal_id)

    def news(self, mal_id):
        return get_news(mal_id)

    def pictures(self, mal_id):
        return get_pictures(mal_id)

    def recommendations(self, mal_id):
        return get_recommendations(mal_id)

    def reviews(self, mal_id, page_number):
        return get_reviews(mal_id, page_number)

    def staff(self, mal_id):
        return get_staff(mal_id)

    def stats(self, mal_id):
        return get_stats(mal_id)
