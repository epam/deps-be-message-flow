__all__ = ["SerializedSagaData"]


class SerializedSagaData:
    def __init__(self, saga_data_type: str, saga_data_json: str) -> None:
        self._saga_data_type = saga_data_type
        self._saga_data_json = saga_data_json

    @property
    def saga_data_type(self) -> str:
        return self._saga_data_type

    @property
    def saga_data_json(self) -> str:
        return self._saga_data_json

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, SerializedSagaData)
            and self.saga_data_type == other.saga_data_type
            and self.saga_data_json == other.saga_data_json
        )
