from .serialized_saga_data import SerializedSagaData

__all__ = ["SagaInstance"]


class SagaInstance:
    def __init__(
        self,
        saga_type: str,
        saga_id: str,
        state_name: str,
        last_request_id: str,
        serialized_saga_data: SerializedSagaData,
        end_state: bool = False,
        compensating: bool = False,
        failed: bool = False,
    ) -> None:
        self.saga_type = saga_type
        self.saga_id = saga_id
        self.state_name = state_name
        self.last_request_id = last_request_id
        self.serialized_saga_data = serialized_saga_data
        self.end_state = end_state
        self.compensating = compensating
        self.failed = failed

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SagaInstance) and self.saga_id == other.saga_id
