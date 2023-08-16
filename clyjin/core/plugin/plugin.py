import clyjin
from clyjin.base.plugin import Plugin
from clyjin.core.plugin.configurator import ConfiguratorModule


class CorePlugin(Plugin):
    NAME = "core"
    MODULE_CLASSES = [
        ConfiguratorModule
    ]
    VERSION = None

    @classmethod
    def get_version(cls) -> str | None:
        cls.VERSION = clyjin.__version__
        return super().get_version()
