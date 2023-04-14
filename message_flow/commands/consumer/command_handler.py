from typing import Callable, Generic, List, Optional, Type

from message_flow.commands.common import C, CommandMessageHeaders
from message_flow.commands.consumer.command_message import CommandMessage
from message_flow.messaging.common import IMessage

CommandResult = Optional[List[IMessage]]
Handler = Callable[[CommandMessage[C]], CommandResult]


class CommandHandler(Generic[C]):
    def __init__(
        self,
        channel: str,
        command_class: Type[C],
        handler: Handler,
    ) -> None:
        self._channel = channel
        self._command_class = command_class
        self._handler = handler

    @property
    def channel(self) -> str:
        return self._channel

    @property
    def command_class(self) -> Type[C]:
        return self._command_class

    def handles(self, message: IMessage) -> bool:
        return self._command_class.__name__ == message.get_required_header(
            CommandMessageHeaders.COMMAND_TYPE
        )

    def invoke_method(self, command_message: CommandMessage) -> CommandResult:
        return self._handler(command_message)
