from dataclasses import dataclass
from typing import TypeVar


@dataclass
class DomainEvent:
    pass


DE = TypeVar("DE", bound=DomainEvent)
