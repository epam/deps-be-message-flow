from typing import Final

from message_flow.commands.common import CommandMessageHeaders
from message_flow.sagas.common.saga_command_headers import SagaCommandHeaders

__all__ = ["SagaReplyHeaders"]


class SagaReplyHeaders:
    REPLY_SAGA_TYPE: Final[str] = CommandMessageHeaders.in_reply(
        SagaCommandHeaders.SAGA_TYPE
    )
    REPLY_SAGA_ID: Final[str] = CommandMessageHeaders.in_reply(
        SagaCommandHeaders.SAGA_ID
    )
