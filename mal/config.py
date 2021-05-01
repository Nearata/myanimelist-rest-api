from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

CACHE = config("CACHE", cast=bool, default=False)
DISABLED_ROUTES = config("DISABLED_ROUTES", cast=CommaSeparatedStrings, default=[])
DEBUG = config("DEBUG", cast=bool, default=False)
HTTP2 = config("HTTP2", cast=bool, default=False)
