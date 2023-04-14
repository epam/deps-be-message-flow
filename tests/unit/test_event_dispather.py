from queue import Empty

import pytest


def test__event_dispatcher(queue, test_event_message, event_dispatcher):
    _, test_message = test_event_message
    event_dispatcher.message_handler(test_message)

    test_output = queue.get_nowait()

    assert test_message == test_output.message


def test__event_dispatcher__handler_not_found(
    queue, domain_event_message, event_dispatcher
):
    _, test_message = domain_event_message
    event_dispatcher.message_handler(test_message)

    with pytest.raises(Empty):
        queue.get_nowait()
