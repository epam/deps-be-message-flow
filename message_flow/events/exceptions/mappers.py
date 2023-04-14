from message_flow.events.exceptions.common import (
    DeserializationError,
    NotFoundException,
    SerializationError,
)


class SchemaNotFound(NotFoundException):
    code = "schema_not_found_exception"


class WrongEventType(SerializationError):
    code = "wrong_event_type_exception"


class MessageTooSmall(DeserializationError):
    code = "message_too_small_exception"
