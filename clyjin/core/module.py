from clyjin.base.module import Module
from clyjin.base.moduleargs import ModuleArg
from clyjin.core.args import CoreArgs
from clyjin.utils.log import Log


class CoreModule(Module):
    ARGS = CoreArgs(
        action=ModuleArg(
            names=[
                "action"
            ],
            type=str
        )
    )

    async def execute(self) -> None:
        Log.debug(", ".join([
            self._name,
            str(self._args),
            str(self._config)
        ]))
