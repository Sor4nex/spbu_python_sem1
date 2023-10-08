from dataclasses import dataclass
from collections import namedtuple


@dataclass
class Queue:
    size: int = 0
    head: dict = None
    tail: dict = None


def create_new_queue() -> Queue:
    return Queue()


def size(given_queue: Queue) -> int:
    return given_queue.size


def empty(given_queue: Queue) -> bool:
    return size(given_queue) == 0


def top(given_queue: Queue) -> any:
    if empty(given_queue):
        return None
    return given_queue.head["current_value"]


def push(given_queue: Queue, new_value: any) -> None:
    new_element = {"current_value": new_value, "next_value": None}
    if empty(given_queue):
        given_queue.head = new_element
    elif size(given_queue) == 1:
        given_queue.head["next_value"] = new_element
        given_queue.tail = new_element
    else:
        given_queue.tail["next_value"] = new_element
        given_queue.tail = new_element
    given_queue.size += 1


def pop(given_queue: Queue) -> None:
    if empty(given_queue):
        return None
    given_queue.head = given_queue.head["next_value"]
    given_queue.size -= 1
