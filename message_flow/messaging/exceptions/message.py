from message_flow.messaging.exceptions.common import MessagingException


class HeaderNotFound(MessagingException):
    code = "message_header_not_found"


class WrongHeader(MessagingException):
    code = "wrong_header"
