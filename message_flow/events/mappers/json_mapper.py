import json
from dataclasses import asdict
from typing import Type, Union

from message_flow.commands.common import C
from message_flow.events.common import DE
from message_flow.events.mappers.interfaces import IDeserializer, ISerializer, T


class JsonMapper(ISerializer, IDeserializer):
    def serialize(self, obj: T) -> bytes:
        return json.dumps(asdict(obj)).encode()

    def deserialize(self, obj_class: Type[T], payload: bytes) -> T:
        return obj_class(**json.loads(payload))  # type: ignore
