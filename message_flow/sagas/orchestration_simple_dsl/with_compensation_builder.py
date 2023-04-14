from typing import Any, Callable, Optional, Protocol, TypeVar

from ...commands.common import Command
from ...commands.consumer import CommandWithDestination
from .invoke_participant_step_builder import InvokeParticipantStepBuilder

__all__ = ["WithCompensationBuilder"]

Data = TypeVar("Data")
C = TypeVar("C", bound=Command)


class WithCompensationBuilder(Protocol[Data]):
    def with_compensation(
        self,
        compensation: Callable[[Data], CommandWithDestination],
        *,
        compensation_predicate: Optional[Callable[[Any], bool]] = None,
    ) -> InvokeParticipantStepBuilder[Data]:
        ...
