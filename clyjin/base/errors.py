from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from clyjin.base.module import Module
    from clyjin.base.plugin import Plugin


class NoModulesPluginError(Exception):
    """
    Plugin contains no modules.
    """
    def __init__(self, PluginClass: type["Plugin"]) -> None:
        super().__init__(
            f"plugin <{PluginClass.get_str()}> defines no modules",
        )


class ForeignModulePluginError(Exception):
    """
    Plugin interacted with module it doesn't have.
    """
    def __init__(
        self,
        PluginClass: type["Plugin"],
        ModuleClass: type["Module"],
    ) -> None:
        super().__init__(
            f"plugin <{PluginClass.get_name()}> does not have module"
            f" <{ModuleClass.get_str()}>",
        )


class DuplicateRootModulePluginError(Exception):
    """
    Plugin has several root modules.
    """
    def __init__(
        self,
        PluginClass: type["Plugin"],
        ModuleClass: type["Module"],
    ) -> None:
        super().__init__(
            f"cannot add root module <{ModuleClass.get_str()}>:"
            f" plugin <{PluginClass.get_str()}> already has a root module",
        )
