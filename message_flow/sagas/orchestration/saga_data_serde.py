import json
from typing import TypeVar

from .saga_data_mapping import SagaDataMapping
from .serialized_saga_data import SerializedSagaData

__all__ = ["SagaDataSerde"]

Data = TypeVar("Data")


class SagaDataSerde:
    @staticmethod
    def serialize_saga_data(saga_data: Data) -> SerializedSagaData:
        return SerializedSagaData(saga_data.__class__.__name__, json.dumps(saga_data.to_dict()))  # type: ignore

    @staticmethod
    def deserialize_saga_data(
        serialized_saga_data: SerializedSagaData, saga_data_mapping: SagaDataMapping
    ) -> Data:
        mapped_class = saga_data_mapping.map(serialized_saga_data.saga_data_type)
        return mapped_class.from_dict(json.loads(serialized_saga_data.saga_data_json))  # type: ignore
