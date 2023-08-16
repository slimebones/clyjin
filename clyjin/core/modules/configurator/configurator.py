from clyjin.core.modules.base import CoreModule
from clyjin.core.modules.configurator.args import ConfiguratorCoreArgs
from clyjin.utils.log import Log


class ConfiguratorCoreModule(CoreModule):
    NAME = "core.configure"
    DESCRIPTION = "configure the system's core"
    ARGS = ConfiguratorCoreArgs(
    )

    async def execute(self) -> None:
        Log.info("[core.configurator] Hello!")
