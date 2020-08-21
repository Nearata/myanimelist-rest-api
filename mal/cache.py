from datetime import timedelta
from pymongo import MongoClient


class Cache:
    mongo_client = MongoClient()

    def __init__(self, database: str, collection: str) -> None:
        self.database = database
        self.collection = collection
        self.documents = self.mongo_client[self.database][self.collection]
        self.documents.create_index("created_at", expireAfterSeconds=int(timedelta(weeks=1).total_seconds()))

    def find_cache(self, mal_id: str, mal_request: str) -> dict:
        cache_key = self.__generate_cache_key(mal_id, mal_request)
        document = self.documents.find_one(cache_key)

        if not document:
            return cache_key

        del document["_id"]
        del document["cache_key"]
        del document["created_at"]

        return document

    def insert_cache(self, json: dict) -> dict:
        return self.documents.insert_one(json)

    def __generate_cache_key(self, mal_id: str, mal_request: str) -> dict:
        return {"cache_key": f"{mal_id}_{mal_request}"}
