from pathlib import Path

from clyjin.base.model import Model
from clyjin.base.module import Module
from clyjin.base.moduleargs import ModuleArgs
from clyjin.base.plugin import Plugin


class CLIArgs(Model):
    """
    Args parsed by first core CLI layer.

    Attributes:
        ModuleClass:
            Target Module Class.
        PluginClass:
            Target Plugin Class.
        populated_module_args:
            Parsed object of args directed to the target module.
        config_path(optional):
            Path to main configuration file. Defaults to None, i.e. hasn't been
            set.
        verbosity_level(optional):
            How verbose printed output should be. Defaults to 0.
    """
    ModuleClass: type[Module]
    PluginClass: type[Plugin]
    populated_module_args: ModuleArgs | None
    config_path: Path | None
    verbosity_level: int
    sysdir: Path | None

    class Config:
        arbitrary_types_allowed = True
