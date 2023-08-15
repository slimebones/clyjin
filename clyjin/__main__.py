from loguru import logger
from .core.cli import parser

@logger.catch
def call_cli():
    parser.main()


if __name__ == "__main__":
    call_cli()
