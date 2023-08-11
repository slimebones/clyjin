from clyjin.core.config import Config


class Module:
    """
    Basic Clyjin unit for defining own interfaces.

    Every defined module should inherit this class and implement method
    `execute(args: list[str])`.

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
        CONFIG(optional):
            Config class attached to the Model. No config is attached by
            default.

    Attributes:
        config(optional):
            Parsed instance of class defined in `CONFIG` class attribute.
            Defaults to None, if the `CONFIG` attribute is not set.

    @abstract
    """
    CONFIG: Config | None = None

    def __init__(self, config: Config | None = None) -> None:
        self._config: Config | None = None
