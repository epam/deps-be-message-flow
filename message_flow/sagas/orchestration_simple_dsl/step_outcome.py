import abc
from typing import Callable, List, Optional, Protocol

from ...commands.consumer import CommandWithDestination

__all__ = ["IStepOutcome", "StepOutcome"]


class IStepOutcome(Protocol):
    def visit(
        self,
        local_consumer: Callable[[Optional[RuntimeError]], None],
        commands_consumer: Callable[[List[CommandWithDestination]], None],
    ) -> None:
        ...


class StepOutcome:
    @classmethod
    def make_local_outcome(
        cls, local_outcome: Optional[RuntimeError] = None
    ) -> IStepOutcome:
        return cls.LocalStepOutcome(local_outcome)

    @classmethod
    def make_remote_outcome(
        cls, commands_to_send: List[CommandWithDestination]
    ) -> IStepOutcome:
        return cls.RemoteStepOutcome(commands_to_send)

    class LocalStepOutcome:
        def __init__(self, local_outcome: Optional[RuntimeError] = None) -> None:
            self._local_outcome = local_outcome

        def visit(
            self,
            local_consumer: Callable[[Optional[RuntimeError]], None],
            commands_consumer: Callable[[List[CommandWithDestination]], None],
        ) -> None:
            local_consumer(self._local_outcome)

    class RemoteStepOutcome:
        def __init__(self, commands_to_send: List[CommandWithDestination]) -> None:
            self._commands_to_send = commands_to_send

        def visit(
            self,
            local_consumer: Callable[[Optional[RuntimeError]], None],
            commands_consumer: Callable[[List[CommandWithDestination]], None],
        ) -> None:
            commands_consumer(self._commands_to_send)
