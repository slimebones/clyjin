from enum import Enum


class CoreAction(Enum):
    Configure = "configure"
    Register = "register"

    def __str__(self) -> str:
        return self.value
