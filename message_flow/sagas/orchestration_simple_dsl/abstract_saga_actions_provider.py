import abc
from typing import Callable, Generic, Optional, TypeVar

from ..orchestration import SagaActions  # type: ignore

__all__ = ["AbstractSagaActionsProvider"]


Data = TypeVar("Data")
SuppliedValue = TypeVar("SuppliedValue")


class AbstractSagaActionsProvider(abc.ABC, Generic[Data, SuppliedValue]):
    def __init__(
        self,
        saga_actions: Optional[SagaActions] = None,
        saga_actions_supplier: Optional[Callable[[], SuppliedValue]] = None,
    ) -> None:
        self._saga_actions = saga_actions
        self._saga_actions_supplier = saga_actions_supplier

    @classmethod
    def with_saga_actions(
        cls, saga_actions: SagaActions
    ) -> "AbstractSagaActionsProvider":
        return cls(saga_actions=saga_actions)

    @classmethod
    def with_saga_actions_provider(
        cls, saga_actions: SagaActions
    ) -> "AbstractSagaActionsProvider":
        return cls(saga_actions=saga_actions)

    def to_saga_actions(
        self,
        f1: Callable[[SagaActions[Data]], SuppliedValue],
        f2: Callable[[SuppliedValue], SuppliedValue],
    ):
        return (
            f1(self._saga_actions)
            if self._saga_actions is not None
            else f2(self._saga_actions_supplier.get())  # type: ignore
        )
