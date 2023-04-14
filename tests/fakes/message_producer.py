from queue import Queue
from typing import List, Tuple

from message_flow.messaging.common import IMessage
from message_flow.messaging.producer import IMessageProducer

MessageInfo = Tuple[str, IMessage]


class FakeMessageProducer(IMessageProducer):
    def __init__(self, queue: Queue) -> None:
        self._queue = queue

    def send(self, destination: str, message: IMessage) -> None:
        self._queue.put_nowait(message)


class FakeMessageListProducer(IMessageProducer):
    def __init__(self, message_queue: List[MessageInfo]) -> None:
        self._producer_messages = message_queue

    def send(self, destination: str, message: IMessage) -> None:
        self._producer_messages.append((destination, message))
