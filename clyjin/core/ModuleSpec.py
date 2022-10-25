from typing import Any, Callable, List, Tuple

from clyjin.core import Err


class ModuleSpec:
    """Specification for a executable module.

    Args:
        name:
            Name of the module
        entrypoint:
            Fn to be called as an entry to the module. Entrypoint receives
            args intended for the module and should return tuple of output and
            Exception occured.
    """
    def __init__(
        self,
        name: str,
        entrypoint: Callable[[List[str]], Tuple[Any, Err]]
    ) -> None:
        self._name = name
        self._entrypoint = entrypoint

    @property
    def name(self) -> str:
        return self._name

    @property
    def entrypoint(self) -> Callable[[List[str]], Tuple[Any, Err]]:
        return self._entrypoint
