from typing import Any, Dict, Optional

from message_flow.messaging.common.interfaces import IMessage
from message_flow.messaging.exceptions import HeaderNotFound


class Message(IMessage):
    def __init__(self, payload: bytes, headers: Dict[str, str]) -> None:
        self._payload = payload
        self._headers = headers

    def __str__(self) -> str:
        return f"{self._payload!r}"

    @property
    def payload(self) -> bytes:
        return self._payload

    @payload.setter
    def payload(self, payload: bytes) -> None:
        self._payload = payload

    @property
    def headers(self) -> Dict[str, Any]:
        return self._headers

    @headers.setter
    def headers(self, headers: Dict[str, str]) -> None:
        self._headers = headers

    def get_id(self) -> str:
        return self.get_required_header(Message.ID)

    def get_header(self, name: str) -> Optional[str]:
        return self._headers.get(name)

    def get_required_header(self, name: str) -> str:
        value = self._headers.get(name)

        if value is None:
            raise HeaderNotFound(f"No such header: {name} in this message {self}")

        return value

    def has_header(self, name: str) -> bool:
        return name in self._headers

    def set_header(self, name: str, value: str) -> None:
        self._headers[name] = value

    def remove_header(self, name: str) -> None:
        del self._headers[name]
