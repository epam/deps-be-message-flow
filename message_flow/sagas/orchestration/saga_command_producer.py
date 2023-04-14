from typing import List

from ...commands.consumer import CommandWithDestination
from ...commands.producer import CommandProducer
from ..common import SagaCommandHeaders  # type: ignore

__all__ = ["SagaCommandProducer"]


class SagaCommandProducer:
    def __init__(self, command_producer: CommandProducer) -> None:
        self._command_producer = command_producer

    def send_commands(
        self,
        saga_type: str,
        saga_id: str,
        commands: List[CommandWithDestination],
        saga_reply_channel: str,
    ) -> str:
        message_id: str = ""
        for command in commands:
            headers = command.extra_headers
            headers[SagaCommandHeaders.SAGA_TYPE] = saga_type
            headers[SagaCommandHeaders.SAGA_ID] = saga_id
            message_id = self._command_producer.send(
                command.destination_channel,
                command.command,
                saga_reply_channel,
                headers=headers,
            )
        return message_id
