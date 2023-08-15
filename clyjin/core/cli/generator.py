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
        registered_modules: list[Module]
    ) -> argparse.ArgumentParser:
        parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Clyjin"
        )

        self._add_common_args(parser)
        module_subparser_hub: argparse._SubParsersAction = \
            self._add_module_subparser_hub(parser)
        self._add_module_args(module_subparser_hub, registered_modules)

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
        registered_modules: list[Module]
    ) -> None:
        for module in registered_modules:

            # add main parser in any case
            module_parser: argparse.ArgumentParser = \
                module_subparser_hub.add_parser(
                    self._get_module_name(module),
                    help=module.DESCRIPTION
                )

            module_args: ModuleArgs | None = module.ARGS
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
            )

            module_parser.add_argument(
                *module_arg.names,
                type=module_arg.type,
                **arg_add_optionals
            )

    @staticmethod
    def _get_module_name(module: Module) -> str:
        if module.NAME is not None:
            return module.NAME

        module_class_name: str = module.__class__.__name__

        # replace suffix "Model"
        module_suffix_occurence: int = module_class_name.find(
            "Model", len(module_class_name) - 5
        )
        if module_suffix_occurence > 1:
            error_message: str = \
                "[core] more than one suffix occurence for module name" \
                f" <{module_class_name}>"
            raise LogicError(error_message)
        elif module_suffix_occurence == 1:
            module_class_name = module_class_name.replace("Model", "")

        return snakefy(module_class_name)
