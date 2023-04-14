import json
from dataclasses import asdict
from uuid import uuid4

from message_flow.events.common import EventMessageHeaders
from message_flow.events.publisher import DomainEventPublisher
from tests.factories import EventFactory


def test__domain_event_publisher(queue, event_publisher: DomainEventPublisher):
    test_aggregate_id = uuid4().hex
    test_aggregate_type = uuid4().hex
    test_event = EventFactory()

    event_publisher.publish(test_aggregate_type, test_aggregate_id, [test_event])

    test_output = queue.get_nowait()

    assert test_aggregate_id == test_output.get_header(EventMessageHeaders.AGGREGATE_ID)
    assert test_aggregate_type == test_output.get_header(
        EventMessageHeaders.AGGREGATE_TYPE
    )
    assert test_event.__class__.__name__ == test_output.get_header(
        EventMessageHeaders.EVENT_TYPE
    )

    assert json.dumps(asdict(test_event)).encode() == test_output.payload


def test__domain_event_publisher__extra_headers(
    queue, event_publisher: DomainEventPublisher
):
    test_aggregate_id = uuid4().hex
    test_aggregate_type = uuid4().hex
    test_event = EventFactory()

    test_extra_headers = {"extra-header": uuid4().hex}

    event_publisher.publish(
        test_aggregate_type, test_aggregate_id, [test_event], headers=test_extra_headers
    )

    test_output = queue.get_nowait()

    assert test_extra_headers["extra-header"] == test_output.get_header("extra-header")
