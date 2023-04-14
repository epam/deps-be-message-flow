from typing import Protocol, TypeVar

from .simple_saga_definition_builder import SimpleSagaDefinitionBuilder
from .step_builder import StepBuilder

__all__ = ["SimpleSagaDsl"]

Data = TypeVar("Data")


class SimpleSagaDsl(Protocol[Data]):
    def step(self) -> StepBuilder[Data]:
        builder = SimpleSagaDefinitionBuilder[Data]()
        return StepBuilder(builder)
