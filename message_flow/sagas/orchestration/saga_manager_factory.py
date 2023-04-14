from typing import TypeVar

from ...commands.producer import CommandProducer
from ...messaging.consumer import IMessageConsumer
from .saga import Saga
from .saga_command_producer import SagaCommandProducer
from .saga_data_serde import SagaDataMapping
from .saga_instance_repository import ISagaInstanceRepository
from .saga_manager_impl import SagaManagerImpl

__all__ = ["SagaManagerFactory"]

SagaData = TypeVar("SagaData")


class SagaManagerFactory:
    def __init__(
        self,
        saga_instance_repository: ISagaInstanceRepository,
        command_producer: CommandProducer,
        message_consumer: IMessageConsumer,
        saga_command_producer: SagaCommandProducer,
        saga_data_mapping: SagaDataMapping,
    ) -> None:
        self._saga_instance_repository = saga_instance_repository
        self._command_producer = command_producer
        self._message_consumer = message_consumer
        self._saga_command_producer = saga_command_producer
        self._saga_data_mapping = saga_data_mapping

    def make(self, saga: Saga[SagaData]) -> SagaManagerImpl:
        return SagaManagerImpl(
            saga,
            self._saga_instance_repository,
            self._command_producer,
            self._message_consumer,
            self._saga_command_producer,
            self._saga_data_mapping,
        )
