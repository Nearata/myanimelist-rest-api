from datetime import datetime, timedelta
from json import dumps

from orm.models import QuerySet

from ..database import Cache


class CacheUtil:
    def query(self, cache_key: str) -> QuerySet:
        return Cache.objects.filter(id=cache_key)

    async def save(self, cache_key: str, json: dict) -> None:
        await Cache.objects.create(
            id=cache_key,
            json=dumps(json),
            expire=datetime.utcnow().date() + timedelta(weeks=1),
        )

    def is_expired(self, cache: Cache) -> bool:
        return datetime.utcnow().date() >= cache.expire
