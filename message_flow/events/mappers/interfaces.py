import abc
from typing import Generic, Type, TypeVar, Union

from message_flow.commands.common import Command
from message_flow.events.common import DomainEvent

T = TypeVar("T", bound=Union[Command, DomainEvent])


class ISerializer(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def serialize(self, obj: T) -> bytes:
        ...


class IDeserializer(abc.ABC):
    @abc.abstractmethod
    def deserialize(self, obj_class: Type[T], payload: bytes) -> T:
        ...
