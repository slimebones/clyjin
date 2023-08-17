from __future__ import annotations

from pathlib import Path  # noqa: TCH003
from clyjin.base.module import Module  # noqa: TCH003
from typing import TYPE_CHECKING

from clyjin.base.model import Model


class PluginInitializeData(Model):
    root_dir: Path
    config_path: Path
    called_module: Module
    called_plugin_sysdir: Path
    called_plugin_common_sysdir: Path
    called_module_sysdir: Path

    class Config:
        arbitrary_types_allowed = True
