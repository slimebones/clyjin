from pathlib import Path


def get_version() -> str:
    with Path(
        Path(__file__).parent,
        ".version",
    ).open("r") as f:
        return f.readline().strip()
