import abc
from typing import Any, Optional, Set


class IMessageConsumer(abc.ABC):
    @abc.abstractmethod
    def subscribe(
        self, channels: Set[str], handler: Any, *, queue: Optional[str] = None
    ) -> None:
        pass
