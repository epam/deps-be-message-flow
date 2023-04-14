from unittest.mock import Mock

from ..testing_support import *
from .commands import *
from .local_saga import *


def test_should_execute_all_steps_successfully():
    steps = Mock(LocalSagaSteps)

    (
        SagaUnitTestSupport.given()
        .saga(LocalSaga(steps), LocalSagaData())
        .expect()
        .command(Do2Command())
        .to("participant2")
        .and_given()
        .success_reply()
        .expect_completed_successfully()
    )


def test_should_rollback_from_step2():
    steps = Mock(LocalSagaSteps)

    (
        SagaUnitTestSupport.given()
        .saga(LocalSaga(steps), LocalSagaData())
        .expect()
        .command(Do2Command())
        .to("participant2")
        .and_given()
        .failure_reply()
        .and_given()
        .expect_rolled_back()
    )


def test_should_handle_failure_of_first_local_step():
    steps = Mock(LocalSagaSteps)
    expected_exception = RuntimeError("Failed")
    steps.local_step1.side_effect = expected_exception

    (
        SagaUnitTestSupport.given()
        .saga(LocalSaga(steps), LocalSagaData())
        .expect_exception(expected_exception)
    )


def test_should_handle_failure_of_last_local_step():
    steps = Mock(LocalSagaSteps)
    steps.local_step3.side_effect = RuntimeError()

    (
        SagaUnitTestSupport.given()
        .saga(LocalSaga(steps), LocalSagaData())
        .expect()
        .command(Do2Command())
        .to("participant2")
        .and_given()
        .success_reply()
        .expect()
        .command(Undo2Command())
        .to("participant2")
        .and_given()
        .success_reply()
        .expect_rolled_back()
    )
