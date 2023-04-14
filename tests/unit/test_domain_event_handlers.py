from uuid import uuid4

from message_flow.events.subscriber.domain_event_handler import DomainEventHandler
from message_flow.events.subscriber.domain_event_handlers_builder import (
    DomainEventHandlersBuilder,
)
from tests.factories import MessageFactory
from tests.factories.event import DomainEvent, SimpleEvent


def test__domain_event_handler__handles(test_event_message):
    test_aggregate_type, test_message = test_event_message

    test_handler = DomainEventHandler(test_aggregate_type, SimpleEvent, lambda x: x)

    assert test_handler.handles(test_message)


def test__domain_event_handler__not_handles():
    test_aggregate_type = uuid4().hex
    test_message = MessageFactory()

    test_handler = DomainEventHandler(test_aggregate_type, SimpleEvent, lambda x: x)

    assert not test_handler.handles(test_message)


def test__domain_event_handler__not_handles__different_event(test_event_message):
    test_aggregate_type, test_message = test_event_message

    test_handler = DomainEventHandler(test_aggregate_type, DomainEvent, lambda x: x)

    assert not test_handler.handles(test_message)


def test__domain_event_handlers_builder(test_event_message, domain_event_message):
    test_aggregate_type_1, test_message_1 = test_event_message
    test_aggregate_type_2, test_message_2 = domain_event_message
    test_queue = uuid4().hex

    expected_aggregate_types = set([test_aggregate_type_1, test_aggregate_type_2])

    builder = DomainEventHandlersBuilder.for_aggregate_type(
        test_aggregate_type_1
    ).on_event(SimpleEvent, lambda x: x)
    builder = builder.and_for_aggregate_type(test_aggregate_type_2).on_event(
        DomainEvent, lambda x: x
    )
    builder = builder.for_queue(test_queue)
    event_handlers = builder.build()

    assert expected_aggregate_types == event_handlers.aggregate_types
    assert test_queue == event_handlers.queue
    assert event_handlers.find_target_method(test_message_1)
    assert event_handlers.find_target_method(test_message_2)


def test__domain_event_handlers_builder__not_find_method(
    test_event_message, domain_event_message
):
    test_aggregate_type_1, _ = test_event_message
    _, test_message_2 = domain_event_message

    builder = DomainEventHandlersBuilder.for_aggregate_type(
        test_aggregate_type_1
    ).on_event(SimpleEvent, lambda x: x)
    event_handlers = builder.build()

    assert event_handlers.find_target_method(test_message_2) is None
