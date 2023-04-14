from typing import TypeVar

from ...commands.common import Command
from .participant_params_and_command import ParticipantParamsAndCommand

__all__ = ["ParticipantInvocationBuilder"]


C = TypeVar("C", bound=Command)


class ParticipantInvocationBuilder:
    def __init__(self, key: str, value: str) -> None:
        self._params = {key: value}

    def with_command(self, command: C) -> ParticipantParamsAndCommand[C]:
        return ParticipantParamsAndCommand[C](self._params, command)
