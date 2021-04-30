from requests import Session

from mal.main import create_app
from mal.cache import CacheUtil

app = create_app()
app.state.session = Session()
app.state.cache = CacheUtil()
