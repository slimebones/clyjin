from functools import partial
import sys
from typing import Any, Callable, List, Tuple, Type

from loguru import logger
from clyjin.core.log import init_logger

class CliArgs:
    def __init__(
        self,
        module_name: str
    ) -> None:
        self._module_name = module_name

    @property
    def module_name(self) -> str:
        return self._module_name

class NoModuleNameException(Exception): pass

def main() -> None:
    init_logger()

    args: CliArgs = _parse_args(sys.argv) 

def _parse_args(args: List[str]) -> CliArgs:
    try:
        module_name: str = args[1]
    except IndexError as err:
        raise NoModuleNameException()
    else:
        return CliArgs(module_name=module_name)

def _process(args: CliArgs) -> None:
    return
