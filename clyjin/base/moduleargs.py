from typing import Any, Generic, TypeVar

from antievil import CannotBeNoneError, UnsetValueError
from pydantic.generics import GenericModel

from clyjin.base.model import Model
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

    Use `argparse_type` if you want to override `type` as an argument to
    `argparse.add_argument`. It is useful in situations where you want to
    accept list, but don't want to invoke argparse's special logic for list
    type. Pass `argparse_type=type` to disable passing type to argparse at all.
    """
    action: str | None = None
    nargs: int | str | None = None
    const: T | None = None
    default: T | None = None
    choices: list[T] | None = None
    required: bool | None = None
    help: str | None = None
    metavar: str | tuple[str, ...] | None = None
    argparse_kwargs: dict[str, Any] | None = None

    argparse_type: type | None = None

    names: list[str]
    type: type[T]

    _value: T | None = None

    @property
    def value(self) -> T:
        if self._value is None:
            raise UnsetValueError(
                explanation=f"cannot get module arg <{self}> value",
            )
        return self._value

    @value.setter
    def value(self, value: T) -> None:
        self._value = value

    def is_optional(self) -> bool:
        return any("-" in name for name in self.names)
