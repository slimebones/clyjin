from pathlib import Path
from clyjin.base.model import Model
from clyjin.base.moduleargs import ModuleArgs


class CLIArgs(Model):
    """
    Args parsed by first core CLI layer.

    Attributes:
        module_name:
            Name of target module.
        module_args:
            Parsed object of args directed to the target module.
        config_path(optional):
            Path to main configuration file. Defaults to None, i.e. hasn't been
            set.
        verbosity_level(optional):
            How verbose printed output should be. Defaults to 0.
    """
    module_name: str
    module_args: ModuleArgs | None
    config_path: Path | None = None
    verbosity_level: int = 0
