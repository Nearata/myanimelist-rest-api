from databases import Database
from orm import JSON, Date, Model, Text
from sqlalchemy import MetaData, create_engine

database = Database("sqlite:///cache.sqlite")
metadata = MetaData()


class Cache(Model):
    __tablename__ = "cache"
    __database__ = database
    __metadata__ = metadata

    id = Text(primary_key=True, unique=True)
    json = JSON()
    expire = Date()


engine = create_engine(str(database.url))
metadata.create_all(engine)
