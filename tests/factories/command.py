from dataclasses import dataclass

import factory

from message_flow.commands.common import Command


@dataclass
class SimpleCommand(Command):
    document_id: str


class CommandFactory(factory.Factory):
    document_id = factory.Faker("uuid4")

    class Meta:
        model = SimpleCommand
