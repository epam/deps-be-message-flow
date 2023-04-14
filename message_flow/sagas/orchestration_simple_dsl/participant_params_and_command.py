from typing import Dict, Generic, TypeVar

from ...commands.common import Command

__all__ = ["ParticipantParamsAndCommand"]

C = TypeVar("C", bound=Command)


class ParticipantParamsAndCommand(Generic[C]):
    def __init__(self, params: Dict[str, str], command: C) -> None:
        self._params = params
        self._command = command

    @property
    def params(self) -> Dict[str, str]:
        return self._params

    @property
    def command(self) -> C:
        return self._command
