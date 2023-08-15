import re


def snakefy(name: str) -> str:
    """Converts name to snake_case.

    Note that this is not reversible using camelfy().

    Args:
        name:
            Name to convert.

    Returns:
        Name converted.
    """
    # Reference: https://stackoverflow.com/a/1176023/14748231
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()
