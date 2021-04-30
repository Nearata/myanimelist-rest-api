from datetime import date, datetime, timedelta
from json import dumps

from mal.database import Cache


class CacheUtil:
    def get_or_none(self, cache_key: str) -> Cache:
        cache: Cache = Cache.get_or_none(Cache.anime_key == cache_key)
        return cache

    def save(self, cache_key: str, json: dict) -> None:
        new_cache = Cache(
            anime_key=cache_key,
            json=dumps(json),
            expire=datetime.utcnow().date() + timedelta(weeks=1),
        )
        new_cache.save()

    def delete(self, cache_key: str) -> None:
        get_cache = Cache.get(Cache.anime_key == cache_key)
        get_cache.delete_instance()

    def is_expired(self, date: date) -> bool:
        return datetime.utcnow().date() >= date
