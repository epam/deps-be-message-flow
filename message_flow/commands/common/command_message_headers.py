from message_flow.messaging.exceptions import WrongHeader


class CommandMessageHeaders:
    COMMAND_HEADER_PREFIX: str = "command_"

    COMMAND_TYPE = COMMAND_HEADER_PREFIX + "type"
    RESOURCE = COMMAND_HEADER_PREFIX + "resource"
    DESTINATION = COMMAND_HEADER_PREFIX + "destination"

    COMMAND_REPLY_PREFIX = "commandreply_"
    REPLY_TO = COMMAND_HEADER_PREFIX + "reply_to"

    @staticmethod
    def in_reply(header: str) -> str:
        if not header.startswith(CommandMessageHeaders.COMMAND_HEADER_PREFIX):
            raise WrongHeader(f"Command message contains a wrong header {header}")

        command_prefix_length = len(CommandMessageHeaders.COMMAND_HEADER_PREFIX)
        return (
            CommandMessageHeaders.COMMAND_REPLY_PREFIX + header[command_prefix_length:]
        )
