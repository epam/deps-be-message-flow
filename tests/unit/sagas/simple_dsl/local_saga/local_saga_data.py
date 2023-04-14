from typing import Dict

from message_flow.commands.consumer import (
    CommandWithDestination,
    CommandWithDestinationBuilder,
)

from ..commands import *

__all__ = ["LocalSagaData"]


class LocalSagaData:
    def do2(self) -> CommandWithDestination:
        return (
            CommandWithDestinationBuilder.send(Do2Command()).to("participant2").build()
        )

    def undo2(self) -> CommandWithDestination:
        return (
            CommandWithDestinationBuilder.send(Undo2Command())
            .to("participant2")
            .build()
        )

    def to_dict(self) -> Dict[str, str]:
        return {}

    @classmethod
    def from_dict(cls, raw_data: Dict[str, str]) -> "LocalSagaData":
        return cls()
