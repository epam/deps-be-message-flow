from typing import Dict

from message_flow.messaging.common import IMessage, Message


class MessageBuilder:
    def __init__(self, body: bytes, *, headers: Dict[str, str] = None) -> None:
        self._body = body
        self._headers = headers if headers is not None else {}

    @classmethod
    def with_message(cls, message: IMessage) -> "MessageBuilder":
        return cls(message.payload, headers=message.headers)

    @classmethod
    def with_payload(cls, payload: bytes) -> "MessageBuilder":
        return cls(payload)

    def with_header(self, name: str, value: str) -> "MessageBuilder":
        self._headers[name] = value
        return self

    def with_extra_headers(
        self, prefix: str, headers: Dict[str, str]
    ) -> "MessageBuilder":
        for key, value in headers.items():
            self._headers[prefix + key] = value

        return self

    def build(self) -> IMessage:
        return Message(self._body, self._headers)
