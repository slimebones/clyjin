import importlib.util
import os
import pkgutil
from pathlib import Path
from typing import TYPE_CHECKING, Any

from antievil import ExpectedTypeError, NotFoundError

from clyjin.base.module import Module
from clyjin.core.cli.cliargs import CLIArgs
from clyjin.core.cli.parser import CLIParser
from clyjin.core.moduleclasses import CORE_MODULE_CLASSES
from clyjin.utils.log import Log

if TYPE_CHECKING:
    from types import ModuleType as PyModuleType


class Boot:
    """
    Central entry unit of application execution.
    """
    def __init__(self, *, rootdir: Path) -> None:
        self._RegisteredModules: list[type[Module]] = []
        self._config_path: Path
        self._sysdir: Path

        self._DEFAULT_SYSDIR: Path = Path(
            os.environ["HOME"],
            ".clyjin",
        )
        self._DEFAULT_CONFIG_PATH: Path = Path(
            rootdir,
            "clyjin.yml",
        )

    async def start(self) -> None:
        await self._collect_registered_modules()
        cli_args: CLIArgs = CLIParser(
            self._RegisteredModules,
        ).parse()
        self._initialize_paths(cli_args)

        module: Module = cli_args.ModuleClass(
            name=cli_args.ModuleClass.get_external_name(),
            description=cli_args.ModuleClass.DESCRIPTION,
            args=cli_args.populated_module_args,
            # TODO(ryzhovalex): implement configs
            # 0
            # config=
        )
        await module.execute()

    def _initialize_paths(self, cli_args: CLIArgs) -> None:
        self._sysdir = \
            self._DEFAULT_SYSDIR \
            if cli_args.sysdir is None else cli_args.sysdir
        # don't create home parents for safety and to avoid permission errors
        self._sysdir.mkdir(parents=False, exist_ok=True)

        self._config_path = \
            self._DEFAULT_CONFIG_PATH \
            if cli_args.config_path is None else cli_args.config_path
        if not self._config_path.exists():
            Log.warning(
                f"[core] config is not found at <{self._config_path}>:"
                " use defaults",
            )

    async def _collect_registered_modules(self) -> None:
        # always add Core modules
        self._RegisteredModules.extend(CORE_MODULE_CLASSES)

        for finder, name, _ispkg in pkgutil.iter_modules():
            if name.startswith("clyjin_"):
                pathstr: str = self._get_finder_pathstr(finder)
                Log.info(
                    f"[core] found module <{name}> at <{pathstr}>",
                )

                try:
                    self._load_module(name)
                except (NotFoundError, ExpectedTypeError) as error:
                    Log.error(
                        "[core] failed to load module"
                        f" <{name}>: error=<{error}>",
                    )

                Log.info(
                    f"[core] loaded module <{name}>",
                )

    def _get_finder_pathstr(self, finder: Any) -> str:
        try:
            return str(finder.path)
        except AttributeError:
            return "unattached path"

    def _load_module(self, name: str) -> None:
        imported_module: PyModuleType = importlib.import_module(name)
        try:
            # MainModule variable is searched by default, maybe later it might
            # be configurable
            ImportedMainModule: type[Module] = imported_module.MainModule
        except AttributeError as error:
            raise NotFoundError(
                title="MainModule attribute of imported module",
                value=imported_module,
            ) from error

        if not issubclass(ImportedMainModule, Module):
            raise ExpectedTypeError(
                obj=ImportedMainModule,
                ExpectedType=Module,
                # TODO(ryzhovalex): use `expected_inheritance` to denote
                #   issubclass() usage as it gets support at Antievil
                # 0
                is_instance_expected=True,
                ActualType=type(ImportedMainModule),
            )

        self._RegisteredModules.append(ImportedMainModule)
