from clyjin.base.config import Config
from clyjin.base.module import Module
from clyjin.core.plugin.args import ConfiguratorCoreArgs
from clyjin.log import Log


class ConfiguratorModule(Module[ConfiguratorCoreArgs, Config]):
    Name = "configure"
    Description = "configure the system's core"
    Args = ConfiguratorCoreArgs(
    )

    async def execute(self) -> None:
        Log.info("[core.configurator] Hello!")
