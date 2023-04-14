from dataclasses import dataclass

import factory

from message_flow.events.common import DomainEvent


@dataclass
class SimpleEvent(DomainEvent):
    aggregate_id: str


class EventFactory(factory.Factory):
    aggregate_id = factory.Faker("uuid4")

    class Meta:
        model = SimpleEvent
