from typing import Protocol

from message_flow.commands.common import Failure, Success

from ..conditional_saga import *

__all__ = ["Handlers"]


class Handlers(Protocol):
    def success1(data: ConditionalSagaData, m: Success) -> None:
        ...

    def failure1(data: ConditionalSagaData, m: Failure) -> None:
        ...

    def compensating1(data: ConditionalSagaData, m: Failure) -> None:
        ...

    def success2(data: ConditionalSagaData, m: Failure) -> None:
        ...

    def failure2(data: ConditionalSagaData, m: Failure) -> None:
        ...
