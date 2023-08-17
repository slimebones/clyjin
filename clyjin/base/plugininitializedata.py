from pathlib import Path
from clyjin.base.model import Model
from clyjin.base.module import Module


class PluginInitializeData(Model):
    root_dir: Path
    config_path: Path
    called_module: Module
    called_plugin_sysdir: Path
    called_plugin_common_sysdir: Path
    called_module_sysdir: Path
