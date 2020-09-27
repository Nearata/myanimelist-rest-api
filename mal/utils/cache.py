from json import dumps
from datetime import date, datetime, timedelta

from mal.database import Cache


class CacheUtil:
    @staticmethod
    def get_or_none(cache_key: str) -> Cache:
        cache: Cache = Cache.get_or_none(Cache.anime_key == cache_key)
        return cache

    @staticmethod
    def save(cache_key: str, json: dict) -> None:
        new_cache = Cache(anime_key=cache_key, json=dumps(json), expire=datetime.utcnow().date() + timedelta(weeks=1))
        new_cache.save()

    @staticmethod
    def delete(cache_key: str) -> None:
        get_cache = Cache.get(Cache.anime_key == cache_key)
        get_cache.delete_instance()

    @staticmethod
    def is_expired(date: date) -> bool:
        return datetime.utcnow().date() >= date
