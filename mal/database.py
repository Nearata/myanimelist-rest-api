from peewee import DateField, Model, SqliteDatabase, TextField

db = SqliteDatabase(
    "cache.db",
    pragmas={
        "journal_mode": "wal",
        "cache_size": -1 * 64000,
        "foreign_keys": 1,
        "synchronous": 1,
    },
)


class Cache(Model):
    anime_key = TextField(unique=True)
    json = TextField()
    expire = DateField()

    class Meta:
        database = db
