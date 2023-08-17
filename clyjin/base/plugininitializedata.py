from __future__ import annotations

from typing import TYPE_CHECKING

from clyjin.base.model import Model

if TYPE_CHECKING:
    from pathlib import Path

    from clyjin.base.module import Module


class PluginInitializeData(Model):
    root_dir: Path
    config_path: Path
    called_module: Module
    called_plugin_sysdir: Path
    called_plugin_common_sysdir: Path
    called_module_sysdir: Path

    class Config:
        arbitrary_types_allowed = True
