from fastapi import Request
from httpx import Client

from .scrapers.anime_scrapers import AnimeScrapers
from .utils.cache import CacheUtil


def get_cache(request: Request) -> CacheUtil:
    return request.app.state.cache


def get_anime(request: Request) -> AnimeScrapers:
    return request.app.state.animescrapers


def get_session(request: Request) -> Client:
    return request.app.state.session
