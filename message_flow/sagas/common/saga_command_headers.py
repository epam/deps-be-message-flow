from typing import Final

from message_flow.commands.common import CommandMessageHeaders

__all__ = ["SagaCommandHeaders"]


class SagaCommandHeaders:
    SAGA_TYPE: Final[str] = CommandMessageHeaders.COMMAND_HEADER_PREFIX + "saga_type"
    SAGA_ID: Final[str] = CommandMessageHeaders.COMMAND_HEADER_PREFIX + "saga_id"
