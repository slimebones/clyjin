from pathlib import Path
from typing import Generic

from pydantic.generics import GenericModel

from clyjin.base.config import ConfigType
from clyjin.base.moduleargs import ModuleArgsType


class ModuleData(GenericModel, Generic[ModuleArgsType, ConfigType]):
    """
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
    """
    name: str
    description: str | None
    args: ModuleArgsType | None
    config: ConfigType | None
    module_sysdir: Path
    rootdir: Path
    verbosity_level: int