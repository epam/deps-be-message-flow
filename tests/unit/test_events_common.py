import json
from dataclasses import asdict
from uuid import uuid4

from message_flow.events.common import make_message_for_domain_event
from tests.factories import EventFactory


def test__make_message_for_domain_event():
    test_aggregate_id = uuid4().hex
    test_aggregate_type = uuid4().hex
    test_event = EventFactory()
    test_payload = json.dumps(asdict(test_event)).encode()
    test_event_type = test_event.__class__.__name__

    expected_payload = json.dumps(asdict(test_event)).encode()
    expected_headers = {
        "event-aggregate-id": test_aggregate_id,
        "event-aggregate-type": test_aggregate_type,
        "event-type": test_event_type,
    }

    test_output = make_message_for_domain_event(
        test_aggregate_type, test_aggregate_id, test_payload, test_event_type
    )
    test_output.headers.pop("ID")

    assert expected_payload == test_output.payload
    assert expected_headers == test_output.headers
