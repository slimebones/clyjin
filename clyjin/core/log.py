import os
import sys
import traceback
from typing import Any, Tuple, Union

from clyjin.core import convert_string_to_bool
from loguru import logger


class UnrecognizedLevelException(Exception):
    def __init__(self, level: str, *args) -> None:
        message = "Unrecognized level {}".format(level)
        super().__init__(message, *args)

class ExceptionsOnlyAllowedException(Exception):
    def __init__(self, obj: object, *args: object) -> None:
        message = "Object {} is not an Exception".format(obj)
        super().__init__(message, *args)

def init_logger() -> None:
    """Initialize logger"""
    SINK = os.environ.get("CLYJIN_LOG_SINK", "var/logs/app.log")
    # LEVEL = os.environ.get("CLYJIN_LOG_LEVEL", "INFO")
    LEVEL = os.environ.get("CLYJIN_LOG_LEVEL", "DEBUG")
    HAS_TO_SERIALIZE: bool = convert_string_to_bool(
        os.environ.get("CLYJIN_HAS_TO_SERIALIZE", "true")
    )

    logger.add(
        SINK,
        level=LEVEL,
        serialize=HAS_TO_SERIALIZE
    )

# DEPRECATED:
#   Custom formatting no more used... builtin loguru formatter is
#   better :-)
###
# def _format_log(record: Any) -> str:
#     logged_err: Union[Exception, None] = None
#     src_args = [record["name"], record["function"]]

#     src = ".".join(src_args)

#     level = _colorize_level(record["level"].name)

#     message = record["message"] if not logged_err else " ".join(
#         logged_err.args
#     )
#     # Reformat src and messages related to module to avoid ANSI errors
#     src = src.replace("<module>", "__module__")
#     message = message.replace("<module>", "__module__")

#     # Time is not required by now, but here is the method for its formatting
#     # print(record["time"].strftime("%Y.%m.%d at %H:%M:%S:%f%z"))

#     # Add traceback info if exception is presented
#     if record.get("exception", None):
#         message += "\n" + traceback.format_exc()

#     return "[{src} / {level}] {message}\n".format(
#         src=src, level=level, message=message
#     )

# def _colorize_level(level: str) -> str:
#     wrapped: str

#     if level == "DEBUG":
#         wrapped = "<magenta>{}</magenta>"
#     elif level == "INFO":
#         wrapped = "<blue>{}</blue>"
#     elif level == "WARNING":
#         wrapped = "<yellow>{}</yellow>"
#     elif level == "ERROR":
#         wrapped = "<red>{}</red>"
#     elif level == "CRITICAL":
#         wrapped = "<black>{}</black>"
#     else:
#         raise UnrecognizedLevelException(level)

#     return wrapped.format(level)
###
