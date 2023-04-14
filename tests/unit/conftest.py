import json
from dataclasses import asdict
from queue import Queue
from uuid import uuid4

import pytest
from pytest_factoryboy import register

from message_flow.commands.common import CommandMessageHeaders
from message_flow.commands.common.command import Command
from message_flow.commands.common.command_util import make_message_for_command
from message_flow.commands.consumer import (
    CommandDispatcher,
    CommandWithDestinationBuilder,
)
from message_flow.commands.consumer.command_handlers_builder import (
    CommandHandlersBuilder,
)
from message_flow.events.common.domain_event import DomainEvent
from message_flow.events.common.event_message_headers import EventMessageHeaders
from message_flow.events.publisher import DomainEventPublisher
from message_flow.events.subscriber import DomainEventDispatcher
from message_flow.events.subscriber.domain_event_handlers_builder import (
    DomainEventHandlersBuilder,
)
from tests.factories import (
    CommandFactory,
    CommandMessageFactory,
    EventFactory,
    MessageFactory,
    SimpleEvent,
)
from tests.factories.command import SimpleCommand
from tests.fakes import FakeMessageConsumer, FakeMessageProducer


@pytest.fixture
def queue():
    return Queue()


@pytest.fixture
def producer(queue):
    return FakeMessageProducer(queue)


@pytest.fixture
def consumer(queue):
    return FakeMessageConsumer(queue)


@pytest.fixture
def event_publisher(producer):
    return DomainEventPublisher(producer)


@pytest.fixture
def test_event_message():
    test_message = MessageFactory()
    test_aggregate_type = test_message.get_header(EventMessageHeaders.AGGREGATE_TYPE)
    return test_aggregate_type, test_message


@pytest.fixture
def domain_event_message():
    test_message = MessageFactory()
    test_aggregate_type = test_message.get_header(EventMessageHeaders.AGGREGATE_TYPE)
    test_message.set_header(EventMessageHeaders.EVENT_TYPE, DomainEvent.__name__)
    return test_aggregate_type, test_message


@pytest.fixture
def test_command_message():
    return CommandMessageFactory()


@pytest.fixture
def command_message():
    test_message = CommandMessageFactory()
    test_message.set_header(CommandMessageHeaders.COMMAND_TYPE, Command.__name__)
    return test_message


@pytest.fixture
def callback(queue):
    def cb(message):
        queue.put_nowait(message)

    return cb


@pytest.fixture
def command_callback(queue):
    def cb(message):
        reply = (
            CommandWithDestinationBuilder.send(CommandFactory())
            .to(uuid4().hex)
            .build(),
        )
        return [
            make_message_for_command(
                uuid4().hex,
                json.dumps(asdict(CommandFactory())),
                SimpleCommand.__class__.__name__,
                "NONE",
            )
        ]

    return cb


@pytest.fixture
def event_handlers(test_event_message, callback):
    test_aggregate_type, _ = test_event_message
    builder = DomainEventHandlersBuilder.for_aggregate_type(
        test_aggregate_type
    ).on_event(SimpleEvent, callback)
    return builder.build()


@pytest.fixture
def event_dispatcher(event_handlers, consumer):
    return DomainEventDispatcher(event_handlers, consumer)


@pytest.fixture
def command_handlers(test_command_message, command_callback):
    return (
        CommandHandlersBuilder.from_channel(
            test_command_message.get_header(CommandMessageHeaders.DESTINATION)
        )
        .on_message(SimpleCommand, command_callback)
        .build()
    )


@pytest.fixture
def command_dispatcher(command_handlers, consumer, producer):
    return CommandDispatcher(command_handlers, consumer, producer)


@pytest.fixture
def event_mapper():
    return {SimpleEvent: 1234}


register(MessageFactory)
register(EventFactory)
register(CommandFactory)
register(CommandMessageFactory)
