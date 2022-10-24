import typing
from clyjin.core import err

UnconvertableStringErr = lambda string: Exception(
    "Unconvertable string {}".format(string))

def convert_string_to_bool(string: str) -> typing.Tuple[bool, err]:
    """Convert given string to bool according to logical rules.
    
    Possible values of input string:
        - "true"
        - "false"
        - "0"
        - "1"

    Args:
        string:
            String to be converted

    Return:
        Converted boolean

    Errors:
        UnrecognizedValueError
    """
    if string in ["true", "1"]:
        return (True, None)
    elif string in ["false", "0"]:
        return (False, None)
    else:
        return (bool(), UnconvertableStringErr(string))
