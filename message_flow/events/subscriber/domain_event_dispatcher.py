import logging
from typing import List, Optional

from message_flow.events.common import EventMessageHeaders
from message_flow.events.mappers import IDeserializer, JsonMapper
from message_flow.events.subscriber.domain_event_envelope import DomainEventEnvelope
from message_flow.events.subscriber.domain_event_handler import DomainEventHandler
from message_flow.events.subscriber.domain_event_handlers import DomainEventHandlers
from message_flow.messaging.common import IMessage
from message_flow.messaging.consumer import IMessageConsumer

_logger = logging.getLogger(__name__)


class DomainEventDispatcher:
    def __init__(
        self,
        domain_event_handlers: DomainEventHandlers,
        message_consumer: IMessageConsumer,
        *,
        deserializer: IDeserializer = JsonMapper()
    ) -> None:
        self._domain_event_handlers = domain_event_handlers
        self._message_consumer = message_consumer
        self._deserializer = deserializer

    @property
    def handlers(self) -> List[DomainEventHandler]:
        return self._domain_event_handlers.handlers

    def initialize(self) -> None:
        self._message_consumer.subscribe(
            self._domain_event_handlers.aggregate_types,
            self.message_handler,
            queue=self._domain_event_handlers.queue,
        )

    def message_handler(self, message: IMessage) -> None:
        aggregate_type: str = message.get_required_header(
            EventMessageHeaders.AGGREGATE_TYPE
        )
        _logger.debug(
            "Got event %s, with payload %s for aggregate %s.",
            message.get_required_header(EventMessageHeaders.EVENT_TYPE),
            message.payload,
            aggregate_type,
        )  # noqa: WPS323

        handler: Optional[
            DomainEventHandler
        ] = self._domain_event_handlers.find_target_method(message)

        if handler is None:
            _logger.debug(
                "Event %s, for aggregate %s doesn't have a handler.",
                message.get_required_header(EventMessageHeaders.EVENT_TYPE),
                aggregate_type,
            )  # noqa: WPS323
            return

        event = self._deserializer.deserialize(handler.event_class, message.payload)

        handler.invoke(
            DomainEventEnvelope(
                message,
                aggregate_type,
                message.get_required_header(EventMessageHeaders.AGGREGATE_ID),
                message.get_required_header(IMessage.ID),
                event,
            )
        )
        _logger.info(
            "Event %s, with payload %s, for aggregate %s processed.",
            message.get_required_header(EventMessageHeaders.EVENT_TYPE),
            message.payload,
            aggregate_type,
        )  # noqa: WPS323
