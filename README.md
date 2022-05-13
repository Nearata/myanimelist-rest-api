# MyAnimeList REST API (Unofficial)

> An unofficial REST API for MyAnimeList.net.

## Requirements

- Python 3.9+
- Pipenv

## Installation

- Install [Pipenv](https://pypi.org/project/pipenv/)
- Clone the repository or download the ZIP
- Open the terminal in the `myanimelist-rest-api` directory and run `pipenv install` to install all the dependencies

## Caching

This project uses `SQLite` to store JSON responses for `7 days` (manually checked). We use [ORM](https://github.com/encode/orm) as driver to comunicate with SQLite database.

## Configuration

This application uses [Starlette Configuration](https://www.starlette.io/config/).

### Options

- CACHE - Default: False
- DISABLED_ROUTES - Default: []
- DEBUG - Default: False
- HTTP2 - Default: False
- USER_AGENT - Default: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0

## Production

Just read the `Deployment` section on [Uvicorn](https://www.uvicorn.org/deployment/) docs.

## Usage Example

Examples can be found on the [Documentation](#Documentation).

## Features

Currently supported features:

- Anime
  - Characters
  - Clubs
  - Episodes
  - Featured
  - More Info
  - News
  - Pictures
  - Recommendations
  - Reviews
  - Staff
  - Stats
- Search
  - Anime
- Top
  - Anime

## Documentation

The [documentation](https://github.com/Nearata/myanimelist-rest-api/wiki) is available here on this repo, under `Wiki`.

## Disclaimer

`MyAnimeList REST API` is independent. We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with MyAnimeList, LLC ([Website](https://myanimelist.net/)).

All product and company names are trademarks™ or registered® trademarks of their respective holders. Use of them does not imply any affiliation with or endorsement by them.

## Unlicense

See [UNLICENSE](UNLICENSE) for details.
