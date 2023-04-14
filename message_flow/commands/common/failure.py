from dataclasses import dataclass

from .outcome import Outcome

__all__ = ["Failure"]


@dataclass
class Failure(Outcome):
    ...
