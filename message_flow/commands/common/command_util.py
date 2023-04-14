from typing import Dict
from uuid import uuid4

from message_flow.commands.common import CommandMessageHeaders
from message_flow.messaging.common import IMessage
from message_flow.messaging.producer import MessageBuilder


def make_message_for_command(
    channel: str,
    payload: bytes,
    command_type: str,
    reply_to: str,
    *,
    headers: Dict[str, str] = {},
) -> IMessage:
    return (
        MessageBuilder.with_payload(payload)
        .with_extra_headers("", headers)
        .with_header(CommandMessageHeaders.DESTINATION, channel)
        .with_header(CommandMessageHeaders.COMMAND_TYPE, command_type)
        .with_header(CommandMessageHeaders.REPLY_TO, reply_to)
        .with_header(IMessage.ID, uuid4().hex)
        .build()
    )
