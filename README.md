# MyAnimeList REST API (Unofficial)

[![Maintainability](https://api.codeclimate.com/v1/badges/a2acb1abd8be12d7c751/maintainability)](https://codeclimate.com/github/Nearata/myanimelist-rest-api/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a2acb1abd8be12d7c751/test_coverage)](https://codeclimate.com/github/Nearata/myanimelist-rest-api/test_coverage)

> An unofficial REST API for MyAnimeList.net.

## Requirements

- Python 3.8+
- Pipenv

## Installation

- Install [Pipenv](https://pypi.org/project/pipenv/)
- Clone the repository or download the ZIP
- Open the terminal in the `myanimelist-rest-api` directory and run `pipenv install` to install all the dependencies

## Caching

This project uses `SQLite` to store JSON responses for `7 days` (manually checked). We use `Peewee` as driver to comunicate with SQLite database.

If you do not want to cache the responses, you can disable it by editing the `CACHE` constant in `config.py` to `False`.

## Production

Just read the `Deployment` section on [Uvicorn](https://www.uvicorn.org/deployment/) docs.

## Usage Example

Examples can be found on the [Documentation](#Documentation)

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

See the complete documentation [here](https://vonnearata.gitbook.io/docs/)

## License

Distributed under the MIT license. See `LICENSE` for more information.

## Contributing

1. Fork it
2. Commit your changes
3. Push to the branch
4. Create a new Pull Request

## Disclaimer

`MyAnimeList REST API` is independent. We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with MyAnimeList, LLC ([Website](https://myanimelist.net/)).

All product and company names are trademarks™ or registered® trademarks of their respective holders. Use of them does not imply any affiliation with or endorsement by them.
