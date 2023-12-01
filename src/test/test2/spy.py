from typing import Callable, Any
from datetime import datetime
from functools import wraps
from inspect import getcallargs


def logger(file_path: str) -> Callable[[Any], Any]:
    def spy(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(func)
        def substitution(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            func_args = getcallargs(func, *args, **kwargs)
            all_paramaters = [f"{arg}={func_args[arg]}" for arg in sorted(func_args)]
            print(
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                func.__name__,
                " ".join(all_paramaters),
                result,
                file=substitution.output_file,
            )
            return result

        substitution.output_file = open(file_path, "w")
        return substitution

    return spy
