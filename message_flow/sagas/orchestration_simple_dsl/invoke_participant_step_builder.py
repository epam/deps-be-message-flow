from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar

from ...commands.common import Command
from ...commands.consumer import CommandWithDestination
from ..orchestration import SagaDefinition  # type: ignore
from .participant_invocation import ParticipantInvocation
from .participant_invocation_impl import ParticipantInvocationImpl
from .participant_invocation_step import ParticipantInvocationStep
from .reply_handler import ReplyHandler
from .simple_saga_definition_builder import SimpleSagaDefinitionBuilder

Data = TypeVar("Data")
C = TypeVar("C", bound=Command)
T = TypeVar("T")


__all__ = ["InvokeParticipantStepBuilder"]


class InvokeParticipantStepBuilder(Generic[Data]):
    def __init__(self, parent: SimpleSagaDefinitionBuilder[Data]) -> None:
        self._parent = parent

        self._action: Optional[ParticipantInvocation[Data]] = None
        self._compensation: Optional[ParticipantInvocation[Data]] = None
        self._action_reply_handlers: Dict[str, ReplyHandler] = {}
        self._compensation_reply_handlers: Dict[str, ReplyHandler] = {}

    def with_action(
        self,
        action: Callable[[Data], CommandWithDestination],
        *,
        predicate: Optional[Callable[[Any], bool]] = None,
    ) -> "InvokeParticipantStepBuilder[Data]":
        self._action = ParticipantInvocationImpl(action, predicate)
        return self

    def with_compensation(
        self,
        compensation: Callable[[Data], CommandWithDestination],
        *,
        compensation_predicate: Optional[Callable[[Any], bool]] = None,
    ) -> "InvokeParticipantStepBuilder[Data]":
        self._compensation = ParticipantInvocationImpl(
            compensation, compensation_predicate
        )
        return self

    def on_reply(
        self, reply_class: Type[T], reply_handler: Callable[[Data, T], None]
    ) -> "InvokeParticipantStepBuilder[Data]":
        if self._compensation is not None:
            self._compensation_reply_handlers[reply_class.__name__] = ReplyHandler(
                reply_class, reply_handler
            )
        else:
            self._action_reply_handlers[reply_class.__name__] = ReplyHandler(
                reply_class, reply_handler
            )
        return self

    def step(self):
        from .step_builder import StepBuilder

        self._add_step()
        return StepBuilder[Data](self._parent)

    def build(self) -> SagaDefinition[Data]:
        self._add_step()
        return self._parent.build()

    def _add_step(self) -> None:
        self._parent.add_step(
            ParticipantInvocationStep[Data](
                self._action,
                self._compensation,
                self._action_reply_handlers,
                self._compensation_reply_handlers,
            )
        )
