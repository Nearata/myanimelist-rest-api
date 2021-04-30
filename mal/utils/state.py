from fastapi import Request
from requests import Session

from mal.scrapers import AnimeScrapers
from mal.utils import CacheUtil


def get_cache(request: Request) -> CacheUtil:
    return request.app.state.cache


def get_anime(request: Request) -> AnimeScrapers:
    return request.app.state.animescrapers


def get_session(request: Request) -> Session:
    return request.app.state.session
