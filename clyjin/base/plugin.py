from typing import TYPE_CHECKING

from antievil import ExpectedTypeError, NotFoundError, PleaseDefineError

from clyjin.base.errors import (
    DuplicateRootModulePluginError,
    ForeignModulePluginError,
    NoModulesPluginError,
)

if TYPE_CHECKING:
    from clyjin.base.module import Module


class Plugin:
    """
    Basic importable unit to add new system's functionality.

    Used only as a class.

    Attributes:
        NAME:
            Plugin's name used as top-level namespace to all Plugin's commands.
        MODULE_CLASSES:
            List of Module classes registered by this plugin.
        VERSION(optional):
            Version of the Plugin. Defaults to NONE.

    @abstract
    """
    NAME: str | None = None
    MODULE_CLASSES: list[type["Module"]] | None = None
    VERSION: str | None = None

    _RootModule: type["Module"] | None = None

    def __init__(self) -> None:
        raise NotImplementedError

    @classmethod
    def get_str(cls) -> str:
        return \
            f"Plugin Class <{cls.get_name()}>, version <{cls.get_version()}>"

    @classmethod
    def get_name(cls) -> str:
        if cls.NAME is None:
            raise PleaseDefineError(
                cannot_do=f"plugin <{cls}> initialization",
                please_define="attribute NAME",
            )
        elif not isinstance(cls.NAME, str):
            raise ExpectedTypeError(
                obj=cls.NAME,
                ExpectedType=str,
                is_instance_expected=True,
                ActualType=type(cls.NAME),
            )

        return cls.NAME.strip().lower()

    @classmethod
    def get_module_classes(cls) -> list[type["Module"]]:
        if cls.MODULE_CLASSES is None:
            raise PleaseDefineError(
                cannot_do=f"plugin <{cls}> initialization",
                please_define="attribute MODULE_CLASSES",
            )
        elif not isinstance(cls.MODULE_CLASSES, list):
            raise ExpectedTypeError(
                obj=cls.MODULE_CLASSES,
                ExpectedType=list,
                is_instance_expected=True,
                ActualType=type(cls.MODULE_CLASSES),
            )
        elif len(cls.MODULE_CLASSES) == 0:
            raise NoModulesPluginError(cls)

        return cls.MODULE_CLASSES

    @classmethod
    def get_version(cls) -> str:
        if cls.VERSION is None:
            return "unversioned"
        elif not isinstance(cls.VERSION, str):
            raise ExpectedTypeError(
                obj=cls.VERSION,
                ExpectedType=str,
                is_instance_expected=True,
                ActualType=type(cls.VERSION),
            )

        return cls.VERSION

    @classmethod
    def get_namespaced_module_name(cls, ModuleClass: type["Module"]) -> str:
        """
        Returns Module's name prefixed by Plugin's name.

        If Module's name is `_root`, the Module is considered to be root of
        it's parent Plugin and thus be available under Plugin's name.

        Each Plugin can contain only one root Module.
        """
        cls._check_has_module(ModuleClass)
        return cls._get_namespaced_module_name_nocheck(ModuleClass)

    @classmethod
    def get_module_class(cls, name: str) -> type["Module"]:
        # TODO(ryzhovalex): cache search results for better performance
        # 0

        for ModuleClass in cls.get_module_classes():
            if ModuleClass.cls_get_name() == name:
                return ModuleClass

        raise NotFoundError(
            title="module class with namespaced name",
            value=name,
            options={
                "plugin_class": cls.get_str(),
            },
        )

    @classmethod
    def _check_has_module(cls, ModuleClass: type["Module"]) -> None:
        if ModuleClass not in cls.get_module_classes():
            raise ForeignModulePluginError(
                PluginClass=cls,
                ModuleClass=ModuleClass,
            )

    @classmethod
    def _get_namespaced_module_name_nocheck(
        cls,
        ModuleClass: type["Module"],
    ) -> str:
        module_name: str = ModuleClass.cls_get_name()
        if module_name == "_root":
            cls._set_root_module_class(ModuleClass)
            return cls.get_name()
        return cls.get_name() + "." + module_name

    @classmethod
    def _set_root_module_class(cls, ModuleClass: type["Module"]) -> None:
        if cls._RootModule is not None and cls._RootModule is not ModuleClass:
            raise DuplicateRootModulePluginError(
                PluginClass=cls,
                ModuleClass=ModuleClass,
            )
        cls._RootModule = ModuleClass
