from typing import Protocol, TypeVar

from message_flow.sagas.orchestration.saga_definition import SagaDefinition

__all__ = ["Saga"]

Data = TypeVar("Data")


class Saga(Protocol[Data]):
    @property
    def saga_definition(self) -> SagaDefinition[Data]:
        if hasattr(self, "_saga_definition"):
            return self._saga_definition  # type: ignore

        raise RuntimeError("Please define _saga_defenition attribute")

    @property
    def saga_type(self) -> str:
        return self.__class__.__name__

    def on_starting(self, saga_id: str, data: Data) -> None:
        ...

    def on_saga_completed_successfully(self, saga_id: str, data: Data) -> None:
        ...

    def on_saga_rolled_back(self, saga_id: str, data: Data) -> None:
        ...

    def on_saga_failed(self, saga_id: str, data: Data) -> None:
        ...
