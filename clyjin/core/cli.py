from functools import partial
import sys
from typing import Any, Callable, List, Tuple, Type

from loguru import logger
from clyjin.core.ArgsTuple import ArgsTuple
from clyjin.core.BUILTIN_MODULE_SPECS import BUILTIN_MODULE_SPECS
from clyjin.core.ModuleSpec import ModuleSpec
from clyjin.core.log import init_logger

class CannotFindSpecException(Exception): pass

class CliArgs:
    """Parsed CLI args.
    
    Args:
        module_name:
            Name of the module spec targets
        args:
            List of arguments for this module
    """
    def __init__(
        self,
        module_name: str,
        args: ArgsTuple
    ) -> None:
        self._module_name = module_name
        self._args = args

    @property
    def module_name(self):
        return self._module_name

    @property
    def args(self):
        return self._args

class NoModuleNameException(Exception): pass

def main() -> None:
    init_logger()

    args: CliArgs = _parse_args(tuple(sys.argv)) 
    _process(args)

def _parse_args(args: ArgsTuple) -> CliArgs:
    try:
        module_name: str = args[1]
    except IndexError as err:
        raise NoModuleNameException()
    else:
        return CliArgs(module_name=module_name, args=args[2:])

def _process(args: CliArgs) -> None:
    spec = _pick_spec(args.module_name)
    spec.entrypoint(args.args)

def _pick_spec(module_name: str) -> ModuleSpec:
    for spec in BUILTIN_MODULE_SPECS:
        if module_name == spec.name:
            return spec
    raise CannotFindSpecException()
