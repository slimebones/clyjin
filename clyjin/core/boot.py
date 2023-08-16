import importlib.util
import os
import pkgutil
from pathlib import Path
from typing import TYPE_CHECKING, Any

from antievil import ExpectedTypeError, NotFoundError

from clyjin.base.moduledata import ModuleData
from clyjin.base.plugin import Plugin
from clyjin.core.cli.cliargs import CLIArgs
from clyjin.core.cli.parser import CLIParser
from clyjin.core.plugin.plugin import CorePlugin
from clyjin.log import Log

if TYPE_CHECKING:
    from types import ModuleType as PyModuleType

    from clyjin.base.module import Module


class Boot:
    """
    Central entry unit of application execution.
    """
    def __init__(self, *, rootdir: Path) -> None:
        self._RegisteredPlugins: list[type[Plugin]] = []
        self._config_path: Path
        self._sysdir: Path
        self._called_module_sysdir: Path

        self._rootdir: Path = rootdir

        self._DEFAULT_SYSDIR: Path = Path(
            os.environ["HOME"],
            ".clyjin",
        )
        self._DEFAULT_CONFIG_PATH: Path = Path(
            self._rootdir,
            "clyjin.yml",
        )

    async def start(self) -> None:
        await self._collect_registered_plugins()
        cli_args: CLIArgs = CLIParser(
            self._RegisteredPlugins,
        ).parse()
        self._initialize_paths(cli_args)

        module: Module = cli_args.ModuleClass(ModuleData(
            name=cli_args.ModuleClass.cls_get_name(),
            ParentPlugin=cli_args.PluginClass,
            description=cli_args.ModuleClass.DESCRIPTION,
            args=cli_args.populated_module_args,
            # TODO(ryzhovalex): implement configs
            # 0
            config=None,
            rootdir=self._rootdir,
            module_sysdir=self._called_module_sysdir,
            verbosity_level=cli_args.verbosity_level,
        ))

        Log.info(
            f"[core] executing module <{module}>"
        )

        await module.execute()

        Log.info(
            f"[core] executed module <{module}>"
        )

    def _initialize_paths(self, cli_args: CLIArgs) -> None:
        self._sysdir = \
            self._DEFAULT_SYSDIR \
            if cli_args.sysdir is None else cli_args.sysdir

        self._called_module_sysdir = Path(
            self._sysdir,
            "plugins",
            cli_args.PluginClass.get_name(),
            cli_args.ModuleClass.cls_get_name(),
        )

        self._sysdir.mkdir(parents=True, exist_ok=True)
        self._called_module_sysdir.mkdir(parents=True, exist_ok=True)

        self._config_path = \
            self._DEFAULT_CONFIG_PATH \
            if cli_args.config_path is None else cli_args.config_path
        if not self._config_path.exists():
            Log.warning(
                f"[core] config is not found at <{self._config_path}>:"
                " use defaults",
            )

    async def _collect_registered_plugins(self) -> None:
        # always add Core Plugin
        self._RegisteredPlugins.append(CorePlugin)
        Log.info(
            f"[core] loaded core plugin <{CorePlugin.get_str()}>",
        )

        for finder, name, _ispkg in pkgutil.iter_modules():
            if name.startswith("clyjin_"):
                pathstr: str = self._get_finder_pathstr(finder)
                Log.info(
                    f"[core] found Python module <{name}> at <{pathstr}>",
                )

                try:
                    LoadedPlugin: type[Plugin] = self._load_plugin(name)
                except (NotFoundError, ExpectedTypeError) as error:
                    Log.error(
                        "[core] failed to load plugin"
                        f" <{name}>: error=<{error}>",
                    )
                    continue

                Log.info(
                    f"[core] loaded plugin <{LoadedPlugin.get_str()}>",
                )

    def _get_finder_pathstr(self, finder: Any) -> str:
        try:
            return str(finder.path)
        except AttributeError:
            return "unattached path"

    def _load_plugin(self, name: str) -> type[Plugin]:
        imported_module: PyModuleType = importlib.import_module(name)
        try:
            # MainPlugin variable is searched by default, maybe later it might
            # be configurable
            ImportedMainPlugin: type[Module] = imported_module.MainPlugin
        except AttributeError as error:
            raise NotFoundError(
                title="MainPlugin attribute of imported module",
                value=imported_module,
            ) from error

        if not issubclass(ImportedMainPlugin, Plugin):
            raise ExpectedTypeError(
                obj=ImportedMainPlugin,
                ExpectedType=Plugin,
                # TODO(ryzhovalex): use `expected_inheritance` to denote
                #   issubclass() usage as it gets support at Antievil
                # 0
                is_instance_expected=True,
                ActualType=type(ImportedMainPlugin),
            )

        self._RegisteredPlugins.append(ImportedMainPlugin)
        return ImportedMainPlugin
