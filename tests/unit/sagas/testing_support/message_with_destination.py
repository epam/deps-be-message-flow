from message_flow.messaging.common import IMessage

__all__ = ["MessageWithDestination"]


class MessageWithDestination:
    def __init__(self, destination: str, message: IMessage) -> None:
        self.destination = destination
        self.message = message

    def __str__(self) -> str:
        return f"<Destination: {self.destination}, Message: {self.message.payload}>"
