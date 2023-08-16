from pathlib import Path
from typing import Generic, TypeVar

from antievil import (CannotBeNoneError, ExpectedTypeError, PleaseDefineError,
                      UnsupportedError)

from clyjin.base.config import ConfigType
from clyjin.base.moduleargs import ModuleArgsType
from clyjin.utils.string import snakefy

ModuleType = TypeVar("ModuleType", bound="Module")
class Module(Generic[ModuleArgsType, ConfigType]):
    """
    Basic Clyjin unit for defining own interfaces.

    Every defined module should inherit this class and implement method
    `execute()`.

    After creating own subclass of Module, you can call
    `clyjin core register <path/to/your/module.py>:MyModule` which will
    register a module MyModule in the clyjin's storage.

    A custom-defined Config can be attached to every Module, which is parsed by
    Clyjin from the user's configuration file, AKA `clyjin.yml`.

    In the configuration file, a field with the name, corresponding to the
    Module's name is used to store any configuration data. For example, for a
    Module named `DonutShopModule`, the according field will be named
    `DonutShop`.

    To attach a config, class-attribute `Model.CONFIG` is used. For further
    details of Config making, see according documentation at
    [Config]($(ref.orwynn.core.config.Config)).

    Class-Attributes:
        NAME:
            Name of the Module primarily used as CLI module's name. If
            `_root` is used as a Module's name, the Module is considered to
            be root to it's parent Plugin.
        DESCRIPTION(optional):
            Description of Module primarily appeared in CLI help section.
            Defaults to None.
        ARGS(optional):
            Module Args class attached to the Module. No args are accepted
            by default. Note that these args are not populated with values,
            for populated args see `self.args` property.
        CONFIG_CLASS(optional):
            Config class attached to the Module. No config is attached by
            default.

    Attributes:
        name:
            Module's name either taken from the `NAME` attribute or by
            snakefying the class's name replacing `Module` suffix.
        description:
            Module's description.
        args:
            Module's parsed args with actual values attached
            if the `ARGS` attribute is not set.
        config:
            Parsed instance of class defined in `CONFIG_CLASS` attribute.
        rootdir:
            From where the module was called from.
        module_sysdir:
            System directory for module's files. Your module should use only
            this directory for long-term file-storage needs.
        verbosity_level:
            How verbose module's messages should be.

    @abstract
    """
    NAME: str | None = None
    DESCRIPTION: str | None = None
    ARGS: ModuleArgsType | None = None
    CONFIG_CLASS: type[ConfigType] | None = None

    def __init__(
        self,
        *,
        name: str,
        description: str | None,
        args: ModuleArgsType | None,
        config: ConfigType | None,
        module_sysdir: Path,
        rootdir: Path,
        verbosity_level: int
    ) -> None:
        self._name: str = name
        self._description: str | None = description
        self._args: ModuleArgsType | None = args
        self._config: ConfigType | None = config
        self._module_sysdir: Path = module_sysdir
        self._rootdir: Path = rootdir
        self._verbosity_level: int = verbosity_level

    @classmethod
    def cls_get_str(cls) -> str:
        return f"Module Class <{cls.cls_get_name()}>"

    @classmethod
    def cls_get_name(cls) -> str:
        if cls.NAME is None:
            raise PleaseDefineError(
                cannot_do=f"module <{cls}> initialization",
                please_define="attribute NAME"
            )
        elif not isinstance(cls.NAME, str):
            raise ExpectedTypeError(
                obj=cls.NAME,
                ExpectedType=str,
                is_instance_expected=True,
                ActualType=type(cls.NAME)
            )

        return cls.NAME.strip().lower()

    @property
    def args(self) -> ModuleArgsType:
        if self._args is None:
            raise CannotBeNoneError(
                title=f"in order to retrieve, Module <{self}> args",
            )
        return self._args

    async def execute(self) -> None:
        raise NotImplementedError
