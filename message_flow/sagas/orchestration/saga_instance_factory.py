from typing import Collection, Dict, TypeVar

from .saga import Saga
from .saga_instance import SagaInstance
from .saga_manager import SagaManager
from .saga_manager_factory import SagaManagerFactory

__all__ = ["SagaInstanceFactory"]

SagaData = TypeVar("SagaData")


class SagaInstanceFactory:
    def __init__(
        self, saga_manager_factory: SagaManagerFactory, sagas: Collection[Saga]
    ) -> None:
        self._saga_managers: Dict[Saga, SagaManager] = {}

        for saga in sagas:
            self._saga_managers[saga] = self._make_saga_manager(
                saga_manager_factory, saga
            )

    def create(self, saga: Saga[SagaData], data: SagaData) -> SagaInstance:
        saga_manager = self._saga_managers.get(saga)
        if saga_manager is None:
            raise RuntimeError(f"No saga manager for {saga}")

        return saga_manager.create(data)

    def _make_saga_manager(
        self, saga_manager_factory: SagaManagerFactory, saga: Saga[SagaData]
    ) -> SagaManager[SagaData]:
        saga_manager = saga_manager_factory.make(saga)
        saga_manager.subscribe_to_reply_channel()
        return saga_manager
