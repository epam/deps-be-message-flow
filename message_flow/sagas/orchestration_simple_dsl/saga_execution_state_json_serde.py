import json
from typing import Any, Dict

from .saga_execution_state import SagaExecutionState

__all__ = ["SagaExecutionStateJsonSerde"]


class SagaExecutionStateJsonSerde:
    @staticmethod
    def encode_state(state: SagaExecutionState) -> str:
        return json.dumps(SagaExecutionStateJsonSerde.to_dict(state))

    @staticmethod
    def to_dict(state: SagaExecutionState) -> Dict[str, Any]:
        return {
            "currently_executing": state.currently_executing,
            "compensating": state.compensating,
            "end_state": state.end_state,
            "failed": state.failed,
        }

    @staticmethod
    def decode_state(current_state: str) -> SagaExecutionState:
        return SagaExecutionStateJsonSerde.from_dict(json.loads(current_state))

    @staticmethod
    def from_dict(state: Dict[str, Any]) -> SagaExecutionState:
        saga_execution_state = SagaExecutionState(
            state.get("currently_executing", -1),
            state.get("compensating", False),
        )
        saga_execution_state.end_state = state.get("end_state", False)
        saga_execution_state.failed = state.get("failed", False)

        return saga_execution_state
