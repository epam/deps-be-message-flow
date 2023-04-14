from message_flow.sagas.orchestration import *
from message_flow.sagas.orchestration_simple_dsl import *

from .local_saga_data import LocalSagaData
from .local_saga_steps import LocalSagaSteps

__all__ = ["LocalSaga"]


class LocalSaga(SimpleSaga[LocalSagaData]):
    def __init__(self, steps: LocalSagaSteps) -> None:
        self._saga_definition = (
            self.step()
            .invoke_local(steps.local_step1)
            .with_compensation(steps.local_step1_compensation)
            .step()
            .invoke_participant(LocalSagaData.do2)
            .with_compensation(LocalSagaData.undo2)
            .step()
            .invoke_local(steps.local_step3)
            .build()
        )
