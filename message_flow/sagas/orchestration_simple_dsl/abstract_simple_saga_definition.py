import abc
import json
import logging
from typing import Any, Callable, Generic, List, TypeVar

from message_flow.sagas.orchestration_simple_dsl.saga_execution_state_json_serde import (
    SagaExecutionStateJsonSerde,
)

from ...messaging.common import IMessage
from ..orchestration import SagaActions  # type: ignore
from .abstract_saga_actions_provider import AbstractSagaActionsProvider
from .abstract_step_to_execute import AbstractStepToExecute
from .isaga_step import ISagaStep
from .reply_handler import ReplyHandler
from .saga_execution_state import SagaExecutionState

__all__ = ["AbstractSimpleSagaDefinition"]

T = TypeVar("T")
Data = TypeVar("Data")
Step = TypeVar("Step", bound=ISagaStep)
ToExecute = TypeVar("ToExecute", bound=AbstractStepToExecute)
Provider = TypeVar("Provider", bound=AbstractSagaActionsProvider)


class AbstractSimpleSagaDefinition(abc.ABC, Generic[Data, Step, ToExecute, Provider]):
    def __init__(self, steps: List[Step]) -> None:
        self._steps = steps

        self._logger = logging.getLogger(self.__class__.__name__)

    def _first_step_to_execute(self, data: Data) -> Provider:
        return self._next_step_to_execute(SagaExecutionState(), data)

    def _handle_failed_compensation_transaction(
        self, saga_type: str, saga_id: str, state: SagaExecutionState, message: IMessage
    ) -> Provider:
        self._logger.error(
            "Saga %s %s failed due to failed compensating transaction %s",
            saga_type,
            saga_id,
            message,
        )
        return self._make_saga_actions_provider(
            SagaActions.builder()
            .with_updated_state(
                SagaExecutionStateJsonSerde.encode_state(
                    SagaExecutionState.make_failed_end_state()
                )
            )
            .with_is_end_state(True)
            .with_is_compensating(state.compensating)
            .with_is_failed(True)
            .build()
        )

    def _saga_actions_for_next_step(
        self,
        saga_type: str,
        saga_id: str,
        saga_data: Data,
        message: IMessage,
        state: SagaExecutionState,
        current_step: Step,
        compensating: bool,
    ) -> Provider:
        if current_step.is_successful_reply(compensating, message):
            return self._next_step_to_execute(state, saga_data)
        elif compensating:
            return self._handle_failed_compensation_transaction(
                saga_type, saga_id, state, message
            )
        else:
            return self._next_step_to_execute(state.start_compensating(), saga_data)

    def _next_step_to_execute(self, state: SagaExecutionState, data: Data) -> Provider:
        skipped: int = 0
        compensating: bool = state.compensating
        direction: int = -1 if compensating else +1

        currently_executing = state.currently_executing + direction

        while currently_executing >= 0 and currently_executing < len(self._steps):
            step: Step = self._steps[currently_executing]

            if step.has_compensation(data) if compensating else step.has_action(data):
                step_to_execute: ToExecute = self._make_step_to_execute(
                    skipped, compensating, step
                )
                return self._make_saga_actions_provider_from_step(
                    step_to_execute, data, state
                )
            else:
                skipped += 1

            currently_executing += direction

        return self._make_saga_actions_provider(
            self._make_end_state_saga_actions(state)
        )

    def _invoke_reply_handler(
        self, message: IMessage, data: Data, handler: ReplyHandler
    ) -> None:
        reply = handler.reply_class(**json.loads(message.payload))  # type: ignore
        handler(data, reply)

    def _make_end_state_saga_actions(
        self, state: SagaExecutionState
    ) -> SagaActions[Data]:
        return (
            SagaActions.builder()
            .with_updated_state(
                SagaExecutionStateJsonSerde.encode_state(
                    SagaExecutionState.make_end_state()
                )
            )
            .with_is_end_state(True)
            .with_is_compensating(state.compensating)
            .build()
        )

    @abc.abstractmethod
    def _make_step_to_execute(
        self, skipped: int, compensating: bool, step: Step
    ) -> ToExecute:
        ...

    @abc.abstractmethod
    def _make_saga_actions_provider(self, saga_actions: SagaActions[Data]) -> Provider:
        ...

    @abc.abstractmethod
    def _make_saga_actions_provider_from_step(
        self, stet_to_execute: ToExecute, data: Data, state: SagaExecutionState
    ) -> Provider:
        ...
