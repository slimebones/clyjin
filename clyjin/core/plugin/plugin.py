import importlib.metadata

import clyjin
from clyjin.base.plugin import Plugin
from clyjin.core.plugin.modules import ConfiguratorModule


class CorePlugin(Plugin):
    Name = "core"
    ModuleClasses = [
        ConfiguratorModule,
    ]
    Version = importlib.metadata.version("clyjin")

    @classmethod
    def get_version(cls) -> str | None:
        cls.Version = clyjin.__version__
        return super().get_version()
