import logging
from typing import Any, List, Optional

import requests
from db_helper import get_command_arguments, add_command
from schema import Command, CommandType
from settings import PROTOCOL, REQUEST_TIMEOUT


def send_command(target: str, type: CommandType, payload_id: int, payload_args: Optional[List[Any]]) -> None:
    headers = {"Content-type": "application/json"}
    clients, payload_info = get_command_arguments(target, payload_id)
    for identifier, external_ip, port in clients:
        payload, default_payload_args = payload_info
        
        if type == CommandType.KILL:
            command = Command(identifier=identifier, type=type)
            
        elif type == CommandType.RUN:
            used_payload_args = payload_args if payload_args else default_payload_args
            command = Command(
                identifier=identifier,
                type=type,
                payload=Command.string_to_base64(payload),
                arguments=used_payload_args,
            )
        
        client_url = generate_client_url(external_ip, port)
        try:
            response = requests.post(
                url=client_url,
                data=command.model_dump_json(),  # type: ignore
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )
            if response.status_code == 200:  # noqa: PLR2004
                add_command(command=command, client_id=identifier, payload_id=payload_id)
                logging.info("Successfully sent %s", command)
            else:
                logging.info(
                    "Failed to send command. Status code: %s", response.status_code
                )
        except requests.exceptions.RequestException as e:
            logging.error("Exception raised while sending command: %s", str(e))


def generate_client_url(host: str, port: int, protocol: str = PROTOCOL) -> str:
    return f"{protocol}://{host}:{port}"
