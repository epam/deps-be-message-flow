import logging
from typing import Dict, List

from message_flow.events.common import DomainEvent, make_message_for_domain_event
from message_flow.events.mappers import ISerializer, JsonMapper
from message_flow.messaging.producer import IMessageProducer

_logger = logging.getLogger(__name__)


class DomainEventPublisher:
    def __init__(
        self,
        message_producer: IMessageProducer,
        *,
        serializer: ISerializer = JsonMapper()
    ) -> None:
        self._message_producer = message_producer
        self._serializer = serializer

    def publish(
        self,
        aggregate_type: str,
        aggregate_id: str,
        domain_events: List[DomainEvent],
        *,
        headers: Dict[str, str] = {}
    ) -> None:
        for event in domain_events:
            payload: bytes = self._serializer.serialize(event)
            _logger.info(
                "Publishing event %s with payload %s...",
                event.__class__.__name__,
                payload.decode(),
            )
            self._message_producer.send(
                aggregate_type,
                make_message_for_domain_event(
                    aggregate_type,
                    aggregate_id,
                    payload,
                    event.__class__.__name__,
                    headers=headers,
                ),
            )
