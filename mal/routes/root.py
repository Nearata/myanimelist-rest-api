from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root() -> dict[Any, Any]:
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "MyAnimeList REST API Unofficial",
            "description": "An unofficial REST API for MyAnimeList.",
            "termsOfService": None,
            "contact": None,
            "license": {
                "name": "MIT",
                "url": "https://raw.githubusercontent.com/Nearata/myanimelist-rest-api/main/LICENSE",
            },
            "version": "1.0.0",
        },
        "servers": {"url": "/", "description": None, "variables": None},
        "paths": {"/anime": {}, "/search": {}, "/top": {}},
        "externalDocs": {
            "description": "Official Documentation",
            "url": "https://github.com/Nearata/myanimelist-rest-api/wiki",
        },
    }
