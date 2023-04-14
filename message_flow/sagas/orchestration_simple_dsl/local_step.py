from typing import Any, Callable, Generic, Optional, TypeVar

from ...commands.common import CommandReplyOutcome, ReplyMessageHeaders
from ...messaging.common import IMessage
from .reply_handler import ReplyHandler
from .saga_step import SagaStep
from .step_outcome import IStepOutcome, StepOutcome

__all__ = ["LocalStep"]

Data = TypeVar("Data")


class LocalStep(Generic[Data], SagaStep[Data]):
    def __init__(
        self,
        local_function: Callable[[Data], None],
        compensation: Optional[Callable[[Data], None]] = None,
    ) -> None:
        self._local_function = local_function
        self._compensation = compensation

    def has_action(self, data: Data) -> bool:
        return True

    def has_compensation(self, data: Data) -> bool:
        return self._compensation is not None

    def is_successful_reply(self, compensating: bool, message: IMessage) -> bool:
        return CommandReplyOutcome.SUCCESS.value == message.get_required_header(
            ReplyMessageHeaders.REPLY_OUTCOME
        )

    def get_reply_handler(
        self, message: IMessage, compensating: bool
    ) -> Optional[ReplyHandler]:
        return None

    def make_step_outcome(self, data: Data, compensating: bool) -> IStepOutcome:
        try:
            if compensating:
                if self.has_compensation(data):
                    self._compensation(data)  # type: ignore
            else:
                self._local_function(data)

            return StepOutcome.make_local_outcome()
        except RuntimeError as error:
            return StepOutcome.make_local_outcome(error)
