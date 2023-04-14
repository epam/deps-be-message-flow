from typing import Any, Callable, Dict, Generic, Optional, TypeVar

from ...commands.common import ReplyMessageHeaders
from ...messaging.common import IMessage
from .participant_invocation import ParticipantInvocation
from .reply_handler import ReplyHandler
from .step_outcome import IStepOutcome, StepOutcome

__all__ = ["ParticipantInvocationStep"]

Data = TypeVar("Data")


class ParticipantInvocationStep(Generic[Data]):
    def __init__(
        self,
        participant_invocation: Optional[ParticipantInvocation[Data]],
        compensation: Optional[ParticipantInvocation[Data]],
        action_reply_handlers: Dict[str, ReplyHandler],
        compensation_reply_handlers: Dict[str, ReplyHandler],
    ) -> None:
        self._action_reply_handlers = action_reply_handlers
        self._compensation_reply_handlers = compensation_reply_handlers
        self._participant_invocation = participant_invocation
        self._compensation = compensation

    def _get_participant_invocation(
        self, compensating: bool
    ) -> Optional[ParticipantInvocation[Data]]:
        return self._compensation if compensating else self._participant_invocation

    def is_successful_reply(self, compensating: bool, message: IMessage) -> bool:
        if (pi := self._get_participant_invocation(compensating)) is not None:
            return pi.is_successful_reply(message)

        raise RuntimeError("No invocation for the step.")

    def has_action(self, data: Data) -> bool:
        return (
            self._participant_invocation is not None
            and self._participant_invocation.is_invocable(data)
        )

    def has_compensation(self, data: Data) -> bool:
        return self._compensation is not None and self._compensation.is_invocable(data)

    def get_reply_handler(
        self, message: IMessage, compensating: bool
    ) -> Optional[ReplyHandler]:
        reply_type: str = message.get_required_header(ReplyMessageHeaders.REPLY_TYPE)
        return (
            self._compensation_reply_handlers
            if compensating
            else self._action_reply_handlers
        ).get(reply_type)

    def make_step_outcome(self, data: Data, compensating: bool) -> IStepOutcome:
        pi = self._get_participant_invocation(compensating)
        if pi is not None:
            commands_to_send = [pi.make_command_to_send(data)]
        else:
            commands_to_send = []
        return StepOutcome.make_remote_outcome(commands_to_send)
