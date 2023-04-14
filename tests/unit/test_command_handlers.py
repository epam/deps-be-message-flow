from uuid import uuid4

from message_flow.commands.consumer import CommandHandlersBuilder
from message_flow.commands.consumer.command_handler import CommandHandler
from tests.factories import CommandMessageFactory
from tests.factories.command import Command, SimpleCommand


def test__command_handler__handles():
    test_message = CommandMessageFactory()

    test_handler = CommandHandler("test_channel", SimpleCommand, lambda x: x)

    assert test_handler.handles(test_message)


def test__domain_command_handler__not_handles():
    test_message = CommandMessageFactory()

    test_handler = CommandHandler("test_channel", Command, lambda x: x)

    assert not test_handler.handles(test_message)


def test__domain_command_handlers_builder(command_message):
    test_message_1 = CommandMessageFactory()
    test_message_2 = command_message
    test_queue = uuid4().hex
    channel1, channel2 = uuid4().hex, uuid4().hex

    builder = CommandHandlersBuilder.from_channel(channel1).on_message(
        SimpleCommand, lambda x: x
    )
    builder = builder.and_from_channel(channel2).on_message(Command, lambda x: x)
    builder = builder.for_queue(test_queue)
    command_handlers = builder.build()

    assert {channel1, channel2} == command_handlers.channels
    assert test_queue == command_handlers.queue
    assert command_handlers.find_target_method(test_message_1)
    assert command_handlers.find_target_method(test_message_2)


def test__domain_command_handlers_builder__not_find_method(command_message):
    channel = uuid4().hex

    builder = CommandHandlersBuilder.from_channel(channel).on_message(
        SimpleCommand, lambda x: x
    )
    command_handlers = builder.build()

    assert command_handlers.find_target_method(command_message) is None
