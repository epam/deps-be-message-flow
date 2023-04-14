from typing import Dict

from message_flow.commands.consumer import (
    CommandWithDestination,
    CommandWithDestinationBuilder,
)

from ..commands import *

__all__ = ["ConditionalSagaData"]


class ConditionalSagaData:
    DO1_COMMAND_EXTRA_HEADERS: Dict[str, str] = {"k": "v"}

    def __init__(self, invoke1: bool) -> None:
        self.invoke1 = invoke1

    def is_invoke1(self) -> bool:
        return self.invoke1

    def do1(self) -> CommandWithDestination:
        return (
            CommandWithDestinationBuilder.send(Do1Command())
            .to("participant1")
            .with_extra_headers(self.DO1_COMMAND_EXTRA_HEADERS)
            .build()
        )

    def undo1(self) -> CommandWithDestination:
        return (
            CommandWithDestinationBuilder.send(Undo1Command())
            .to("participant1")
            .with_extra_headers(self.DO1_COMMAND_EXTRA_HEADERS)
            .build()
        )

    def do2(self) -> CommandWithDestination:
        return (
            CommandWithDestinationBuilder.send(Do2Command()).to("participant2").build()
        )

    def to_dict(self) -> Dict[str, str]:
        return {"invoke1": "true" if self.invoke1 else "false"}

    @classmethod
    def from_dict(cls, raw_data: Dict[str, str]) -> "ConditionalSagaData":
        return cls(True if raw_data.get("invoke1") == "true" else False)
