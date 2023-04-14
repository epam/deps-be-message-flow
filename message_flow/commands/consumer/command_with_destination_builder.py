from typing import Dict

from message_flow.commands.common.command import C
from message_flow.commands.consumer.command_with_destination import (
    CommandWithDestination,
)


class CommandWithDestinationBuilder:
    def __init__(self, command: C) -> None:
        self._command = command

        self._destination_channel: str = ""
        self._extra_headers: Dict[str, str] = {}

    @classmethod
    def send(cls, command: C) -> "CommandWithDestinationBuilder":
        return cls(command)

    def to(self, destination_channel: str) -> "CommandWithDestinationBuilder":
        self._destination_channel = destination_channel
        return self

    def with_extra_headers(
        self, headers: Dict[str, str]
    ) -> "CommandWithDestinationBuilder":
        self._extra_headers = headers
        return self

    def build(self) -> CommandWithDestination:
        return CommandWithDestination(
            self._destination_channel, self._command, extra_headers=self._extra_headers
        )
