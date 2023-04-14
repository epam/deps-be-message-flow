import json
from dataclasses import asdict
from uuid import uuid4

from message_flow.commands.common import make_message_for_command
from tests.factories import CommandFactory


def test__make_message_for_command():
    test_destination = uuid4().hex
    test_reply_to = uuid4().hex
    test_event = CommandFactory()
    test_payload = json.dumps(asdict(test_event)).encode()
    test_command_type = test_event.__class__.__name__

    expected_payload = json.dumps(asdict(test_event)).encode()
    expected_headers = {
        "command_type": test_command_type,
        "command_destination": test_destination,
        "command_reply_to": test_reply_to,
    }

    test_output = make_message_for_command(
        test_destination, test_payload, test_command_type, test_reply_to
    )

    del test_output.headers["ID"]

    assert expected_payload == test_output.payload
    assert expected_headers == test_output.headers
