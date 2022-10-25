"""Create flask application hosts OpenAPI documentation."""
import os
from functools import reduce
from typing import Any, Generator, Iterator, List, Sequence, Tuple
from loguru import logger

import yaml
from clyjin.core.ArgsTuple import ArgsTuple
from flask import Flask, render_template, send_from_directory, stream_template

BIND_FLAG_OPTIONS = ["-b", "--bind"]
API_PATHS_FILE_FLAG_OPTIONS = ["-f", "--file"]
DEBUG_FLAG_OPTIONS = ["-d", "--debug"]

class APISpecNotFoundException(Exception): pass

class APISpec:
    """Specification grabbed for entrypoint.
    
    Args:
        name:
            Name of the spec
        entrypoint_path:
            Path to raw openapi entrypoint file 
    """
    def __init__(self, name: str, entrypoint_path: str) -> None:
        self._name = name
        self._entrypoint_path = entrypoint_path

    @property
    def name(self):
        return self._name

    @property
    def entrypoint_path(self):
        return self._entrypoint_path

class ServerArgs:
    """Arguments for initializing api server.
    
    Args:
        host:
            Host to be run on
        port:
            Port to be run on
        api_specs:
            APISpecs to be loaded to the server
        is_debug:
            Whether debug mode is on
    """
    def __init__(
        self,
        host: str,
        port: int,
        api_specs: Tuple[APISpec],
        is_debug: bool
    ) -> None:
        self._host = host
        self._port = port
        self._api_specs = api_specs
        self._is_debug = is_debug

    @property
    def host(self):
        return self._host
    
    @property
    def port(self):
        return self._port

    @property
    def api_specs(self):
        return self._api_specs

    @property
    def is_debug(self):
        return self._is_debug

    def get_api_spec_by_name(self, name: str) -> APISpec:
        try:
            return next(filter(lambda spec: spec.name == name, self.api_specs))
        except StopIteration:
            raise APISpecNotFoundException()

    def get_api_spec_by_entrypoint_path(self, path: str) -> APISpec:
        try:
            # TMP fix for missing leading slash because of flask route
            # truncating
            if path[:4] == "home":
                path = "/" + path
            #

            return next(filter(
                lambda spec: spec.entrypoint_path == path, self.api_specs
            ))
        except StopIteration:
            raise APISpecNotFoundException()

    def get_api_spec_by_dirname_path(self, path: str) -> APISpec:
        try:
            # TMP fix for missing leading slash because of flask route
            # truncating
            if path[:4] == "home":
                path = "/" + path
            #

            return next(filter(
                lambda spec: os.path.dirname(spec.entrypoint_path) == path,
                self.api_specs
            ))
        except StopIteration:
            raise APISpecNotFoundException()

def main(args: ArgsTuple) -> None:
    server_args = _parse_args(args)
    _run_app(server_args)

def _parse_args(args: ArgsTuple) -> ServerArgs:
    host, port = _parse_binded_host_port(args)
    api_specs = tuple(_parse_api_specs(args))
    is_debug = _parse_debug_flag(args)

    return ServerArgs(
        host=host, port=port, api_specs=api_specs, is_debug=is_debug
    )

def _parse_debug_flag(args: ArgsTuple) -> bool:
    try:
        next(filter(
            lambda option: option in args,
            DEBUG_FLAG_OPTIONS
        ))
    except StopIteration:
        return False
    else:
        return True

def _parse_api_specs(
        args: ArgsTuple
    ) -> Iterator[APISpec]:

    def _load_api_paths(path: str) -> Iterator[str]:
        with open(path, "r") as f:
            paths: List[str] = f.readlines()
        yield from map(
            lambda path: path.strip(),
            filter(lambda path: not path.isspace(), paths)
        )

    def _create_spec(path: str) -> APISpec:
        return APISpec(
            name=yaml.load(open(path, "r"), yaml.SafeLoader)["info"]["title"],
            entrypoint_path=path
        )

    # Find appropriate file arg option, load file for this option, create spec
    # out of this file content specified paths
    yield from map(
        lambda path: _create_spec(path),
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

def _parse_binded_host_port(args: ArgsTuple) -> Tuple[str, int]:
    def _parse(bind_string: str) -> Tuple[str, int]:
        host, port =  bind_string.split(":")
        port = int(port)
        return host, port

    for option in BIND_FLAG_OPTIONS:
        if option in args:
            return _parse(args[args.index(option)+1])

    return "0.0.0.0", 5000

def _run_app(args: ServerArgs) -> None:
    app = Flask(__name__)
    app.config["DEBUG"] = args.is_debug

    @app.route("/public/<path:path>")
    def public(path: str):
        return send_from_directory("public", path)

    @app.route("/raw/<path:path>")
    def raw(path: str):
        # Spec should be found to disallow random file exposing
        actual_path = args.get_api_spec_by_dirname_path(
            os.path.dirname(path)
        ).entrypoint_path

        return send_from_directory(
            os.path.dirname(actual_path), os.path.basename(path)
        )

    @app.route("/<api_name>")
    def swagger(api_name: str):
        api_url = (
            "/raw" + args.get_api_spec_by_name(
                api_name
            ).entrypoint_path
        # Remove double slashes which might occur on absolute entrypoint path
        # appending
        ).replace("//", "/")
        print(api_url)

        return render_template(
            "index.html",
            api_entrypoint_url=api_url
        )

    app.run(host=args.host, port=args.port)
