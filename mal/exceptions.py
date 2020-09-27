from fastapi.exceptions import HTTPException


class ParameterNotValid(HTTPException):
    def __init__(self, parameter: str) -> None:
        super().__init__(status_code=422, detail={
            "title": "Parameter not valid",
            "description": f"The parameter `{parameter}` is not valid. Please double check the docs."
        })


class MissingParameter(HTTPException):
    def __init__(self, parameter: str) -> None:
        super().__init__(status_code=422, detail={
            "title": "Missing parameter",
            "description": f"The parameter `{parameter}` is missing. Please double check the docs."
        })
