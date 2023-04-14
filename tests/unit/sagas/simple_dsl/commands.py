from message_flow.commands.common import Command

__all__ = [
    "Do1Command",
    "Undo1Command",
    "Do2Command",
    "Undo2Command",
]


class Do1Command(Command):
    ...


class Do2Command(Command):
    ...


class Undo1Command(Command):
    ...


class Undo2Command(Command):
    ...
