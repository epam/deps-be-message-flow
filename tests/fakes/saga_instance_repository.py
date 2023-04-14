from uuid import uuid4

from message_flow.sagas.orchestration import ISagaInstanceRepository, SagaInstance


class FakeSagaInstanceRepository(ISagaInstanceRepository):
    def __init__(self) -> None:
        self._db = {}

    def save(self, saga_instance: SagaInstance) -> SagaInstance:
        saga_instance.saga_id = uuid4().hex
        self._db[saga_instance.saga_id] = saga_instance
        return saga_instance

    def find(self, saga_id: str) -> SagaInstance:
        return self._db[saga_id]

    def update(self, saga_instance: SagaInstance) -> SagaInstance:
        self._db[saga_instance.saga_id] = saga_instance
        return saga_instance
