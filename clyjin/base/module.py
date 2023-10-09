from typing import TYPE_CHECKING, Generic, TypeVar

from antievil import (
    CannotBeNoneError,
    PleaseDefineError,
    TypeExpectError,
)

from clyjin.base.config import ConfigType
from clyjin.base.moduleargs import ModuleArgsType

if TYPE_CHECKING:
    from pathlib import Path

    from clyjin.base.moduledata import ModuleData
    from clyjin.base.plugin import Plugin

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
        Name:
            Name of the Module primarily used as CLI module's name. If
            `$root` is used as a Module's name, the Module is considered to
            be root to it's parent Plugin.
        Description(optional):
            Description of Module primarily appeared in CLI help section.
            Defaults to None.
        Args(optional):
            Module Args class attached to the Module. No args are accepted
            by default. Note that these args are not populated with values,
            for populated args see `self.args` property.
        CONFIG_CLASS(optional):
            Config class attached to the Module. No config is attached by
            default.

    Attributes:
        module_data:
            Required data to initialize the Module. Passed by Clyjin System.

    @abstract
    """
    Name: str | None = None
    Description: str | None = None
    Args: ModuleArgsType | None = None
    CONFIG_CLASS: type[ConfigType] | None = None

    def __init__(
        self,
        module_data: "ModuleData[ModuleArgsType, ConfigType]",
    ) -> None:
        self._name: str = module_data.name
        self._description: str | None = module_data.description
        self._args: ModuleArgsType | None = module_data.args
        self._config: ConfigType | None = module_data.config
        self._plugin_common_sysdir: Path = module_data.plugin_common_sysdir
        self._module_sysdir: Path = module_data.module_sysdir
        self._rootdir: Path = module_data.rootdir
        self._verbosity_level: int = module_data.verbosity_level
        self._ParentPlugin: type["Plugin"] = module_data.ParentPlugin

    def __str__(self) -> str:
        return \
            f"Module <{self.cls_get_name()}>" \
            f" of Plugin <{self._ParentPlugin.get_str()}>"

    @classmethod
    def cls_get_str(cls) -> str:
        return f"Module Class <{cls.cls_get_name()}>"

    @classmethod
    def cls_get_name(cls) -> str:
        if cls.Name is None:
            raise PleaseDefineError(
                cannot_do=f"module <{cls}> initialization",
                please_define="attribute Name",
            )
        elif not isinstance(cls.Name, str):
            raise TypeExpectError(
                obj=cls.Name,
                ExpectedType=str,
                expected_inheritance="instance",
                ActualType=type(cls.Name),
            )

        return cls.Name.strip().lower()

    @property
    def args(self) -> ModuleArgsType:
        if self._args is None:
            raise CannotBeNoneError(
                title=f"in order to retrieve, Module <{self}> args",
            )
        return self._args

    async def execute(self) -> None:
        raise NotImplementedError
