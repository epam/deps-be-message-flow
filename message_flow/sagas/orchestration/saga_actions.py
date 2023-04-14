from typing import Any, Final, Generic, List, Optional, TypeVar

from message_flow.commands.consumer.command_with_destination import (
    CommandWithDestination,
)

__all__ = ["SagaActions"]


Data = TypeVar("Data")


class SagaActions(Generic[Data]):
    def __init__(
        self,
        commands: List[CommandWithDestination],
        updated_saga_data: Optional[Data],
        updated_state: Optional[str],
        end_state: bool,
        compensating: bool,
        failed: bool,
        local: bool,
        local_exception: Optional[RuntimeError],
    ) -> None:
        self._commands = commands
        self._updated_saga_data = updated_saga_data
        self._updated_state = updated_state
        self._end_state = end_state
        self._compensating = compensating
        self._local = local
        self._local_exception = local_exception
        self._failed = failed

    @property
    def commands(self) -> List[CommandWithDestination]:
        return self._commands

    @property
    def updated_saga_data(self) -> Optional[Data]:
        return self._updated_saga_data

    @property
    def updated_state(self) -> str:
        if self._updated_state is None:
            raise RuntimeError("No updated state.")

        return self._updated_state

    @property
    def is_end_state(self) -> bool:
        return self._end_state

    @property
    def is_compensating(self) -> bool:
        return self._compensating

    @property
    def is_local(self) -> bool:
        return self._local

    @property
    def is_failed(self) -> bool:
        return self._failed

    @property
    def local_exception(self) -> Optional[RuntimeError]:
        return self._local_exception

    class Builder:
        def __init__(self) -> None:
            self._commands: List[CommandWithDestination] = []
            self._updated_saga_data: Optional[Any] = None
            self._updated_state: Optional[str] = None
            self._end_state: bool = False
            self._compensating: bool = False
            self._local: bool = False
            self._failed: bool = False
            self._local_exception: Optional[RuntimeError] = None

        def build(self) -> "SagaActions[Any]":
            return SagaActions(
                self._commands,
                self._updated_saga_data,
                self._updated_state,
                self._end_state,
                self._compensating,
                self._failed,
                self._local,
                self._local_exception,
            )

        def with_command(
            self, command: CommandWithDestination
        ) -> "SagaActions.Builder":
            self._commands.append(command)
            return self

        def with_updated_saga_data(self, data: Data) -> "SagaActions.Builder":
            self._updated_saga_data = data
            return self

        def with_updated_state(self, state: str) -> "SagaActions.Builder":
            self._updated_state = state
            return self

        def with_commands(
            self, commands: List[CommandWithDestination]
        ) -> "SagaActions.Builder":
            self._commands.extend(commands)
            return self

        def with_is_end_state(self, end_state: bool) -> "SagaActions.Builder":
            self._end_state = end_state
            return self

        def with_is_failed(self, failed: bool) -> "SagaActions.Builder":
            self._failed = failed
            return self

        def with_is_compensating(self, compensating: bool) -> "SagaActions.Builder":
            self._compensating = compensating
            return self

        def with_is_local(
            self, local_exception: Optional[RuntimeError]
        ) -> "SagaActions.Builder":
            self._local = True
            self._local_exception = local_exception
            return self

        def build_actions(
            self, data: Data, compensating: bool, state: str, end_state: bool
        ) -> "SagaActions[Data]":
            return (
                self.with_updated_saga_data(data)
                .with_updated_state(state)
                .with_is_end_state(end_state)
                .with_is_compensating(compensating)
                .build()
            )

    @classmethod
    def builder(cls) -> "Builder":
        return cls.Builder()
