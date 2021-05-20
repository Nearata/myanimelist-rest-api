from http import HTTPStatus

from fastapi.responses import JSONResponse


class BaseError(JSONResponse):
    def __init__(
        self, status_code: int = 200, title: str = None, detail: str = None
    ) -> None:
        content = {"error": {"status": status_code, "title": title, "detail": detail}}
        super().__init__(
            content=content,
            status_code=status_code,
            headers=None,
            media_type=None,
            background=None,
        )


class HTTPErrorResponse(BaseError):
    def __init__(self, status_code: int) -> None:
        http = HTTPStatus(status_code)
        super().__init__(
            status_code=status_code, title=http.phrase, detail=http.description
        )
