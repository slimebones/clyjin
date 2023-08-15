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

    def _collect_registered_modules(self) -> None:
        # always add Core module
        self._RegisteredModules.append(CoreModule)
