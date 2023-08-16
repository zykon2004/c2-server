import sqlite3

import uvicorn
from db_helper import update_command_status, update_or_insert_client
from fastapi import FastAPI, Request
from logger import LOGGING_CONFIG, setup_logger
from schema import Message, StatusType
from settings import DB_LOCATION, SERVER_PORT


def create_listener() -> FastAPI:
    app = FastAPI()
    db_connection = sqlite3.connect(DB_LOCATION)
    db_connection.cursor()

    @app.post("/", response_model=None)
    async def get_messages(message: Message, request: Request) -> None:
        if message.status == StatusType.HEARTBEAT:
            update_or_insert_client(message, request)
        else:
            update_command_status(message)

    return app


if __name__ == "__main__":
    setup_logger("c2-server")
    uvicorn.run(
        create_listener(),
        host="0.0.0.0",  # noqa: S104
        port=SERVER_PORT,
        log_config=LOGGING_CONFIG,
        # ssl_keyfile=str(Path("../keys/key.pem")),
        # ssl_certfile=Path("../keys/cert.pem"),
    )
