from typing import Callable, Generic, TypeVar

from ..orchestration import SagaActions  # type: ignore
from .abstract_saga_actions_provider import AbstractSagaActionsProvider

__all__ = ["SagaActionsProvider"]

Data = TypeVar("Data")


class SagaActionsProvider(
    AbstractSagaActionsProvider[Data, SagaActions[Data]], Generic[Data]
):
    @classmethod
    def from_actions(cls, actions: SagaActions[Data]) -> "SagaActionsProvider":
        return cls(saga_actions=actions)

    @classmethod
    def from_supplier(
        cls, supplier: Callable[[], SagaActions[Data]]
    ) -> "SagaActionsProvider":
        return cls(saga_actions_supplier=supplier)
