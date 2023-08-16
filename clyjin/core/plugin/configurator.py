from clyjin.base.module import Module
from clyjin.core.plugin.args import ConfiguratorCoreArgs
from clyjin.log import Log


class ConfiguratorModule(Module):
    NAME = "configure"
    DESCRIPTION = "configure the system's core"
    ARGS = ConfiguratorCoreArgs(
    )

    async def execute(self) -> None:
        Log.info("[core.configurator] Hello!")
