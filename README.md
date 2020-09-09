# MyAnimeList REST API (Unofficial)

[![Maintainability](https://api.codeclimate.com/v1/badges/a2acb1abd8be12d7c751/maintainability)](https://codeclimate.com/github/Nearata/myanimelist-rest-api/maintainability)

> An unofficial REST API for MyAnimeList.

## Requirements

- Python 3.8+
- Pipenv
- MongoDB (optional)

## Installation

- Install [Pipenv](https://pypi.org/project/pipenv/)
- Clone the repository or download the ZIP
- Open the terminal in the `myanimelist-rest-api` directory and run `pipenv install` to install all the dependencies

## Caching

This project uses `MongoDB` to store JSON responses for `7 days`. We use `PyMongo` as driver to comunicate with MongoDB Server.

If you want to cache the JSON responses, just comment out the line `CacheMiddleware()` in `create_app()` function.

## Production

At the moment, there's no recommended way to setup a server for production.

## Development setup

- Run `pipenv install --dev` to install both `dependencies` and `dev-dependencies`
- Comment the `CacheMiddleware()` line in `create_app()` (this way you will always get a fresh response)
- Run `pipenv run python dev.py` to start the wsgi development server on [http://127.0.0.1:5000](http://127.0.0.1:5000)

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
  - Search
  - Staff
  - Stats
  - Top

## Documentation

See the complete documentation [here](https://vonnearata.gitbook.io/docs/)

## License

Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing

1. Fork it
2. Commit your changes
3. Push to the branch
4. Create a new Pull Request

## Disclaimer

`MyAnimeList REST API` is independent. We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with MyAnimeList, LLC ([Website](https://myanimelist.net/)).

All product and company names are trademarks™ or registered® trademarks of their respective holders. Use of them does not imply any affiliation with or endorsement by them.
