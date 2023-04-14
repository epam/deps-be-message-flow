from typing import Callable, Generic, Optional, TypeVar

from ..orchestration import SagaDefinition  # type: ignore
from .local_step import LocalStep
from .simple_saga_definition_builder import SimpleSagaDefinitionBuilder

__all__ = ["LocalStepBuilder"]


Data = TypeVar("Data")


class LocalStepBuilder(Generic[Data]):
    def __init__(
        self,
        parent: SimpleSagaDefinitionBuilder[Data],
        local_function: Callable[[Data], None],
    ) -> None:
        self._parent = parent
        self._local_function = local_function

        self._compensation: Optional[Callable[[Data], None]] = None

    def with_compensation(
        self, local_compensation: Callable[[Data], None]
    ) -> "LocalStepBuilder[Data]":
        self._compensation = local_compensation
        return self

    def step(self):
        from .step_builder import StepBuilder

        self._parent.add_step(LocalStep(self._local_function, self._compensation))
        return StepBuilder[Data](self._parent)

    def build(self) -> SagaDefinition[Data]:
        self._parent.add_step(LocalStep(self._local_function, self._compensation))
        return self._parent.build()
