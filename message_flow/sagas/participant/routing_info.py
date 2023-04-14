from typing import Any, Dict

from message_flow.commands.consumer import CommandMessage

__all__ = ["make_routing_info"]


def make_routing_info(command_message: CommandMessage) -> Dict[str, Any]:
    return {"routing_info": command_message.correlation_headers}
