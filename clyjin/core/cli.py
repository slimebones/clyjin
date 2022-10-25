from functools import partial
import sys
from typing import Any, Callable, List, Tuple, Type

from loguru import logger
from clyjin.core.log import init_logger
from clyjin.core import Err

class CliArgs:
    def __init__(
        self,
        module_name: str = ""
    ) -> None:
        self._module_name = module_name

    @property
    def module_name(self) -> str:
        return self._module_name

NoModuleNameErr = lambda: Exception(
    "You should define module name as first argument"
)

def main() -> Tuple[None, Err]:
    _, err = init_logger()
    if err:
        logger.bind(err=err).error("")

    args: CliArgs
    args, err = _parse_args(sys.argv) 
    if err:
        logger.bind(err=err).error("")
        exit(1)

    return (None, None)

def _parse_args(args: List[str]) -> Tuple[CliArgs, Err]:
    try:
        module_name: str = args[2]
    except IndexError as err:
        return (CliArgs(), err)
    else:
        return (CliArgs(module_name=module_name), None)

def _process(args: CliArgs) -> Tuple[None, Err]:
    return (None, None)
