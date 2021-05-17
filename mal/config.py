from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

CACHE = config("CACHE", cast=bool, default=False)
DISABLED_ROUTES = config("DISABLED_ROUTES", cast=CommaSeparatedStrings, default=[])
DEBUG = config("DEBUG", cast=bool, default=False)
HTTP2 = config("HTTP2", cast=bool, default=False)
USER_AGENT = config("USER_AGENT", cast=str, default="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")
