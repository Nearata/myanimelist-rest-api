from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from mal.main import create_app

app = create_app()


@pytest.fixture
async def client() -> AsyncGenerator["AsyncClient", None]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
