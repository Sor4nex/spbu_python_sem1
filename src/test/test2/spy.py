from typing import Callable, Any, Iterator
from datetime import datetime


def print_usage_statistic(
    spied_function: Callable[[Any], Any]
) -> Iterator[tuple[str, list]]:
    try:
        for call in spied_function.calls_board:
            yield call
    except AttributeError:
        raise AttributeError("no usage statistic for undecorated function")


def spy(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def substitution(*args, **kwargs) -> Any:
        all_params = {"positional arguments": args}
        all_params.update(kwargs)
        substitution.calls_board.append((datetime.now(), all_params))
        return func(*args, **kwargs)

    substitution.calls_board = []
    return substitution
