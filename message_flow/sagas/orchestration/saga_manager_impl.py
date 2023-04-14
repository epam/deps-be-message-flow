import logging
import re
from typing import Generic, TypeVar

from ...commands.common import CommandReplyOutcome, ReplyMessageHeaders
from ...commands.producer import CommandProducer
from ...messaging.common import IMessage
from ...messaging.consumer import IMessageConsumer
from ...messaging.producer import MessageBuilder
from ..common import SagaReplyHeaders  # type: ignore
from .saga import Saga
from .saga_actions import SagaActions
from .saga_command_producer import SagaCommandProducer
from .saga_data_serde import SagaDataMapping, SagaDataSerde
from .saga_definition import SagaDefinition
from .saga_instance import SagaInstance
from .saga_instance_repository import ISagaInstanceRepository

__all__ = ["SagaManagerImpl"]

Data = TypeVar("Data")


class SagaManagerImpl(Generic[Data]):
    def __init__(
        self,
        saga: Saga[Data],
        saga_instance_repository: ISagaInstanceRepository,
        command_producer: CommandProducer,
        message_consumer: IMessageConsumer,
        saga_command_producer: SagaCommandProducer,
        saga_data_mapping: SagaDataMapping,
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

        self._saga = saga
        self._saga_instance_repository = saga_instance_repository
        self._command_producer = command_producer
        self._message_consumer = message_consumer
        self._saga_command_producer = saga_command_producer
        self._saga_data_mapping = saga_data_mapping

    @property
    def _saga_type(self) -> str:
        return self._saga.saga_type

    @property
    def _state_definition(self) -> SagaDefinition[Data]:
        sm = self._saga.saga_definition

        if sm is None:
            raise RuntimeError("state machine cannot be null")

        return sm

    def create(self, saga_data: Data) -> SagaInstance:
        saga_instance = SagaInstance(
            self._saga_type,
            "None",
            "????",
            "None",
            SagaDataSerde.serialize_saga_data(saga_data),
        )

        saga_instance = self._saga_instance_repository.save(saga_instance)

        saga_id = saga_instance.saga_id

        self._saga.on_starting(saga_instance.saga_id, saga_data)

        actions: SagaActions[Data] = self._state_definition.start(saga_data)

        if actions.local_exception is not None:
            raise actions.local_exception

        self._process_actions(
            self._saga.saga_type, saga_id, saga_instance, saga_data, actions
        )

        return saga_instance

    def subscribe_to_reply_channel(self) -> None:
        self._message_consumer.subscribe(
            {self._make_saga_reply_channel()},
            self.handle_message,
            queue=self._make_saga_reply_queue(),
        )

    def handle_message(self, message: IMessage) -> None:
        self._logger.debug("Handle message invoked %s", message)
        if message.has_header(SagaReplyHeaders.REPLY_SAGA_ID):
            self._handle_reply(message)
        else:
            self._logger.warning(
                "Handle message doesn't know what to do with: %s ", message
            )

    def _handle_reply(self, message: IMessage) -> None:
        if not self._is_reply_for_this_saga_type(message):
            return

        self._logger.debug("Handle reply %s", message)

        saga_id = message.get_required_header(SagaReplyHeaders.REPLY_SAGA_ID)
        saga_type = message.get_required_header(SagaReplyHeaders.REPLY_SAGA_TYPE)

        saga_instance = self._saga_instance_repository.find(saga_id)

        saga_data: Data = SagaDataSerde.deserialize_saga_data(
            saga_instance.serialized_saga_data,
            self._saga_data_mapping,
        )

        current_state = saga_instance.state_name

        self._logger.info("Current state=%s", current_state)

        actions = self._state_definition.handle_reply(
            saga_type, saga_id, current_state, saga_data, message
        )

        self._logger.info("Handled reply. Sending commands %s", actions.commands)

        self._process_actions(saga_type, saga_id, saga_instance, saga_data, actions)

    def _is_reply_for_this_saga_type(self, message: IMessage) -> bool:
        if (
            reply_saga_type := message.get_header(SagaReplyHeaders.REPLY_SAGA_TYPE)
        ) is not None:
            return reply_saga_type == self._saga_type

        return False

    def _process_actions(
        self,
        saga_type: str,
        saga_id: str,
        saga_instance: SagaInstance,
        saga_data: Data,
        actions: SagaActions[Data],
    ) -> None:
        while True:
            if actions.local_exception is not None:
                actions = self._state_definition.handle_reply(
                    saga_type,
                    saga_id,
                    actions.updated_state,
                    actions.updated_saga_data,  # type: ignore
                    MessageBuilder.with_payload(b"{}")
                    .with_header(
                        ReplyMessageHeaders.REPLY_OUTCOME,
                        CommandReplyOutcome.FAILURE.value,
                    )
                    .with_header(ReplyMessageHeaders.REPLY_TYPE, "Failure")
                    .build(),
                )
            else:
                last_request_id: str = self._saga_command_producer.send_commands(
                    self._saga_type,
                    saga_id,
                    actions.commands,
                    self._make_saga_reply_channel(),
                )
                saga_instance.last_request_id = last_request_id

                self._update_state(saga_instance, actions)

                saga_instance.serialized_saga_data = SagaDataSerde.serialize_saga_data(
                    actions.updated_saga_data
                    if actions.updated_saga_data
                    else saga_data
                )

                if actions.is_end_state:
                    self._perform_end_state_actions(
                        saga_id,
                        saga_instance,
                        actions.is_compensating,
                        actions.is_failed,
                        saga_data,
                    )

                self._saga_instance_repository.update(saga_instance)

                if not actions.is_local:
                    break

                actions = self._state_definition.handle_reply(
                    saga_type,
                    saga_id,
                    actions.updated_state,
                    actions.updated_saga_data,  # type: ignore
                    MessageBuilder.with_payload(b"{}")
                    .with_header(
                        ReplyMessageHeaders.REPLY_OUTCOME,
                        CommandReplyOutcome.SUCCESS.value,
                    )
                    .with_header(ReplyMessageHeaders.REPLY_TYPE, "Success")
                    .build(),
                )

    def _make_saga_reply_channel(self) -> str:
        return f"{self._saga_type}-reply"

    def _make_saga_reply_queue(self) -> str:
        kebab_case_saga_type = re.sub("(?!^)([A-Z]+)", r"-\1", self._saga_type).lower()
        return f"{kebab_case_saga_type}-queue"

    def _update_state(
        self, saga_instance: SagaInstance, actions: SagaActions[Data]
    ) -> None:
        if actions.updated_state is not None:
            saga_instance.state_name = actions.updated_state
            saga_instance.end_state = actions.is_end_state
            saga_instance.compensating = actions.is_compensating
            saga_instance.failed = actions.is_failed

    def _perform_end_state_actions(
        self,
        saga_id: str,
        saga_instance: SagaInstance,
        compensating: bool,
        failed: bool,
        saga_data: Data,
    ) -> None:
        if failed:
            self._saga.on_saga_failed(saga_id, saga_data)

        if compensating:
            self._saga.on_saga_rolled_back(saga_id, saga_data)
        else:
            self._saga.on_saga_completed_successfully(saga_id, saga_data)
