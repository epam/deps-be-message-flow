import abc
from typing import Generic, TypeVar

from ..orchestration import SagaActions  # type: ignore
from .isaga_step import ISagaStep
from .saga_execution_state import SagaExecutionState
from .saga_execution_state_json_serde import SagaExecutionStateJsonSerde

__all__ = ["AbstractStepToExecute"]


Data = TypeVar("Data")
SagaStep = TypeVar("SagaStep", bound=ISagaStep)


class AbstractStepToExecute(abc.ABC, Generic[Data, SagaStep]):
    def __init__(self, step: SagaStep, skipped: int, compensating: bool) -> None:
        self._step = step
        self._skipped = skipped
        self._compensating = compensating

    def _size(self) -> int:
        return 1 + self._skipped

    def _make_saga_actions(
        self,
        builder: SagaActions.Builder,
        data: Data,
        new_state: SagaExecutionState,
        compensating: bool,
    ) -> SagaActions[Data]:
        state: str = SagaExecutionStateJsonSerde.encode_state(new_state)
        return builder.build_actions(data, compensating, state, new_state.end_state)
