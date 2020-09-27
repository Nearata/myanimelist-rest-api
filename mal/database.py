from peewee import DateField, Model, SqliteDatabase, TextField


db = SqliteDatabase("cache.db", pragmas={
    "journal_mode": "wal"
})

class Cache(Model):
    anime_key = TextField(unique=True)
    json = TextField()
    expire = DateField()

    class Meta:
        database = db


class Database:
    @staticmethod
    def connect() -> None:
        db.connect()
        db.create_tables([Cache])

    @staticmethod
    def close() -> None:
        db.close()
