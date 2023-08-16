import argparse
import typing
from typing import Any

from antievil import ExpectedTypeError, LogicError, NotFoundError

from clyjin.base.module import Module
from clyjin.base.moduleargs import ModuleArg, ModuleArgs
from clyjin.core.cli.cliargs import CLIArgs
from clyjin.core.cli.generator import CLIGenerator

if typing.TYPE_CHECKING:
    from pathlib import Path


class CLIParser:
    """
    Parser CLI args into application objects.

    Attributes:
        registered_modules:
            Modules registered in the system to initialize parser groups for.
    """
    def __init__(self, RegisteredModules: list[type[Module]]) -> None:
        self._RegisteredModules: list[type[Module]] = RegisteredModules
        self._parser: argparse.ArgumentParser = CLIGenerator().get_parser(
            self._RegisteredModules,
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

        ModuleClass: type[Module] = self._find_registered_module_by_name(
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
            populated_module_args=populated_module_args,
            config_path=config_path,
            verbosity_level=verbosity_level,
            sysdir=sysdir,
        )

    def _find_registered_module_by_name(
        self,
        module_name: str,
    ) -> type[Module]:
        for ModuleClass in self._RegisteredModules:
            if ModuleClass.get_external_name() == module_name:
                return ModuleClass

        raise NotFoundError(
            title="module with name",
            value=module_name,
        )

    def _populate_module_args_from_namespace(
        self,
        ModuleClass: type[Module],
        namespace: argparse.Namespace,
    ) -> ModuleArgs | None:
        empty_module_args: ModuleArgs | None = ModuleClass.ARGS

        if empty_module_args is None:
            # nothing to populate, left as it is
            return empty_module_args

        empty_module_args = typing.cast(ModuleArgs, empty_module_args)
        populated_module_args: ModuleArgs = empty_module_args.model_copy(
            deep=True,
        )

        for arg_name, _module_arg in empty_module_args.model_dump().items():
            if not isinstance(arg_name, str):
                raise ExpectedTypeError(
                    obj=arg_name,
                    ExpectedType=str,
                    is_instance_expected=True,
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

            # arg value should be strictly the same as described in module's
            # arg spec
            if type(arg_value) is not module_arg.type:
                raise ExpectedTypeError(
                    obj=arg_value,
                    ExpectedType=module_arg.type,
                    is_instance_expected=False,
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
