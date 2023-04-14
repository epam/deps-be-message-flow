from typing import Protocol, TypeVar

from .saga_instance import SagaInstance

__all__ = ["SagaManager"]

Data = TypeVar("Data", contravariant=True)


class SagaManager(Protocol[Data]):
    def create(self, saga_data: Data) -> SagaInstance:
        ...

    def subscribe_to_reply_channel(self) -> None:
        ...
