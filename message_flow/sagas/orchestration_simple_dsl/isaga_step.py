from typing import Protocol, TypeVar

from ...messaging.common.interfaces import IMessage

Data = TypeVar("Data", contravariant=True)

__all__ = ["ISagaStep"]


class ISagaStep(Protocol[Data]):
    def is_successful_reply(self, compensating: bool, message: IMessage) -> bool:
        ...

    def has_action(self, data: Data) -> bool:
        ...

    def has_compensation(self, data: Data) -> bool:
        ...
