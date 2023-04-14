from dataclasses import dataclass

from .outcome import Outcome

__all__ = ["Success"]


@dataclass
class Success(Outcome):
    ...
