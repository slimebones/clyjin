import os
from pathlib import Path
from antievil import NotFoundError
from clyjin.base.module import Module
from clyjin.core.cli.parser import CLIParser
from clyjin.core.cli.cliargs import CLIArgs
from clyjin.core.moduleclasses import CORE_MODULE_CLASSES
from clyjin.core.modules.base import CoreModule


class Boot:
    """
    Central entry unit of application execution.
    """
    def __init__(self, rootdir: Path) -> None:
        self._RegisteredModules: list[type[Module]] = []
        self._config_path: Path
        self._sysdir: Path

        self._DEFAULT_SYSDIR: Path = Path(
            os.environ["HOME"],
            ".clyjin"
        )
        self._DEFAULT_CONFIG_PATH: Path = Path(
            rootdir,
            "clyjin.yml"
        )

    async def start(self) -> None:
        self._collect_registered_modules()
        cli_args: CLIArgs = CLIParser(
            self._RegisteredModules
        ).parse()

        self._sysdir = \
            self._DEFAULT_SYSDIR \
            if cli_args.sysdir is None else cli_args.sysdir
        # don't create home parents for safety and to avoid permission errors
        self._sysdir.mkdir(parents=False, exist_ok=True)

        self._config_path = \
            self._DEFAULT_CONFIG_PATH \
            if cli_args.config_path is None else cli_args.config_path
        if not self._config_path.exists():
            raise NotFoundError(
                title="config path",
                value=self._config_path
            )

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
        # always add Core modules
        self._RegisteredModules.extend(CORE_MODULE_CLASSES)
