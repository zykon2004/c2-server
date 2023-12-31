from pathlib import Path

from decouple import config

SECRET_KEY = config(
    "SECRET_KEY", default="qonOUAf/wwonkxviM+P6uNBpoOjUpmoX88YHA+EwLkc="
)
PROTOCOL = config("PROTOCOL", default="http")
SERVER_HOST = config("SERVER_HOST", default="0.0.0.0")  # noqa: S104
SERVER_PORT = config("SERVER_PORT", default=8080, cast=int)
REQUEST_TIMEOUT = config("REQUEST_TIMEOUT", default=5, cast=int)
CLIENT_LIVELINESS_THRESHOLD_MINUTES = config(
    "CLIENT_LIVELINESS_THRESHOLD_MINUTES", default=1, cast=int
)

DB_LOCATION = Path(__file__).resolve().parents[1] / "resources" / "db.sqlite3"
DB_ENGINE = f"sqlite:///{DB_LOCATION}"
KEYS_PATH = Path(__file__).parents[1] / "resources"
