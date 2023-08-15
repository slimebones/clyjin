import argparse
from typing import Any, Generic, Iterable, TypeVar
from clyjin.base.model import Model
from pydantic.generics import GenericModel
from clyjin.utils.types import T


ModuleArgsType = TypeVar("ModuleArgsType", bound="ModuleArgs")
class ModuleArgs(Model):
    """
    Args object parsed by CLI and passed to Module.

    While the keys might be freely chosen (but should be strings), the values
    should be of `$(ref.clyjin.base.moduleargs.ModuleArg)` type.

    @abstract
    """


class ModuleArg(GenericModel, Generic[T]):
    """
    Description of Module's Argument, in form similar (except without e.g.
    `dest` argument) to `argparse.ArgumentParser.add_argument()` call.

    This object is also passed back to the host Module after the parsing, with
    according values attached.
    """
    action: Any | None = None
    nargs: int | None = None
    const: Any | None = None
    default: T | None = None
    choices: Iterable[T] | None = None
    required: bool | None = None
    help: str | None = None
    metavar: str | tuple[str, ...] | None = None
    argparse_kwargs: dict[str, Any] | None = None

    names: list[str]
    type: type[T]

    value: T | None = None
