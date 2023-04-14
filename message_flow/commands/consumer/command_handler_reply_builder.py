from message_flow.commands.common import (
    CommandMessageHeaders,
    CommandReplyOutcome,
    ReplyMessageHeaders,
)
from message_flow.messaging.common import IMessage
from message_flow.messaging.producer import MessageBuilder


class CommandHandlerReplyBuilder:
    @staticmethod
    def _with(reply: IMessage, outcome: CommandReplyOutcome) -> IMessage:
        return (
            MessageBuilder.with_message(reply)
            .with_header(
                ReplyMessageHeaders.REPLY_TYPE,
                reply.get_required_header(CommandMessageHeaders.COMMAND_TYPE),
            )
            .with_header(ReplyMessageHeaders.REPLY_OUTCOME, outcome.name)
            .build()
        )

    @staticmethod
    def with_success(reply: IMessage) -> IMessage:
        return CommandHandlerReplyBuilder._with(reply, CommandReplyOutcome.SUCCESS)

    @staticmethod
    def with_failure(reply: IMessage) -> IMessage:
        return CommandHandlerReplyBuilder._with(reply, CommandReplyOutcome.FAILURE)
