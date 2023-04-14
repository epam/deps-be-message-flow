from typing import Any, Dict, Generic, List, Optional, TypeVar

from pytest import fail

from message_flow.commands.common import (
    Command,
    CommandMessageHeaders,
    CommandReplyOutcome,
    Failure,
    ReplyMessageHeaders,
    Success,
)
from message_flow.commands.producer import CommandProducer
from message_flow.events.mappers import JsonMapper
from message_flow.messaging.common import IMessage
from message_flow.messaging.producer import IMessageProducer, MessageBuilder
from message_flow.sagas.orchestration import *
from message_flow.sagas.orchestration_simple_dsl import *

from .message_with_destination import MessageWithDestination

__all__ = ["SagaUnitTestSupport"]

T = TypeVar("T")


class SagaUnitTestSupport(Generic[T]):
    SAGA_ID: str = "1"

    def __init__(self) -> None:
        self._saga_manager: SagaManagerImpl = None
        self._expected_command: Command = None

        self._sent_commands: List[MessageWithDestination] = []
        self._sent_command: MessageWithDestination = None
        self._create_exception: Optional[Exception] = None

        self._counter = 2

        self._saga_instance: SagaInstance = None

    def _gen_id(self) -> str:
        self._counter += 1
        return str(self._counter)

    @classmethod
    def given(cls) -> "SagaUnitTestSupport":
        return cls()

    def saga(self, saga: Saga[T], saga_data: T) -> "SagaUnitTestSupport[T]":
        saga_instance_repository = self.SagaInstanceRepository(self)

        command_producer = CommandProducer(self.MessageProducer(self))
        saga_command_producer = SagaCommandProducer(command_producer)

        message_consumer = None
        saga_data_mapping = SagaDataMapping(
            {saga_data.__class__.__name__: saga_data.__class__}
        )

        self._saga_manager = SagaManagerImpl(
            saga,
            saga_instance_repository,
            command_producer,
            message_consumer,
            saga_command_producer,
            saga_data_mapping,
        )

        try:
            self._saga_manager.create(saga_data)
        except Exception as error:
            self._create_exception = error

        return self

    def expect(self) -> "SagaUnitTestSupport[T]":
        if self._create_exception is not None:
            raise RuntimeError(f"Saga creation failed: {self._create_exception}")

        return self

    def command(self, command: Command) -> "SagaUnitTestSupport[T]":
        self._expected_command = command
        return self

    def to(self, command_channel: str) -> "SagaUnitTestSupport[T]":
        assert 1 == len(self._sent_commands)
        self._sent_command = self._sent_commands[0]
        assert command_channel == self._sent_command.destination
        assert (
            self._expected_command.__class__.__name__
        ), self._sent_command.message.get_required_header(
            CommandMessageHeaders.COMMAND_TYPE
        )
        self._sent_commands.clear()

        return self

    def with_extra_headers(
        self, expected_extra_headers: Dict[str, str]
    ) -> "SagaUnitTestSupport[T]":
        actual_headers = self._sent_command.message.headers
        if not all(
            {expected_extra_headers.get(k) == v for k, v in actual_headers.items()}
        ):
            fail(
                f"Expected headers {actual_headers} to contain {expected_extra_headers}"
            )

        return self

    def and_given(self) -> "SagaUnitTestSupport[T]":
        return self

    def success_reply(
        self, reply: Optional[Any] = Success()
    ) -> "SagaUnitTestSupport[T]":
        outcome = CommandReplyOutcome.SUCCESS
        self._send_reply(reply, outcome)
        return self

    def failure_reply(
        self, reply: Optional[Any] = Failure()
    ) -> "SagaUnitTestSupport[T]":
        outcome = CommandReplyOutcome.FAILURE
        self._send_reply(reply, outcome)
        return self

    def _send_reply(self, reply: Any, outcome: CommandReplyOutcome) -> None:
        message = (
            MessageBuilder.with_payload(JsonMapper().serialize(reply))
            .with_header(ReplyMessageHeaders.REPLY_OUTCOME, outcome.value)
            .with_header(ReplyMessageHeaders.REPLY_TYPE, reply.__class__.__name__)
            .with_extra_headers(
                "", self._correlation_headers(self._sent_command.message.headers)
            )
            .build()
        )

        id = self._gen_id()
        message.headers[IMessage.ID] = id
        self._saga_manager.handle_message(message)

    def _correlation_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        correlation_headers: Dict[str, str] = {
            CommandMessageHeaders.in_reply(key): value
            for key, value in headers.items()
            if key.startswith(CommandMessageHeaders.COMMAND_HEADER_PREFIX)
        }
        correlation_headers[ReplyMessageHeaders.IN_REPLY_TO] = headers.get(
            IMessage.ID, ""
        )
        return correlation_headers

    def expect_completed_successfully(self) -> "SagaUnitTestSupport[T]":
        self._assert_no_commands()
        assert self._saga_instance.end_state
        assert not self._saga_instance.compensating

        return self

    def expect_rolled_back(self) -> "SagaUnitTestSupport[T]":
        self._assert_no_commands()
        assert self._saga_instance.end_state
        assert self._saga_instance.compensating

        return self

    def _assert_no_commands(self) -> None:
        if (commands_len := len(self._sent_commands)) == 0:
            return
        elif commands_len == 1:
            mwd = self._sent_commands[0]
            fail(
                f"Expected saga to have finished but found a command of {mwd.message.get_required_header(CommandMessageHeaders.COMMAND_TYPE)} sent to {mwd.destination}: {mwd.message}"
            )
        else:
            assert [] == self._sent_commands

    def expect_exception(self, expected_create_exception: Exception) -> None:
        assert expected_create_exception == self._create_exception

    def assert_saga_data(self, saga_data_consumer) -> "SagaUnitTestSupport[T]":
        saga_data_consumer(
            SagaDataSerde.deserialize_saga_data(
                self._saga_instance.serialized_saga_data,
                self._saga_manager._saga_data_mappingD,
            )
        )
        return self

    class SagaInstanceRepository(ISagaInstanceRepository):
        def __init__(self, parent: "SagaUnitTestSupport") -> None:
            self._parent = parent

        def save(self, saga_instance: SagaInstance) -> SagaInstance:
            saga_instance.saga_id = self._parent.SAGA_ID
            self._parent._saga_instance = saga_instance
            return saga_instance

        def find(self, saga_id: str) -> SagaInstance:
            return self._parent._saga_instance

        def update(self, saga_instance: SagaInstance) -> SagaInstance:
            self._parent._saga_instance = saga_instance
            return saga_instance

    class MessageProducer(IMessageProducer):
        def __init__(self, parent: "SagaUnitTestSupport") -> None:
            self._parent = parent

        def send(self, destination: str, message: IMessage) -> None:
            id: str = self._parent._gen_id()
            message.set_header(IMessage.ID, id)
            self._parent._sent_commands.append(
                MessageWithDestination(destination, message)
            )
