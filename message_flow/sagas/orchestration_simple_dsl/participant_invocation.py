from typing import Protocol, TypeVar

from ...commands.consumer import CommandWithDestination
from ...messaging.common.interfaces import IMessage

__all__ = ["ParticipantInvocation"]

Data = TypeVar("Data", contravariant=True)


class ParticipantInvocation(Protocol[Data]):
    def is_successful_reply(self, message: IMessage) -> bool:
        ...

    def is_invocable(self, data: Data) -> bool:
        ...

    def make_command_to_send(self, data: Data) -> CommandWithDestination:
        ...
