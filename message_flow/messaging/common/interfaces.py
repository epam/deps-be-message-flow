import abc
from typing import Any, Dict, Optional, Union


class IMessage(abc.ABC):
    ID: str = "ID"

    @abc.abstractproperty
    def payload(self) -> bytes:
        ...

    @abc.abstractproperty
    def headers(self) -> Dict[str, Any]:
        ...

    @abc.abstractmethod
    def get_id(self) -> str:
        ...

    @abc.abstractmethod
    def get_header(self, name: str) -> Optional[str]:
        ...

    @abc.abstractmethod
    def get_required_header(self, name: str) -> str:
        ...

    @abc.abstractmethod
    def has_header(self, name: str) -> bool:
        ...

    @abc.abstractmethod
    def set_header(self, name: str, value: str) -> None:
        ...

    @abc.abstractmethod
    def remove_header(self, name: str) -> None:
        ...
