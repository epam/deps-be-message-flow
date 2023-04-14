from typing import Any, Dict

__all__ = ["SagaExecutionState"]


class SagaExecutionState:
    def __init__(
        self, currently_executing: int = -1, compensating: bool = False
    ) -> None:
        self.currently_executing = currently_executing
        self.compensating = compensating
        self.end_state: bool = False
        self.failed: bool = False

    def start_compensating(self) -> "SagaExecutionState":
        return SagaExecutionState(self.currently_executing, True)

    def next_state(self, size: int) -> "SagaExecutionState":
        return SagaExecutionState(
            self.currently_executing - size
            if self.compensating
            else self.currently_executing + size,
            self.compensating,
        )

    @classmethod
    def make_end_state(self) -> "SagaExecutionState":
        ses = SagaExecutionState()
        ses.end_state = True
        return ses

    @classmethod
    def make_failed_end_state(self) -> "SagaExecutionState":
        ses = SagaExecutionState()
        ses.end_state = True
        ses.failed = True
        return ses
