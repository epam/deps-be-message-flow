from typing import Callable, List, Optional, Type

from message_flow.commands.common import C
from message_flow.commands.consumer.command_handler import CommandHandler, Handler
from message_flow.commands.consumer.command_handlers import CommandHandlers


class CommandHandlersBuilder:
    def __init__(self, channel: str) -> None:
        self._channel = channel

        self._queue: str = ""
        self._handlers: List[CommandHandler] = []

    @classmethod
    def from_channel(cls, channel: str) -> "CommandHandlersBuilder":
        return cls(channel)

    def and_from_channel(self, channel: str) -> "CommandHandlersBuilder":
        self._channel = channel
        return self

    def for_queue(self, queue: str) -> "CommandHandlersBuilder":
        self._queue = queue
        return self

    def on_message(
        self, command_class: Type[C], handler: Handler
    ) -> "CommandHandlersBuilder":
        self._handlers.append(CommandHandler[C](self._channel, command_class, handler))
        return self

    def build(self) -> CommandHandlers:
        return CommandHandlers(self._handlers, queue=self._queue)
