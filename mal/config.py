from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

CACHE = config('CACHE', cast=bool, default=False)
DISABLED_ROUTES = config('DISABLED_ROUTES', cast=CommaSeparatedStrings, default=[])
