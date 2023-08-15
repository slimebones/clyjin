import argparse
from pathlib import Path
from clyjin.base.module import Module
from clyjin.base.moduleargs import ModuleArgs
from clyjin.core.cli.generator import CLIGenerator
from clyjin.core.cliargs import CLIArgs


class CLIParser:
    """
    Parser CLI args into application objects.

    Attributes:
        registered_modules:
            Modules registered in the system to initialize parser groups for.
    """
    def __init__(self, registered_modules: list[Module]) -> None:
        self._registered_modules: list[Module] = registered_modules
        self._parser: argparse.ArgumentParser = CLIGenerator().get_parser(
            self._registered_modules
        )

    def parse(
        self,
        args: list[str] | None = None
    ) -> CLIArgs:
        """
        Parses incoming CLI args either from `args` argument or from system's
        args.

        Args:
            args(optional):
                List of string args to parse. System args are parsed by
                default.
        """
        namespace: argparse.Namespace = self._parser.parse_args(args)

        module_name: str = namespace.module
        module_args: ModuleArgs | None = self._get_module_args(namespace)
        config_path: Path | None = namespace.config_path
        verbosity_level: int = namespace.verbosity_level

    def _get_module_args(
        self,
        namespace: argparse.Namespace
    ) -> ModuleArgs | None:
