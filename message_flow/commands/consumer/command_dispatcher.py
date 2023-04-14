import logging
from typing import List, Optional

from message_flow.commands.common.command_message_headers import CommandMessageHeaders
from message_flow.commands.consumer.command_handler import CommandHandler, CommandResult
from message_flow.commands.consumer.command_handler_params import CommandHandlerParams
from message_flow.commands.consumer.command_handlers import CommandHandlers
from message_flow.commands.consumer.command_message import CommandMessage
from message_flow.events.mappers.interfaces import IDeserializer, ISerializer
from message_flow.events.mappers.json_mapper import JsonMapper
from message_flow.messaging.common.interfaces import IMessage
from message_flow.messaging.consumer import IMessageConsumer
from message_flow.messaging.producer import IMessageProducer
from message_flow.messaging.producer.message_builder import MessageBuilder

_logger = logging.getLogger(__name__)


class CommandDispatcher:
    def __init__(
        self,
        command_handlers: CommandHandlers,
        message_consumer: IMessageConsumer,
        message_producer: IMessageProducer,
        *,
        serializer: ISerializer = JsonMapper(),
        deserializer: IDeserializer = JsonMapper()
    ) -> None:
        self._command_handlers = command_handlers
        self._message_consumer = message_consumer
        self._message_producer = message_producer

        self._serializer = serializer
        self._deserializer = deserializer

    @property
    def handlers(self) -> List[CommandHandler]:
        return self._command_handlers.handlers

    def initialize(self) -> None:
        self._message_consumer.subscribe(
            self._command_handlers.channels,
            self.message_handler,
            queue=self._command_handlers.queue,
        )

    def message_handler(self, message: IMessage) -> None:
        _logger.debug(
            "Got command %s, with payload %s.",
            message.get_required_header(CommandMessageHeaders.COMMAND_TYPE),
            message.payload,
        )  # noqa: WPS323
        command_handler: Optional[
            CommandHandler
        ] = self._command_handlers.find_target_method(message)

        if command_handler is None:
            _logger.debug(
                "Command %s doesn't have a handler.",
                message.get_required_header(CommandMessageHeaders.COMMAND_TYPE),
            )  # noqa: WPS323
            return

        command_handler_params = CommandHandlerParams(message)
        command_message = CommandMessage(
            message.get_id(),
            self._deserializer.deserialize(
                command_handler.command_class, message.payload
            ),
            command_handler_params.correlation_headers,
            message,
        )
        replies: CommandResult = self._invoke(command_handler, command_message)

        if replies is None:
            return

        self._send_replies(replies, command_handler_params)
        _logger.info(
            "Command %s, with payload %s processed.",
            message.get_required_header(CommandMessageHeaders.COMMAND_TYPE),
            message.payload,
        )  # noqa: WPS323

    def _invoke(
        self, command_handler: CommandHandler, command_message: CommandMessage
    ) -> CommandResult:
        return command_handler.invoke_method(command_message)

    def _send_replies(
        self, replies: List[IMessage], command_handler_params: CommandHandlerParams
    ) -> None:
        for reply in replies:
            message = (
                MessageBuilder.with_message(reply)
                .with_extra_headers("", command_handler_params.correlation_headers)
                .build()
            )
            self._message_producer.send(command_handler_params.default_reply_channel, message)  # type: ignore
