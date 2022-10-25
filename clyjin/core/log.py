import os
import sys
from typing import Any, Tuple, Union

from clyjin.util import convert_string_to_bool
from clyjin.core import Err
from loguru import logger


UnrecognizedLevelErr = lambda level: Exception(
    "Unrecognized level {}".format(level)
)
NotAnExceptionErr = lambda obj: Exception(
    "Object {} is not an Exception".format(obj)
)

def init_logger() -> Tuple[None, Err]:
    print(__name__)
    SINK = os.environ.get("CLYJIN_LOG_SINK", "var/logs/app.log")
    # LEVEL = os.environ.get("CLYJIN_LOG_LEVEL", "INFO")
    LEVEL = os.environ.get("CLYJIN_LOG_LEVEL", "DEBUG")
    has_to_serialize, err = convert_string_to_bool(
        os.environ.get("CLYJIN_HAS_TO_SERIALIZE", "true")
    )
    if err is None:
        HAS_TO_SERIALIZE: bool = has_to_serialize
    else:
        logger.bind(err=err).error("")
        exit(1)

    # Remove default sink
    logger.remove(0)

    logger.add(
        sys.stdout,
        level=LEVEL,
        format=_format_log,
        colorize=True
    )

    logger.add(
        SINK,
        level=LEVEL,
        format=_format_log,
        serialize=HAS_TO_SERIALIZE
    )

    return (None, None)

def _format_log(record: Any) -> str:
    logged_err: Union[Exception, None] = None
    src_args = [record["name"], record["function"]]

    if (record["extra"].get("err", None)):
        logged_err = record["extra"]["err"]
        src_args.append(logged_err.__class__.__name__)

    src = ".".join(src_args)

    level, err = _colorize_level(record["level"].name)
    if err is not None:
        print(
            "[#clyjin.logger.format / ERROR] {}: {}"
                .format(err.__class__.__name__, " ".join(err.args))
        )

    message = record["message"] if not logged_err else " ".join(
        logged_err.args
    )

    # Time is not required by now, but here is the method for its formatting
    # print(record["time"].strftime("%Y.%m.%d at %H:%M:%S:%f%z"))

    return "[{src} / {level}] {message}\n".format(
        src=src, level=level, message=message
    )

def _colorize_level(level: str) -> Tuple[str, Err]:
    wrapped: str

    if level == "DEBUG":
        wrapped = "<magenta>{}</magenta>"
    elif level == "INFO":
        wrapped = "<blue>{}</blue>"
    elif level == "WARNING":
        wrapped = "<yellow>{}</yellow>"
    elif level == "ERROR":
        wrapped = "<red>{}</red>"
    elif level == "CRITICAL":
        wrapped = "<black>{}</black>"
    else:
        return ("", UnrecognizedLevelErr(level))

    return (wrapped.format(level), None)
