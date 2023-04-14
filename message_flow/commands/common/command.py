from dataclasses import dataclass
from typing import TypeVar


@dataclass
class Command:
    pass


C = TypeVar("C", bound=Command)
