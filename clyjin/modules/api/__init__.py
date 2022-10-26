"""Create flask application hosts OpenAPI documentation."""
import os
from functools import reduce
from typing import Any, Generator, Iterator, List, Sequence, Tuple
import aiohttp_jinja2
import jinja2
from loguru import logger
from aiohttp import web

import yaml
from clyjin.core.ArgsTuple import ArgsTuple

BIND_FLAG_OPTIONS = ["-b", "--bind"]
API_PATHS_FILE_FLAG_OPTIONS = ["-f", "--file"]


def _load_api_paths(path: str) -> Iterator[str]:
    with open(path, "r") as f:
        paths: List[str] = f.readlines()
    yield from map(
        lambda path: path.strip(),
        filter(lambda path: not path.isspace(), paths)
    )

def _get_api_name_from_entrypoint(path: str) -> str:
    return yaml.load(open(path, "r"), yaml.SafeLoader)["info"]["title"]

def _parse_api_entrypoint_path_by_name(
        name: str,
        args: ArgsTuple
    ) -> Iterator[str]:
    # Find appropriate file arg option, load file for this option, create spec
    # out of this file content specified paths
    api_paths = _load_api_paths(args[
            args.index(
                next(filter(
                    lambda option: option in args,
                    API_PATHS_FILE_FLAG_OPTIONS
                ))
            ) + 1
        ]
    )
    yield from filter(
        # Lower both sides for better matching of capitalized packages, i.e.
        # in routes they will always be responsive for any-cased variants
        lambda path:
            _get_api_name_from_entrypoint(path).lower() == name.lower(),
        api_paths
    )

def _validate_api_dirname(
        dirname: str,
        args: ArgsTuple
    ) -> None:
    # FIXME:
    #   If dirname will be a folder inside actual correct dirname, e.g.
    #   .../oapi/player/player.yml - it won't validate this - need to implement
    #   recursion to check all the way until match occurs or top of the tree is
    #   reached

    next(
        filter(
            lambda path: os.path.dirname(path) == dirname,
            _load_api_paths(args[
                    args.index(
                        next(filter(
                            lambda option: option in args,
                            API_PATHS_FILE_FLAG_OPTIONS
                        ))
                    ) + 1
                ]
            )
        )
    )

def _parse_binded_host_port(args: ArgsTuple) -> Tuple[str, int]:
    def _parse(bind_string: str) -> Tuple[str, int]:
        host, port =  bind_string.split(":")
        port = int(port)
        return host, port

    for option in BIND_FLAG_OPTIONS:
        if option in args:
            return _parse(args[args.index(option)+1])

    return "0.0.0.0", 5000

def main(args: Tuple[str]) -> None:
    async def _get_public(req):
        # FIXME:
        #   Security problems, rewrite or add additional checks to disallow path
        #   building. But if i use path as a route var, seems like that browser
        #   disallows such types of routes.
        path = str(req.match_info["path"])
        return web.FileResponse(
            os.path.join(
                "clyjin/modules/api/public",
                path
            )
        )

    async def _get_oapi(req):
        module_name = str(req.match_info["module_name"])

        entrypoint_path = next(
            _parse_api_entrypoint_path_by_name(module_name, args)
        )

        api_url = "/raw/{}".format(
            entrypoint_path
        )

        return aiohttp_jinja2.render_template(
            "index.html",
            req,
            {"api_entrypoint_url": api_url}
        )

    async def _get_raw(req):
        path = str(req.match_info["path"])

        # Spec by dirname should be found to disallow random file exposing
        _validate_api_dirname(
            os.path.dirname(path),
            args
        )

        return web.FileResponse(
            path
        )

    #-- Initialization --#
    app = web.Application()
    aiohttp_jinja2.setup(app,
        loader=jinja2.FileSystemLoader("clyjin/modules/api/templates"))

    app.add_routes([
        web.get(r"/public/{path:.*}", _get_public),
        web.get(r"/raw/{path:.*}", _get_raw),
        web.get(r"/{module_name}", _get_oapi),
    ])

    host, port = _parse_binded_host_port(args)
    web.run_app(app, host=host, port=port)

    # @app.route("/<api_name>")
    # def swagger(api_name: str):

    #     return render_template(
    #         "index.html",
    #         api_entrypoint_url=api_url
    #     )

    # app.run(host=args.host, port=args.port)
