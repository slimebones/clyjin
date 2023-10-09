import argparse
import typing
from typing import Any

from antievil import (
    LogicError,
    NotFoundError,
    TypeExpectError,
    UnsupportedError,
)

from clyjin.base.module import Module
from clyjin.base.moduleargs import ModuleArg, ModuleArgs
from clyjin.base.plugin import Plugin
from clyjin.core.cli.cliargs import CLIArgs
from clyjin.core.cli.generator import CLIGenerator

if typing.TYPE_CHECKING:
    from pathlib import Path


class CLIParser:
    """
    Parser CLI args into application objects.

    Attributes:
        RegisteredPlugins:
            Plugin classes registered in the system to initialize parser
            groups for.
    """
    def __init__(self, RegisteredPlugins: list[type[Plugin]]) -> None:
        self._RegisteredPlugins: list[type[Plugin]] = RegisteredPlugins
        self._parser: argparse.ArgumentParser = CLIGenerator().get_parser(
            self._RegisteredPlugins,
        )

    def parse(
        self,
        args: list[str] | None = None,
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

        PluginClass: type[Plugin]
        ModuleClass: type[Module]
        PluginClass, ModuleClass = \
            self._get_plugin_module_classses_from_input_name(
                namespace.module,
            )

        populated_module_args: ModuleArgs | None = \
            self._populate_module_args_from_namespace(
                ModuleClass,
                namespace,
            )
        config_path: Path | None = namespace.config_path
        verbosity_level: int = namespace.verbosity_level
        sysdir: Path | None = namespace.sysdir

        return CLIArgs(
            ModuleClass=ModuleClass,
            PluginClass=PluginClass,
            populated_module_args=populated_module_args,
            config_path=config_path,
            verbosity_level=verbosity_level,
            sysdir=sysdir,
        )

    def _get_plugin_module_classses_from_input_name(
        self,
        input_name: str,
    ) -> tuple[type[Plugin], type[Module]]:
        PluginClass: type[Plugin]
        ModuleClass: type[Module]

        plugin_name: str
        module_name: str
        input_name_dots_count: int = input_name.count(".")
        if input_name_dots_count == 0:
            plugin_name = input_name
            module_name = "$root"
        elif input_name_dots_count == 1:
            plugin_name, module_name = input_name.split(".")
        else:
            raise UnsupportedError(
                title="more than one separation dot in input module name",
                value=input_name,
            )

        for PC in self._RegisteredPlugins:
            if PC.get_name() == plugin_name:
                PluginClass = PC
                ModuleClass = PluginClass.get_module_class(module_name)
                return PluginClass, ModuleClass

        raise NotFoundError(
            title="registered plugin for namespaced name",
            value=input_name,
        )

    def _populate_module_args_from_namespace(
        self,
        ModuleClass: type[Module],
        namespace: argparse.Namespace,
    ) -> ModuleArgs | None:
        empty_module_args: ModuleArgs | None = ModuleClass.Args

        if empty_module_args is None:
            # nothing to populate, left as it is
            return empty_module_args

        empty_module_args = typing.cast(ModuleArgs, empty_module_args)
        populated_module_args: ModuleArgs = empty_module_args.model_copy(
            deep=True,
        )

        for arg_name, _module_arg in empty_module_args.model_dump().items():
            if not isinstance(arg_name, str):
                raise TypeExpectError(
                    obj=arg_name,
                    ExpectedType=str,
                    expected_inheritance="instance",
                    ActualType=type(arg_name),
                )

            module_arg: ModuleArg = ModuleArg.parse_obj(_module_arg)

            try:
                arg_value: Any = vars(namespace)[arg_name]
            except KeyError as error:
                error_message: str = \
                    f"cannot find argument with name <{arg_name}>" \
                    " in generated namespace"
                raise LogicError(error_message) from error

            if (
                # arg value set to None if it is not defined, which should be
                # handled at the called module
                arg_value is not None
                and not isinstance(arg_value, module_arg.type)
            ):
                raise TypeExpectError(
                    obj=arg_value,
                    ExpectedType=module_arg.type,
                    expected_inheritance="instance",
                    ActualType=type(arg_value),
                )

            try:
                # finally set value for the module args object, i.e. populate
                getattr(populated_module_args, arg_name).value = arg_value
            except ValueError as error:  # arg_name not found
                error_message: str = \
                    f"cannot find argument with name <{arg_name}>" \
                    f" in model args <{empty_module_args}>"
                raise LogicError(error_message) from error

        return populated_module_args
