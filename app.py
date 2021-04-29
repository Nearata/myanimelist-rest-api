from uvicorn import run

from mal.main import create_app
from mal.config import DEBUG

app = create_app()

def main() -> None:
    run(
        "app:app",
        host="0.0.0.0",
        port=8765,
        reload=DEBUG
    )


if __name__ == "__main__":
    main()
