from typing import Protocol, TypeVar

from ..orchestration import Saga  # type: ignore
from .simple_saga_dsl import SimpleSagaDsl

__all__ = ["SimpleSaga"]

Data = TypeVar("Data", covariant=True)


class SimpleSaga(Saga[Data], SimpleSagaDsl[Data], Protocol[Data]):
    ...
