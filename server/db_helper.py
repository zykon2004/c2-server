import json
from datetime import datetime, timedelta
from typing import Any, List, Optional

from models import Client, Payload
from models import Command as CommandTableEntry
from schema import Command, Message
from settings import CLIENT_LIVELINESS_THRESHOLD_MINUTES, DB_ENGINE
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

ENGINE = create_engine(DB_ENGINE)


def update_or_insert_client(message: Message, request):
    with Session(ENGINE) as session:  # type: ignore
        message_id = str(message.identifier)
        existing_client = session.query(Client).filter_by(id=message_id).first()

        client_info = json.loads(message.get_result())

        if existing_client:
            existing_client.last_seen = datetime.now()
            existing_client.external_ip = request.client.host
            existing_client.port = client_info.get("port")
        else:
            new_client = Client(
                id=message_id,
                os=client_info.get("os"),
                hostname=client_info.get("hostname"),
                last_seen=datetime.now(),
                external_ip=request.client.host,
                port=client_info.get("port"),
            )
            session.add(new_client)

        session.commit()


def update_command_status(message: Message):
    with Session(ENGINE) as session:  # type: ignore
        command_id = str(message.identifier)
        command = session.query(Command).filter_by(id=command_id).first()

        if command:
            command.status = message.status.value
            command.response = message.get_result()
            command.last_update = datetime.now()

        session.commit()


def get_active_clients(
    with_column_names: bool = False,
    client_liveliness_threshold: int = CLIENT_LIVELINESS_THRESHOLD_MINUTES,
) -> List[Any]:
    with Session(ENGINE) as session:  # type: ignore
        liveliness_threshold_delta = datetime.now() - timedelta(
            minutes=client_liveliness_threshold
        )
        active_clients_query = session.query(Client).filter(
            Client.last_seen >= liveliness_threshold_delta
        )

        if with_column_names:
            return [Client.__table__.columns.keys(), *active_clients_query.all()]

        return active_clients_query.all()


def get_command_arguments(target: str, payload_id: Optional[int]):
    with Session(ENGINE) as session:  # type: ignore
        if target == "all":
            liveliness_threshold_delta = datetime.now() - timedelta(
                minutes=CLIENT_LIVELINESS_THRESHOLD_MINUTES
            )
            clients_query = session.query(Client).filter(
                Client.last_seen >= liveliness_threshold_delta
            )
            client_result = [
                (client.id, client.external_ip, client.port)
                for client in clients_query.all()
            ]
        else:
            client = session.query(Client).filter_by(id=target).first()
            client_result = (
                [(client.id, client.external_ip, client.port)] if client else []
            )
        if payload_id:
            payload_query = session.query(Payload).filter_by(id=payload_id).first()
            payload = (
                (payload_query.payload, payload_query.default_arguments)
                if payload_query
                else None
            )
        else:
            payload = None

    return client_result, payload


def add_command(
    command: Command,
    client_id: str,
    payload_id: Optional[int] = None,
):
    with Session(ENGINE) as session:  # type: ignore
        new_command = CommandTableEntry(
            id=str(command.identifier),
            payload_id=payload_id,
            arguments=command.arguments,
            client_id=client_id,
            time_sent=datetime.now(),
            type=command.type.value,
        )
        session.add(new_command)
        session.commit()
