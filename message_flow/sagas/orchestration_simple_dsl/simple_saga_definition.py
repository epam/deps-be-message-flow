from typing import Generic, List, TypeVar

from ...messaging.common import IMessage
from ..orchestration import SagaActions  # type: ignore
from .abstract_simple_saga_definition import AbstractSimpleSagaDefinition
from .saga_actions_provider import SagaActionsProvider
from .saga_execution_state import SagaExecutionState
from .saga_execution_state_json_serde import SagaExecutionStateJsonSerde
from .saga_step import SagaStep
from .step_to_execute import StepToExecute

__all__ = ["SimpleSagaDefinition"]

Data = TypeVar("Data")


class SimpleSagaDefinition(
    AbstractSimpleSagaDefinition[
        Data, SagaStep[Data], StepToExecute[Data], SagaActionsProvider[Data]
    ],
    Generic[Data],
):
    def __init__(self, steps: List[SagaStep[Data]]) -> None:
        super().__init__(steps)

    def start(self, saga_data: Data) -> SagaActions[Data]:
        return self._to_saga_actions(self._first_step_to_execute(saga_data))

    def handle_reply(
        self,
        saga_type: str,
        saga_id: str,
        current_state: str,
        saga_data: Data,
        message: IMessage,
    ) -> SagaActions[Data]:
        state: SagaExecutionState = SagaExecutionStateJsonSerde.decode_state(
            current_state
        )
        current_step: SagaStep[Data] = self._steps[state.currently_executing]
        compensating: bool = state.compensating

        reply_handler = current_step.get_reply_handler(message, compensating)
        if reply_handler is not None:
            self._invoke_reply_handler(message, saga_data, reply_handler)

        sap: SagaActionsProvider[Data] = self._saga_actions_for_next_step(
            saga_type, saga_id, saga_data, message, state, current_step, compensating
        )
        return self._to_saga_actions(sap)

    def _to_saga_actions(self, sap: SagaActionsProvider[Data]) -> SagaActions[Data]:
        return sap.to_saga_actions(lambda x: x, lambda x: x)

    def _make_saga_actions_provider(
        self, saga_actions: SagaActions[Data]
    ) -> SagaActionsProvider[Data]:
        return SagaActionsProvider[Data].from_actions(saga_actions)

    def _make_saga_actions_provider_from_step(
        self,
        stet_to_execute: StepToExecute[Data],
        data: Data,
        state: SagaExecutionState,
    ) -> SagaActionsProvider[Data]:
        return SagaActionsProvider[Data].from_actions(
            stet_to_execute.execute_step(data, state)
        )

    def _make_step_to_execute(
        self, skipped: int, compensating: bool, step: SagaStep[Data]
    ) -> StepToExecute[Data]:
        return StepToExecute[Data](step, skipped, compensating)
