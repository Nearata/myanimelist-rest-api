from uvicorn import run

from mal.main import create_app

app = create_app()

def main() -> None:
    run(
        "app:app",
        host="0.0.0.0",
        port=8765,
        reload=True
    )


if __name__ == "__main__":
    main()
