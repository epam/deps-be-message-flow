from typing import List, Optional, Set

from message_flow.events.subscriber.domain_event_handler import DomainEventHandler
from message_flow.messaging.common import IMessage


class DomainEventHandlers:
    def __init__(
        self, handlers: List[DomainEventHandler], *, queue: Optional[str] = None
    ) -> None:
        self._handlers = handlers
        self._queue = queue

    @property
    def handlers(self) -> List[DomainEventHandler]:
        return self._handlers

    @property
    def queue(self) -> Optional[str]:
        return self._queue

    @property
    def aggregate_types(self) -> Set[str]:
        return set(map(lambda h: h.aggregate_type, self._handlers))

    def find_target_method(self, message: IMessage) -> Optional[DomainEventHandler]:
        return next(filter(lambda h: h.handles(message), self._handlers), None)  # type: ignore
