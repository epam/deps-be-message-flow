import abc
from typing import Any, Callable, Generic, Optional, Protocol, TypeVar

__all__ = ["AbstractParticipantInvocation"]

Data = TypeVar("Data")


class AbstractParticipantInvocation(abc.ABC, Generic[Data]):
    def __init__(
        self, an_invocable_predicate: Optional[Callable[[Any], bool]] = None
    ) -> None:
        self._invocable_predicate = an_invocable_predicate

    def is_invocable(self, data: Data) -> bool:
        if self._invocable_predicate is not None:
            return self._invocable_predicate(data)

        return True
