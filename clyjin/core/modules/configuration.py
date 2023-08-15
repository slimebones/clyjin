from clyjin.base.module import Module
from clyjin.base.moduleargs import ModuleArg
from clyjin.core.modules.args import ConfigurationCoreArgs
from clyjin.core.modules.base import CoreModule
from clyjin.utils.log import Log


class ConfigurationCoreModule(CoreModule):
    NAME = "core.configure"
    DESCRIPTION = "configure the system's core"
    ARGS = ConfigurationCoreArgs(
    )

    async def execute(self) -> None:
        raise NotImplementedError
