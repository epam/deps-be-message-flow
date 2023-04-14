from typing import Protocol, TypeVar

from message_flow.messaging.common import IMessage
from message_flow.sagas.orchestration.saga_actions import SagaActions

__all__ = ["SagaDefinition"]

Data = TypeVar("Data")


class SagaDefinition(Protocol[Data]):
    def start(self, saga_data: Data) -> SagaActions[Data]:
        ...

    def handle_reply(
        self,
        saga_type: str,
        saga_id: str,
        current_state: str,
        saga_data: Data,
        message: IMessage,
    ) -> SagaActions[Data]:
        ...
