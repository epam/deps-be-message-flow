from message_flow.sagas.orchestration import *
from message_flow.sagas.orchestration_simple_dsl import *

from .conditional_saga_data import ConditionalSagaData

__all__ = ["ConditionalSaga"]


class ConditionalSaga(SimpleSaga[ConditionalSagaData]):
    def __init__(self) -> None:
        self._saga_definition = (
            self.step()
            .invoke_participant(
                ConditionalSagaData.do1, predicate=ConditionalSagaData.is_invoke1
            )
            .with_compensation(
                ConditionalSagaData.undo1,
                compensation_predicate=ConditionalSagaData.is_invoke1,
            )
            .step()
            .invoke_participant(ConditionalSagaData.do2)
            .build()
        )
