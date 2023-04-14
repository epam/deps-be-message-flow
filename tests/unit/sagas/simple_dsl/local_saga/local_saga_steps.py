from typing import Protocol

from .local_saga_data import LocalSagaData

__all__ = ["LocalSagaSteps"]


class LocalSagaSteps(Protocol):
    def local_step1(data: LocalSagaData) -> None:
        ...

    def local_step1_compensation(data: LocalSagaData) -> None:
        ...

    def local_step3(data: LocalSagaData) -> None:
        ...
