import argparse
from argparse import _SubParsersAction as ArgparseSubParsersAction
from pathlib import Path
from typing import Any

from antievil import TypeExpectError, UnsupportedError

from clyjin.base.module import Module
from clyjin.base.moduleargs import ModuleArg, ModuleArgs
from clyjin.base.plugin import Plugin


class CLIGenerator:
    """
    Generates argument parser for registered modules.
    """
    def get_parser(
        self,
        RegisteredPlugins: list[type[Plugin]],
    ) -> argparse.ArgumentParser:
        parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Clyjin",
        )

        self._add_common_args(parser)
        self._module_subparser_hub: ArgparseSubParsersAction = \
            self._add_module_subparser_hub(parser)
        self._add_plugins_parsers(RegisteredPlugins)

        return parser

    def _add_common_args(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="verbosity level",
            dest="verbosity_level",
        )
        parser.add_argument(
            "-c",
            "--config",
            type=Path,
            default=None,
            help=
                "path to config file. Defaults to `clyjin.yml` in current dir",
            dest="config_path",
        )
        parser.add_argument(
            "--sysdir",
            type=Path,
            default=None,
            help=
                "directory for clyjin global configs."
                " Defaults to `$HOME/.clyjin`",
            dest="sysdir",
        )

    def _add_module_subparser_hub(
        self,
        parser: argparse.ArgumentParser,
    ) -> ArgparseSubParsersAction:
        return parser.add_subparsers(
            help="module to launch",
            dest="module",
        )

    def _add_plugins_parsers(
        self,
        RegisteredPlugins: list[type[Plugin]],
    ) -> None:
        for PluginClass in RegisteredPlugins:
            self._add_plugin_modules_parsers(
                PluginClass,
            )

    def _add_plugin_modules_parsers(
        self,
        PluginClass: type[Plugin],
    ) -> None:
        for ModuleClass in PluginClass.get_module_classes():
            self._add_plugin_module_parser(PluginClass, ModuleClass)

    def _add_plugin_module_parser(
        self,
        PluginClass: type[Plugin],
        ModuleClass: type[Module],
    ) -> None:
        # add main parser in any case
        module_parser: argparse.ArgumentParser = \
            self._module_subparser_hub.add_parser(
                # prefix any module name with Plugin's namespace
                PluginClass.get_namespaced_module_name(ModuleClass),
                help=ModuleClass.Description,
            )

        module_args: ModuleArgs | None = ModuleClass.Args
        if module_args is None:
            # register modules without args only with initial keyword
            return
        self._parse_module_args(module_args, module_parser)

    def _parse_module_args(
        self,
        module_args: ModuleArgs,
        module_parser: argparse.ArgumentParser,
    ) -> None:
        for arg_name, _module_arg in module_args.model_dump().items():
            if not isinstance(arg_name, str):
                raise TypeExpectError(
                    obj=arg_name,
                    ExpectedType=str,
                    expected_inheritance="instance",
                    ActualType=type(arg_name),
                )

            module_arg: ModuleArg = ModuleArg.parse_obj(_module_arg)

            argparse_type: type | None  = \
                module_arg.type \
                if module_arg.argparse_type is None \
                else module_arg.argparse_type

            arg_add_optionals: dict[str, Any] = dict(
                type=argparse_type,
                action=module_arg.action,
                nargs=module_arg.nargs,
                const=module_arg.const,
                default=module_arg.default,
                choices=module_arg.choices,
                required=module_arg.required,
                help=module_arg.help,
                metavar=module_arg.metavar,
                **module_arg.argparse_kwargs
                    if module_arg.argparse_kwargs else {},
            )

            if arg_add_optionals["action"] == "store_true":
                del arg_add_optionals["nargs"]
                del arg_add_optionals["const"]
                del arg_add_optionals["choices"]
                del arg_add_optionals["metavar"]

            if argparse_type is type:
                del arg_add_optionals["type"]

            # do not supply `dest` for positional arguments - argparse gives
            # an error for that
            if module_arg.is_optional():
                module_parser.add_argument(
                    *module_arg.names,
                    dest=arg_name,
                    **arg_add_optionals,
                )
            else:
                # positional arguments are always required
                if (
                    arg_add_optionals["required"] is not None
                    and arg_add_optionals["required"] is False
                ):
                    raise UnsupportedError(
                        title="non-required positional with name",
                        value=arg_name,
                    )
                del arg_add_optionals["required"]

                module_parser.add_argument(
                    *module_arg.names,
                    **arg_add_optionals,
                )
