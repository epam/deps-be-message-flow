from queue import Empty

import pytest

from message_flow.commands.common.command_message_headers import CommandMessageHeaders
from tests.factories.message import CommandMessageFactory


def test__command_dispatcher(queue, command_dispatcher):
    test_message = CommandMessageFactory()
    command_dispatcher.message_handler(test_message)

    test_output = queue.get_nowait()

    assert test_message.get_header(
        CommandMessageHeaders.DESTINATION
    ) == test_output.headers.pop("commandreply_destination")
    assert test_message.get_header(
        CommandMessageHeaders.REPLY_TO
    ) == test_output.headers.pop("commandreply_reply_to")
    assert test_message.get_header(
        CommandMessageHeaders.COMMAND_TYPE
    ) == test_output.headers.pop("commandreply_type")
    assert test_message.get_header("ID") == test_output.headers.pop(
        "reply_to_message_id"
    )


def test__command_dispatcher__handler_not_found(
    queue, command_message, command_dispatcher
):
    command_dispatcher.message_handler(command_message)

    with pytest.raises(Empty):
        queue.get_nowait()
