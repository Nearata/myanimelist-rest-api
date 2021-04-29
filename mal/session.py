from fastapi import Request
from requests import Session


def get_session(request: Request) -> Session:
    return request.app.state.session
