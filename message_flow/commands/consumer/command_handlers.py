from typing import List, Optional, Set

from message_flow.commands.consumer.command_handler import CommandHandler
from message_flow.messaging.common import IMessage


class CommandHandlers:
    def __init__(
        self, handlers: List[CommandHandler], *, queue: Optional[str] = None
    ) -> None:
        self._handlers = handlers
        self._queue = queue if queue else ""

    @property
    def channels(self) -> Set[str]:
        return {handler.channel for handler in self._handlers}

    @property
    def handlers(self) -> List[CommandHandler]:
        return self._handlers

    @property
    def queue(self) -> str:
        return self._queue

    def find_target_method(self, message: IMessage) -> Optional[CommandHandler]:
        return next(filter(lambda h: h.handles(message), self._handlers), None)  # type: ignore
