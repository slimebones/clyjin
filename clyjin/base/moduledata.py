from pathlib import Path
from typing import Generic

from pydantic.generics import GenericModel

# we should import Config and ModuleArgs since otherwise Pydantic will give
# an undefined error for our generic usage
from clyjin.base.config import Config, ConfigType  # noqa: F401
from clyjin.base.moduleargs import ModuleArgs, ModuleArgsType  # noqa: F401
from clyjin.base.plugin import Plugin


class ModuleData(GenericModel, Generic[ModuleArgsType, ConfigType]):
    """
    Attributes:
        name:
            Module's name either taken from the `Name` attribute or by
            snakefying the class's name replacing `Module` suffix.
        ParentPlugin:
            Parent Plugin of this Module.
        description:
            Module's description.
        args:
            Module's parsed args with actual values attached
            if the `Args` attribute is not set.
        config:
            Parsed instance of class defined in `CONFIG_CLASS` attribute.
        rootdir:
            From where the module was called from.
        plugin_common_sysdir:
            System directory for Plugin's common files used by all Plugin's
            modules.
        module_sysdir:
            System directory for module's files. Your module should use only
            this directory for long-term file-storage needs.
        verbosity_level:
            How verbose module's messages should be.
    """
    name: str
    ParentPlugin: type[Plugin]
    description: str | None
    args: ModuleArgsType | None
    config: ConfigType | None
    plugin_common_sysdir: Path
    module_sysdir: Path
    rootdir: Path
    verbosity_level: int
