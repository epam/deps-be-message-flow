class EventsException(Exception):
    code = "base_events_exception"


class NotFoundException(EventsException):
    code = "events_not_found_exception"


class SerializationError(EventsException):
    code = "serialization_error_exception"


class DeserializationError(EventsException):
    code = "deserialization_error_exception"
