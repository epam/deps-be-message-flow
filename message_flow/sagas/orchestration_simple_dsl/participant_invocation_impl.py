from typing import Any, Callable, Generic, Optional, TypeVar

from ...commands.common import Command, CommandReplyOutcome, ReplyMessageHeaders
from ...commands.consumer import CommandWithDestination
from ...messaging.common import IMessage
from .abstract_participant_invocation import AbstractParticipantInvocation

__all__ = ["ParticipantInvocationImpl"]

Data = TypeVar("Data")


class ParticipantInvocationImpl(AbstractParticipantInvocation[Data], Generic[Data]):
    def __init__(
        self,
        command_builder: Callable[[Data], CommandWithDestination],
        an_invocable_predicate: Optional[Callable[[Any], bool]] = None,
    ) -> None:
        super().__init__(an_invocable_predicate)
        self._command_builder = command_builder

    def is_successful_reply(self, message: IMessage) -> bool:
        return CommandReplyOutcome.SUCCESS.value == message.get_required_header(
            ReplyMessageHeaders.REPLY_OUTCOME
        )

    def make_command_to_send(self, data: Data) -> CommandWithDestination:
        return self._command_builder(data)
