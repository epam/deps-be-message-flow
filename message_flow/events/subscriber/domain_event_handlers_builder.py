from typing import Callable, List, Type

from message_flow.events.common import DomainEvent
from message_flow.events.subscriber.domain_event_envelope import DomainEventEnvelope, T
from message_flow.events.subscriber.domain_event_handler import DomainEventHandler
from message_flow.events.subscriber.domain_event_handlers import DomainEventHandlers


class DomainEventHandlersBuilder:
    def __init__(self, aggregate_type: str) -> None:
        self._aggregate_type = aggregate_type
        self._queue: str = ""
        self._handlers: List[DomainEventHandler] = []

    @classmethod
    def for_aggregate_type(cls, aggregate_type: str) -> "DomainEventHandlersBuilder":
        return cls(aggregate_type)

    def for_queue(self, queue: str) -> "DomainEventHandlersBuilder":
        self._queue = queue
        return self

    def for_tenant(self, tenant: str) -> "DomainEventHandlersBuilder":
        self._aggregate_type = ".".join((tenant, self._aggregate_type))
        return self

    def on_event(
        self,
        event_class: Type[T],
        handler: Callable[[DomainEventEnvelope[DomainEvent]], None],
    ) -> "DomainEventHandlersBuilder":
        self._handlers.append(
            DomainEventHandler(self._aggregate_type, event_class, handler)
        )
        return self

    def and_for_aggregate_type(
        self, aggregate_type: str
    ) -> "DomainEventHandlersBuilder":
        self._aggregate_type = aggregate_type
        return self

    def build(self) -> DomainEventHandlers:
        return DomainEventHandlers(self._handlers, queue=self._queue)
