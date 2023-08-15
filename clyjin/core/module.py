from clyjin.base.module import Module
from clyjin.base.moduleargs import ModuleArg
from clyjin.core.action import CoreAction
from clyjin.core.args import CoreArgs
from clyjin.utils.log import Log


class CoreModule(Module):
    ARGS = CoreArgs(
        action=ModuleArg[CoreAction](
            names=[
                "action"
            ],
            type=CoreAction,
            choices=list(CoreAction),
            help="core action to perform"
        )
    )

    async def execute(self) -> None:
        Log.debug(", ".join([
            self._name,
            str(self._args),
            str(self._config)
        ]))
