from typing import Callable, Type

from message_flow.events.common import DomainEvent, EventMessageHeaders
from message_flow.events.subscriber.domain_event_envelope import DomainEventEnvelope
from message_flow.messaging.common import IMessage


class DomainEventHandler:
    def __init__(
        self,
        aggregate_type: str,
        event_class: Type[DomainEvent],
        handler: Callable[[DomainEventEnvelope[DomainEvent]], None],
    ) -> None:
        self._aggregate_type = aggregate_type
        self._event_class = event_class
        self._handler = handler

    @property
    def event_class(self) -> Type[DomainEvent]:
        return self._event_class

    @property
    def aggregate_type(self) -> str:
        return self._aggregate_type

    def handles(self, message: IMessage) -> bool:
        return self._aggregate_type == message.get_required_header(
            EventMessageHeaders.AGGREGATE_TYPE
        ) and self._event_class.__name__ == message.get_required_header(
            EventMessageHeaders.EVENT_TYPE
        )

    def invoke(self, dee: DomainEventEnvelope[DomainEvent]) -> None:
        self._handler(dee)
