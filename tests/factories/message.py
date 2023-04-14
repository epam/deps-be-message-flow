import json
from dataclasses import asdict
from uuid import uuid4

import factory

from message_flow.commands.common import CommandMessageHeaders
from message_flow.events.common.event_message_headers import EventMessageHeaders
from message_flow.messaging.common import Message
from tests.factories.command import CommandFactory, SimpleCommand
from tests.factories.event import EventFactory, SimpleEvent


class MessageFactory(factory.Factory):
    payload = factory.LazyFunction(lambda: json.dumps(asdict(EventFactory())).encode())
    headers = factory.Dict(
        {
            Message.ID: uuid4().hex,
            EventMessageHeaders.AGGREGATE_ID: uuid4().hex,
            EventMessageHeaders.AGGREGATE_TYPE: uuid4().hex,
            EventMessageHeaders.EVENT_TYPE: SimpleEvent.__name__,
        }
    )

    class Meta:
        model = Message


class CommandMessageFactory(factory.Factory):
    payload = factory.LazyFunction(
        lambda: json.dumps(asdict(CommandFactory())).encode()
    )
    headers = factory.Dict(
        {
            Message.ID: uuid4().hex,
            CommandMessageHeaders.DESTINATION: uuid4().hex,
            CommandMessageHeaders.REPLY_TO: uuid4().hex,
            CommandMessageHeaders.COMMAND_TYPE: SimpleCommand.__name__,
        }
    )

    class Meta:
        model = Message
