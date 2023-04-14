from queue import Empty, Queue
from typing import Any, Optional, Set

from message_flow.messaging.consumer import IMessageConsumer


class FakeMessageConsumer(IMessageConsumer):
    def __init__(self, queue: Queue) -> None:
        self._queue = queue

    def subscribe(
        self, channels: Set[str], handler: Any, *, queue: Optional[str] = None
    ) -> None:
        pass
