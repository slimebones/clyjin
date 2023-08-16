from typing import Generic, TypeVar

from antievil import CannotBeNoneError, UnsupportedError

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
        NAME(optional):
            Name of the Module primarily used as CLI module's name. Defaults
            to snaked class's name without `Module` suffix, if it presents.
            For example `MyCustomModule` -> `my_custom`.
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
        description(optional):
            Module's description. Defaults to None, if the `DESCRIPTION`
            attribute is not set.
        args(optional):
            Module's parsed args with actual values attached. Defaults to None,
            if the `ARGS` attribute is not set.
        config(optional):
            Parsed instance of class defined in `CONFIG_CLASS` attribute.
            Defaults to None, if the `CONFIG_CLASS` attribute is not set.

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
        description: str | None = None,
        args: ModuleArgsType | None = None,
        config: ConfigType | None = None,
    ) -> None:
        self._name: str = name
        self._description: str | None = description
        self._args: ModuleArgsType | None = args
        self._config: ConfigType | None = config

    @classmethod
    def get_external_name(cls) -> str:
        if cls.NAME is not None:
            return cls.NAME

        module_class_name: str = cls.__name__

        # replace suffix "Model"
        module_suffix_occurence: int = module_class_name.find(
            "Module", len(module_class_name) - 6,
        )
        if module_suffix_occurence == 0:
            raise UnsupportedError(
                title="module named with bare \"Module\": for class",
                value=cls,
            )
        elif module_suffix_occurence != -1:
            module_class_name = module_class_name.replace("Module", "")

        return snakefy(module_class_name)

    @property
    def args(self) -> ModuleArgsType:
        if self._args is None:
            raise CannotBeNoneError(
                title=f"in order to retrieve, Module <{self}> args",
            )
        return self._args

    async def execute(self) -> None:
        raise NotImplementedError
