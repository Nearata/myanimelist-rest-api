import uvicorn

from mal.main import create_app
from mal.database import Database
from mal.config import Config


app = create_app()

@app.on_event("startup")
def startup() -> None:
    if Config.CACHE:
        Database.connect()

@app.on_event("shutdown")
def shutdown() -> None:
    if Config.CACHE:
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
