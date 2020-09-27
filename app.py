import uvicorn

from mal.main import create_app
from mal.database import Database

app = create_app()

@app.on_event("startup")
def startup() -> None:
    Database.connect()

@app.on_event("shutdown")
def shutdown() -> None:
    Database.close()

def main() -> None:
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8765,
        reload=True
    )


if __name__ == "__main__":
    main()
