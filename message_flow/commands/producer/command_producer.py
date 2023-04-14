import logging
from typing import Dict, Optional

from message_flow.commands.common import Command, make_message_for_command
from message_flow.events.mappers.interfaces import ISerializer
from message_flow.events.mappers.json_mapper import JsonMapper
from message_flow.messaging.common.interfaces import IMessage
from message_flow.messaging.producer.message_producer import IMessageProducer

_logger = logging.getLogger(__name__)


class CommandProducer:
    def __init__(
        self,
        message_producer: IMessageProducer,
        *,
        serializer: ISerializer = JsonMapper()
    ) -> None:
        self._message_producer = message_producer
        self._serializer = serializer

    def send(
        self,
        channel: str,
        command: Command,
        reply_to: str,
        *,
        headers: Optional[Dict[str, str]] = None
    ) -> str:
        message: IMessage = make_message_for_command(
            channel,
            self._serializer.serialize(command),
            command.__class__.__name__,
            reply_to,
            headers=headers if headers else {},
        )
        _logger.info(
            "Sending command %s with payload %s...",
            command.__class__.__name__,
            message.payload.decode(),
        )
        self._message_producer.send(channel, message)
        return message.get_id()
