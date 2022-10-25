from typing import Optional


class BaseErr(Exception):
    def __init__(self, message: str, src: str, *args: object) -> None:
        super().__init__(message, *args)

Err = Optional[BaseErr]
