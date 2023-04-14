from typing import Dict, Generic

from message_flow.commands.common import C
from message_flow.messaging.common.message import IMessage


class CommandMessage(Generic[C]):
    def __init__(
        self,
        message_id: str,
        command: C,
        correlation_headers: Dict[str, str],
        message: IMessage,
    ) -> None:
        self._message_id = message_id
        self._command = command
        self._correlation_headers = correlation_headers
        self._message = message

    @property
    def message(self) -> IMessage:
        return self._message

    @property
    def message_id(self) -> str:
        return self._message_id

    @property
    def command(self) -> C:
        return self._command

    @property
    def correlation_headers(self) -> Dict[str, str]:
        return self._correlation_headers
