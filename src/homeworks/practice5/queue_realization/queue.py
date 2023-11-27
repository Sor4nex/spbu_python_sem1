from dataclasses import dataclass
from typing import TypeVar, Generic, Optional


N = TypeVar("N")


@dataclass
class Node(Generic[N]):
    current_value: N
    next_value: Optional["Node[N]"] = None


@dataclass
class Queue(Generic[N]):
    size: int = 0
    head: Optional[Node[N]] = None
    tail: Optional[Node[N]] = None


def create_new_queue() -> Queue[N]:
    return Queue()


def get_size(given_queue: Queue[N]) -> int:
    return given_queue.size


def is_empty(given_queue: Queue[N]) -> bool:
    return get_size(given_queue) == 0


def get_top(given_queue: Queue[N]) -> Optional[N]:
    if is_empty(given_queue):
        return None
    return given_queue.head.current_value


def push(given_queue: Queue[N], new_value: N) -> None:
    new_element = Node(new_value, None)
    if is_empty(given_queue):
        given_queue.head = new_element
    elif get_size(given_queue) == 1:
        given_queue.head.next_value = new_element
        given_queue.tail = new_element
    else:
        given_queue.tail.next_value = new_element
        given_queue.tail = new_element
    given_queue.size += 1


def pop(given_queue: Queue[N]) -> Optional[N]:
    if is_empty(given_queue):
        return None
    result = given_queue.head.current_value
    given_queue.head = given_queue.head.next_value
    given_queue.size -= 1
    return result
