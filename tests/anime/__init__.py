from httpx import AsyncClient

from mal.utils.cache import CacheUtil
from mal.main import create_app
from mal.scrapers.anime_scrapers import AnimeScrapers


app = create_app()
app.state.session = AsyncClient()
app.state.cache = CacheUtil()
app.state.animescrapers = AnimeScrapers(app.state.session)
