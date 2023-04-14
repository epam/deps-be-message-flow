from typing import Generic, List, TypeVar

from ..orchestration import SagaDefinition  # type: ignore
from .saga_step import SagaStep
from .simple_saga_definition import SimpleSagaDefinition

__all__ = ["SimpleSagaDefinitionBuilder"]

Data = TypeVar("Data")


class SimpleSagaDefinitionBuilder(Generic[Data]):
    def __init__(self) -> None:
        self._saga_steps: List[SagaStep[Data]] = []

    def add_step(self, saga_step: SagaStep[Data]) -> None:
        self._saga_steps.append(saga_step)

    def build(self) -> SagaDefinition[Data]:
        return SimpleSagaDefinition[Data](self._saga_steps)
