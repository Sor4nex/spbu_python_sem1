from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    current_value: None
    next_value: None


@dataclass
class Queue:
    size: int = 0
    head: Node = None
    tail: Node = None


def create_new_queue() -> Queue:
    return Queue()


def get_size(given_queue: Queue) -> int:
    return given_queue.size


def is_empty(given_queue: Queue) -> bool:
    return get_size(given_queue) == 0


def get_top(given_queue: Queue) -> Any:
    if is_empty(given_queue):
        return None
    return given_queue.head.current_value


def push(given_queue: Queue, new_value: any) -> None:
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


def pop(given_queue: Queue) -> None:
    if is_empty(given_queue):
        return None
    given_queue.head = given_queue.head.next_value
    given_queue.size -= 1
