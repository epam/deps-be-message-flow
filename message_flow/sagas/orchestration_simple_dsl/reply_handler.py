from typing import Callable, Generic, Type, TypeVar

__all__ = ["ReplyHandler"]

T = TypeVar("T")
Data = TypeVar("Data")


class ReplyHandler(Generic[Data, T]):
    def __init__(
        self, reply_class: Type[T], reply_handler: Callable[[Data, T], None]
    ) -> None:
        self._reply_class = reply_class
        self._reply_handler = reply_handler

    def __call__(self, data: Data, reply: T) -> None:
        self._reply_handler(data, reply)

    @property
    def reply_class(self) -> Type[T]:
        return self._reply_class
