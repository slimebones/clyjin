from pathlib import Path


def _get_version() -> str:
    with Path(
        Path(__file__).parent,
        ".version"
    ).open("r") as f:
        return f.read().strip()

__version__ = _get_version()
