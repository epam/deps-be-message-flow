import abc

from .saga_instance import SagaInstance

__all__ = ["ISagaInstanceRepository"]


class ISagaInstanceRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, saga_instance: SagaInstance) -> SagaInstance:
        ...

    @abc.abstractmethod
    def find(self, saga_id: str) -> SagaInstance:
        ...

    @abc.abstractmethod
    def update(self, saga_instance: SagaInstance) -> SagaInstance:
        ...
