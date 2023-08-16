from clyjin.base.config import Config
from clyjin.base.module import Module
from clyjin.core.plugin.args import ConfiguratorCoreArgs
from clyjin.log import Log


class ConfiguratorModule(Module[ConfiguratorCoreArgs, Config]):
    NAME = "configure"
    DESCRIPTION = "configure the system's core"
    ARGS = ConfiguratorCoreArgs(
    )

    async def execute(self) -> None:
        Log.info("[core.configurator] Hello!")
