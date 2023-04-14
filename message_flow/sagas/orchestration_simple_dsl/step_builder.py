from typing import Any, Callable, Generic, Optional, TypeVar

from ...commands.common import Command
from ...commands.consumer import CommandWithDestination
from .invoke_participant_step_builder import InvokeParticipantStepBuilder
from .local_step_builder import LocalStepBuilder
from .simple_saga_definition_builder import SimpleSagaDefinitionBuilder

__all__ = ["StepBuilder"]

Data = TypeVar("Data")
C = TypeVar("C", bound=Command)


class StepBuilder(Generic[Data]):
    def __init__(self, builder: SimpleSagaDefinitionBuilder[Data]) -> None:
        self._parent = builder

    def invoke_local(
        self, local_function: Callable[[Data], None]
    ) -> LocalStepBuilder[Data]:
        return LocalStepBuilder[Data](self._parent, local_function)

    def invoke_participant(
        self,
        action: Callable[[Data], CommandWithDestination],
        *,
        predicate: Optional[Callable[[Any], bool]] = None,
    ) -> InvokeParticipantStepBuilder[Data]:
        return InvokeParticipantStepBuilder[Data](self._parent).with_action(
            action, predicate=predicate
        )

    def with_compensation(
        self,
        compensation: Callable[[Data], CommandWithDestination],
        *,
        compensation_predicate: Optional[Callable[[Any], bool]] = None,
    ) -> InvokeParticipantStepBuilder[Data]:
        return InvokeParticipantStepBuilder[Data](self._parent).with_compensation(
            compensation, compensation_predicate=compensation_predicate
        )
