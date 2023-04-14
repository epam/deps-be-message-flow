from message_flow.commands.common import Failure, Success
from message_flow.sagas.orchestration import *
from message_flow.sagas.orchestration_simple_dsl import *

from ..conditional_saga import *
from .handlers import Handlers

__all__ = ["WithHandlersSaga"]


class WithHandlersSaga(SimpleSaga[ConditionalSagaData]):
    def __init__(self, handlers: Handlers) -> None:
        self._handlers = handlers

        self._saga_definition = (
            self.step()
            .invoke_participant(
                ConditionalSagaData.do1, predicate=ConditionalSagaData.is_invoke1
            )
            .on_reply(Failure, handlers.failure1)
            .on_reply(Success, handlers.success1)
            .with_compensation(
                ConditionalSagaData.undo1,
                compensation_predicate=ConditionalSagaData.is_invoke1,
            )
            .on_reply(Success, handlers.compensating1)
            .step()
            .invoke_participant(ConditionalSagaData.do2)
            .on_reply(Failure, handlers.failure2)
            .on_reply(Success, handlers.success2)
            .build()
        )
