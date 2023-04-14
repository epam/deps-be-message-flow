from typing import Any, Dict, Tuple
from uuid import uuid4

from message_flow.commands.common import (
    CommandMessageHeaders,
    CommandReplyOutcome,
    Failure,
    ReplyMessageHeaders,
    Success,
)
from message_flow.commands.consumer.command_message import CommandMessage
from message_flow.events.mappers import JsonMapper
from message_flow.messaging.common import IMessage
from message_flow.messaging.producer import MessageBuilder

__all__ = ["PluginReplyBuilder"]


class PluginReplyBuilder:
    def __init__(self, command_message: CommandMessage) -> None:
        self._command_message = command_message

        self._routing_info, self._destination = self._extract_routing_info()

    @classmethod
    def for_command(cls, command_message: CommandMessage) -> "PluginReplyBuilder":
        return cls(command_message)

    def with_success(self, reply: Any = Success()) -> Tuple[str, IMessage]:
        return self._destination, (
            MessageBuilder.with_payload(JsonMapper().serialize(reply))
            .with_header(
                ReplyMessageHeaders.REPLY_OUTCOME, CommandReplyOutcome.SUCCESS.value
            )
            .with_header(ReplyMessageHeaders.REPLY_TYPE, reply.__class__.__name__)
            .with_header(IMessage.ID, uuid4().hex)
            .with_extra_headers("", self._routing_info)
            .build()
        )

    def with_failure(self, reply: Any = Failure()) -> Tuple[str, IMessage]:
        return self._destination, (
            MessageBuilder.with_payload(JsonMapper().serialize(reply))
            .with_header(
                ReplyMessageHeaders.REPLY_OUTCOME, CommandReplyOutcome.FAILURE.value
            )
            .with_header(ReplyMessageHeaders.REPLY_TYPE, reply.__class__.__name__)
            .with_header(IMessage.ID, uuid4().hex)
            .with_extra_headers("", self._routing_info)
            .build()
        )

    def _extract_routing_info(self) -> Tuple[Dict[str, Any], str]:
        headers = self._command_message.message.headers
        if (routing_info := headers.get("routing_info")) is None:
            raise RuntimeError("Please provide routing info in the message.")

        destination = routing_info.get(
            CommandMessageHeaders.in_reply(CommandMessageHeaders.REPLY_TO)
        )

        return routing_info, destination
