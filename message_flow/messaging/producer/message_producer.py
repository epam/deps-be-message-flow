import abc

from message_flow.messaging.common import IMessage


class IMessageProducer(abc.ABC):
    @abc.abstractmethod
    def send(self, destination: str, message: IMessage) -> None:
        pass
