from typing import Dict
from uuid import uuid4

from message_flow.events.common.event_message_headers import EventMessageHeaders
from message_flow.messaging.common import IMessage
from message_flow.messaging.producer import MessageBuilder


def make_message_for_domain_event(
    aggregate_type: str,
    aggregate_id: str,
    payload: bytes,
    event_type: str,
    *,
    headers: Dict[str, str] = None,
) -> IMessage:
    return (
        MessageBuilder.with_payload(payload)
        .with_extra_headers("", headers if headers else {})
        .with_header(EventMessageHeaders.AGGREGATE_ID, aggregate_id)
        .with_header(EventMessageHeaders.AGGREGATE_TYPE, aggregate_type)
        .with_header(EventMessageHeaders.EVENT_TYPE, event_type)
        .with_header(IMessage.ID, uuid4().hex)
        .build()
    )
