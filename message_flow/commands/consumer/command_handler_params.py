from typing import Dict, Optional

from message_flow.commands.common import CommandMessageHeaders, ReplyMessageHeaders
from message_flow.messaging.common import IMessage


class CommandHandlerParams:
    def __init__(self, message: IMessage) -> None:
        self._correlation_headers = self._get_correlation_headers(message.headers)
        self._default_reply_channel = message.get_header(CommandMessageHeaders.REPLY_TO)

    @property
    def correlation_headers(self) -> Dict[str, str]:
        return self._correlation_headers

    @property
    def default_reply_channel(self) -> Optional[str]:
        return self._default_reply_channel

    def _get_correlation_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        correlation_headers: Dict[str, str] = {
            CommandMessageHeaders.in_reply(key): value
            for key, value in headers.items()
            if key.startswith(CommandMessageHeaders.COMMAND_HEADER_PREFIX)
        }
        correlation_headers[ReplyMessageHeaders.IN_REPLY_TO] = headers.get(
            IMessage.ID, ""
        )
        return correlation_headers
