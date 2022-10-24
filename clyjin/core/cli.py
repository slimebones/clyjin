from typing import Tuple
from clyjin.core.log import init_logger
from clyjin.core import Err


def main() -> Tuple[None, Err]:
    return init_logger()
