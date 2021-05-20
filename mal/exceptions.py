from starlette.requests import Request
from starlette.responses import JSONResponse


class ValidationException(Exception):
    def __init__(self, parameter: str, title: str, detail: str) -> None:
        self.parameter = parameter
        self.title = title
        self.detail = detail


class InvalidParameter(ValidationException):
    def __init__(self, parameter: str) -> None:
        super().__init__(
            parameter,
            title="Invalid Parameter",
            detail=f"The parameter `{parameter}` is not valid. Please double check the docs.",
        )


class MissingParameter(ValidationException):
    def __init__(self, parameter: str) -> None:
        super().__init__(
            parameter,
            title="Missing Parameter",
            detail=f"The parameter `{parameter}` is missing. Please double check the docs.",
        )


async def validation_exception_handler(
    request: Request, exc: ValidationException
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": {"status": 422, "title": exc.title, "detail": exc.detail}},
    )
