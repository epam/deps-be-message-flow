from typing import Generic, TypeVar

from ..orchestration import SagaActions  # type: ignore
from .abstract_step_to_execute import AbstractStepToExecute
from .saga_execution_state import SagaExecutionState
from .saga_step import SagaStep

__all__ = ["StepToExecute"]

Data = TypeVar("Data")


class StepToExecute(AbstractStepToExecute[Data, SagaStep[Data]], Generic[Data]):
    def __init__(self, step: SagaStep, skipped: int, compensating: bool) -> None:
        super().__init__(step, skipped, compensating)

    def execute_step(
        self, data: Data, current_state: SagaExecutionState
    ) -> SagaActions[Data]:
        new_state: SagaExecutionState = current_state.next_state(self._size())
        builder = SagaActions.builder()
        compensating: bool = current_state.compensating

        self._step.make_step_outcome(data, self._compensating).visit(
            builder.with_is_local, builder.with_commands
        )

        return self._make_saga_actions(builder, data, new_state, compensating)
