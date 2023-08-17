from pathlib import Path
from typing import Literal

# This should not be here
SECRET_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTY5MTk1ODg2OCwiaWF0IjoxNjkxOTU4ODY4fQ.mi9ar0R_mHsq1JCvdbEvwHz40fGVgZXIARefYJ9f4iU"  # noqa: S105

SERVER_PORT = 8080
REQUEST_TIMEOUT = 5
CLIENT_LIVELINESS_THRESHOLD_MINUTES = 600
DB_LOCATION = Path(__file__).resolve().parents[1] / "resources" / "db.sqlite3"
DB_ENGINE = f"sqlite:///{DB_LOCATION}"
PROTOCOL: Literal["http", "https"] = "http"
