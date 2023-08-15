import argparse
from pathlib import Path
from typing import Any
from antievil import LogicError, ExpectedTypeError
from clyjin.base.module import Module
from clyjin.base.moduleargs import ModuleArg, ModuleArgs, ModuleArgsType
from clyjin.utils.string import snakefy


class CLIGenerator:
    """
    Generates argument parser for registered modules.
    """
    def get_parser(
        self,
        RegisteredModules: list[type[Module]]
    ) -> argparse.ArgumentParser:
        parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Clyjin"
        )

        self._add_common_args(parser)
        module_subparser_hub: argparse._SubParsersAction = \
            self._add_module_subparser_hub(parser)
        self._add_module_args(module_subparser_hub, RegisteredModules)

        return parser

    def _add_common_args(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-v",
            "--verbose",
            type=int,
            default=0,
            action="count",
            help="verbosity level",
            dest="verbosity_level",
        )
        parser.add_argument(
            "-c",
            "--config",
            type=Path,
            default=None,
            action="count",
            help=
                "path to config file. Defaults to `clyjin.yml` in current dir",
            dest="config_path",
        )

    def _add_module_subparser_hub(
        self,
        parser: argparse.ArgumentParser
    ) -> argparse._SubParsersAction:
        return parser.add_subparsers(
            help="module to launch",
            dest="module",
        )

    def _add_module_args(
        self,
        module_subparser_hub: argparse._SubParsersAction,
        RegisteredModules: list[type[Module]]
    ) -> None:
        for ModuleClass in RegisteredModules:

            # add main parser in any case
            module_parser: argparse.ArgumentParser = \
                module_subparser_hub.add_parser(
                    ModuleClass.get_external_name(),
                    help=ModuleClass.DESCRIPTION
                )

            module_args: ModuleArgs | None = ModuleClass.ARGS
            if module_args is None:
                # register modules without args only with initial keyword
                continue
            self._parse_module_args(module_args, module_parser)

    def _parse_module_args(
        self,
        module_args: ModuleArgs,
        module_parser: argparse.ArgumentParser
    ) -> None:
        for arg_name, module_arg in module_args.model_dump().items():
            if not isinstance(arg_name, str):
                raise ExpectedTypeError(
                    obj=arg_name,
                    ExpectedType=str,
                    is_instance_expected=True,
                    ActualType=type(arg_name)
                )
            elif not isinstance(module_arg, ModuleArg):
                raise ExpectedTypeError(
                    obj=module_arg,
                    ExpectedType=ModuleArg,
                    is_instance_expected=True,
                    ActualType=type(module_arg)
                )

            arg_add_optionals: dict[str, Any] = dict(
                action=module_arg.action,
                nargs=module_arg.nargs,
                const=module_arg.const,
                default=module_arg.default,
                choices=module_arg.choices,
                required=module_arg.required,
                help=module_arg.help,
                metavar=module_arg.metavar,
                **module_arg.argparse_kwargs
                    if module_arg.argparse_kwargs else {}
            )

            module_parser.add_argument(
                *module_arg.names,
                type=module_arg.type,
                dest=arg_name,
                **arg_add_optionals
            )
