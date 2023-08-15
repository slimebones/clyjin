from clyjin.base.module import Module
from clyjin.core.cli.parser import CLIParser
from clyjin.core.cli.cliargs import CLIArgs
from clyjin.core.module import CoreModule


class Boot:
    """
    Central entry unit of application execution.
    """
    def __init__(self) -> None:
        self._RegisteredModules: list[type[Module]] = []

    async def start(self) -> None:
        self._collect_registered_modules()
        cli_args: CLIArgs = CLIParser(
            self._RegisteredModules
        ).parse()

        module: Module = cli_args.ModuleClass(
            name=cli_args.ModuleClass.get_external_name(),
            description=cli_args.ModuleClass.DESCRIPTION,
            args=cli_args.populated_module_args,
            # TODO(ryzhovalex): implement configs
            # 0
            # config=
        )

        await module.execute()

    def _collect_registered_modules(self) -> None:
        # always add Core module
        self._RegisteredModules.append(CoreModule)
