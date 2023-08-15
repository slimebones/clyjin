from pathlib import Path
from clyjin.base.module import Module
from clyjin.base.moduleargs import ModuleArg
from clyjin.core.modules.args import RegisterCoreArgs
from clyjin.core.modules.base import CoreModule
from clyjin.utils.log import Log


class RegisterCoreModule(CoreModule):
    NAME = "core.register"
    DESCRIPTION = "register new modules in the system"
    ARGS = RegisterCoreArgs(
        module_classpath=ModuleArg[list](
            names=[
                "module_classpath"
            ],
            type=list,
            nargs="+",
            argparse_type=type,
            help=
                "path to module's class in format `path/to/script.py:MyModule`"
        )
    )

    async def execute(self) -> None:
        Log.debug(self.args.module_classpath.value)
