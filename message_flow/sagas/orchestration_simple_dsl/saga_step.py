from typing import Any, Callable, Optional, Protocol, TypeVar

from ...messaging.common import IMessage
from .isaga_step import ISagaStep
from .reply_handler import ReplyHandler
from .step_outcome import IStepOutcome

__all__ = ["SagaStep"]

Data = TypeVar("Data", contravariant=True)


class SagaStep(ISagaStep[Data], Protocol[Data]):
    def get_reply_handler(
        self, message: IMessage, compensating: bool
    ) -> Optional[ReplyHandler]:
        ...

    def make_step_outcome(self, data: Data, compensating: bool) -> IStepOutcome:
        ...
