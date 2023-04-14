from typing import Dict

from message_flow.commands.common.command import C


class CommandWithDestination:
    def __init__(
        self,
        destination_channel: str,
        command: C,
        *,
        extra_headers: Dict[str, str] = None
    ) -> None:
        self._destination_channel = destination_channel
        self._command = command
        self._extra_headers = extra_headers if extra_headers is not None else {}

    @property
    def destination_channel(self) -> str:
        return self._destination_channel

    @property
    def command(self) -> C:
        return self._command

    @property
    def extra_headers(self) -> Dict[str, str]:
        return self._extra_headers
