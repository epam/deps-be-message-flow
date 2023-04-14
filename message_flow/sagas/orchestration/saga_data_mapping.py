from typing import Any, Dict, Type, TypeVar

__all__ = ["SagaDataMapping"]


class SagaDataMapping:
    def __init__(self, mapping: Dict[str, Type[Any]]) -> None:
        self._mapping = mapping

    def map(self, class_name: str) -> Type[Any]:
        if (mapped_class := self._mapping.get(class_name)) is None:
            raise RuntimeError(f"No mapping for class {class_name}")

        return mapped_class
