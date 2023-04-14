from typing import Generic, TypeVar

from message_flow.events.common import DomainEvent
from message_flow.messaging.common import IMessage

T = TypeVar("T", bound=DomainEvent)


class DomainEventEnvelope(Generic[T]):
    def __init__(
        self,
        message: IMessage,
        aggregate_type: str,
        aggregate_id: str,
        event_id: str,
        event: T,
    ) -> None:
        self._message = message
        self._aggregate_type = aggregate_type
        self._aggregate_id = aggregate_id
        self._event_id = event_id
        self._event = event

    @property
    def aggregate_id(self) -> str:
        return self._aggregate_id

    @property
    def message(self) -> IMessage:
        return self._message

    @property
    def event(self) -> T:
        return self._event

    @property
    def aggregate_type(self) -> str:
        return self._aggregate_type

    @property
    def event_id(self) -> str:
        return self._event_id
