from typing import Callable, TypeVar
from functools import wraps
from warnings import warn
from traceback import format_exc


Inputs = TypeVar("Inputs")
Outputs = TypeVar("Outputs")


WARNING_MESSAGE = """error occurred during the execution of the program.
error: {}
function name: {}
line number: {}
line: {}
"""


def parse_exception_stacktrace(stacktrace: str) -> tuple[str, str, str, str]:
    stacktrace = stacktrace.split("\n")
    error = stacktrace[-2].strip()
    function_name = stacktrace[-5].split(", ")[2].split(" ")[1].strip()
    error_line_number = stacktrace[-5].split(", ")[1].split(" ")[1].strip()
    error_string = stacktrace[-4].strip()
    return error, function_name, error_line_number, error_string


def make_warning_message(stacktrace: tuple[str, str, str, str]) -> str:
    return WARNING_MESSAGE.format(
        stacktrace[0], stacktrace[1], stacktrace[2], stacktrace[3]
    )


def safe_cell(
    input_function: Callable[[Inputs], Outputs]
) -> Callable[[Inputs], Outputs]:
    @wraps(input_function)
    def substitution(*args, **kwargs) -> Outputs:
        try:
            result = input_function(*args, **kwargs)
        except Exception:
            exception_stacktrace = parse_exception_stacktrace(format_exc())
            warn(make_warning_message(exception_stacktrace), Warning)
            return None
        return result

    return substitution
