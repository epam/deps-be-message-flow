from ..testing_support import *
from .commands import *
from .conditional_saga import *


def test_should_execute_all_steps_successfully():
    (
        SagaUnitTestSupport.given()
        .saga(ConditionalSaga(), ConditionalSagaData(True))
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


def test_should_rollback():
    (
        SagaUnitTestSupport.given()
        .saga(ConditionalSaga(), ConditionalSagaData(True))
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


def test_should_execute_all_steps_except1_successfully():
    (
        SagaUnitTestSupport.given()
        .saga(ConditionalSaga(), ConditionalSagaData(False))
        .expect()
        .command(Do2Command())
        .to("participant2")
        .and_given()
        .success_reply()
        .expect_completed_successfully()
    )


def test_should_rollback_except1():
    (
        SagaUnitTestSupport.given()
        .saga(ConditionalSaga(), ConditionalSagaData(False))
        .expect()
        .command(Do2Command())
        .to("participant2")
        .and_given()
        .failure_reply()
        .expect_rolled_back()
    )


def test_should_failure_on_first_step():
    (
        SagaUnitTestSupport.given()
        .saga(ConditionalSaga(), ConditionalSagaData(True))
        .expect()
        .command(Do1Command())
        .to("participant1")
        .and_given()
        .failure_reply()
        .expect_rolled_back()
    )
