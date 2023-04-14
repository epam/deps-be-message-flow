from unittest.mock import Mock

from ..testing_support import *
from .commands import *
from .conditional_saga import *
from .with_handlers_saga import *


def test_should_execute_all_steps_successfully():
    handlers = Mock(Handlers)

    (
        SagaUnitTestSupport.given()
        .saga(WithHandlersSaga(handlers), ConditionalSagaData(True))
        .expect()
        .command(Do1Command())
        .to("participant1")
        .and_given()
        .success_reply()
        .expect()
        .command(Do2Command())
        .to("participant2")
        .and_given()
        .success_reply()
        .expect_completed_successfully()
    )

    assert 1 == handlers.success1.call_count
    assert 1 == handlers.success2.call_count


def test_should_rollback():
    handlers = Mock(Handlers)

    (
        SagaUnitTestSupport.given()
        .saga(WithHandlersSaga(handlers), ConditionalSagaData(True))
        .expect()
        .command(Do1Command())
        .to("participant1")
        .and_given()
        .success_reply()
        .expect()
        .command(Do2Command())
        .to("participant2")
        .and_given()
        .failure_reply()
        .expect()
        .command(Undo1Command())
        .to("participant1")
        .and_given()
        .success_reply()
        .expect_rolled_back()
    )

    assert 1 == handlers.success1.call_count
    assert 1 == handlers.failure2.call_count
    assert 1 == handlers.compensating1.call_count


def test_should_execute_all_steps_except1_successfully():
    handlers = Mock(Handlers)

    (
        SagaUnitTestSupport.given()
        .saga(WithHandlersSaga(handlers), ConditionalSagaData(False))
        .expect()
        .command(Do2Command())
        .to("participant2")
        .and_given()
        .success_reply()
        .expect_completed_successfully()
    )

    assert 1 == handlers.success2.call_count


def test_should_rollback_except1():
    handlers = Mock(Handlers)

    (
        SagaUnitTestSupport.given()
        .saga(WithHandlersSaga(handlers), ConditionalSagaData(False))
        .expect()
        .command(Do2Command())
        .to("participant2")
        .and_given()
        .failure_reply()
        .expect_rolled_back()
    )

    assert 1 == handlers.failure2.call_count


def test_should_failure_on_first_step():
    handlers = Mock(Handlers)

    (
        SagaUnitTestSupport.given()
        .saga(WithHandlersSaga(handlers), ConditionalSagaData(True))
        .expect()
        .command(Do1Command())
        .to("participant1")
        .and_given()
        .failure_reply()
        .expect_rolled_back()
    )

    assert 1 == handlers.failure1.call_count
