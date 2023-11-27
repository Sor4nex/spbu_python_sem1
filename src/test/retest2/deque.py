from dataclasses import dataclass
from typing import TypeVar, Optional, Generic


V = TypeVar("V")


@dataclass
class Node(Generic[V]):
    value: V
    next: Optional["Node[V]"] = None


@dataclass
class Deque(Generic[V]):
    size: int = 0
    head: Optional[Node[V]] = None


def create_deque() -> Deque[V]:
    return Deque()


def get_size(deque: Deque[V]) -> int:
    return deque.size


def is_empty(deque: Deque[V]) -> bool:
    return get_size(deque) == 0


def pushBack(deque: Deque[V], value: V) -> None:
    if is_empty(deque):
        deque.head = Node(value)
        deque.size += 1
        return
    current_element = deque.head
    for i in range(get_size(deque) - 1):
        current_element = current_element.next
    current_element.next = Node(value)
    deque.size += 1


def pushFront(deque: Deque[V], value: V) -> None:
    deque.head = Node(value) if is_empty(deque) else Node(value, deque.head)
    deque.size += 1


def popFront(deque: Deque[V]) -> V:
    if is_empty(deque):
        raise ValueError("cannot pop: deque is empty")
    elif get_size(deque) == 1:
        popped_value = deque.head.value
        deque.head = None
        deque.size -= 1
        return popped_value
    popped_value = deque.head.value
    deque.head = deque.head.next
    deque.size -= 1
    return popped_value


def popBack(deque: Deque[V]) -> V:
    if is_empty(deque):
        raise ValueError("cannot pop: deque is empty")
    elif get_size(deque) == 1:
        popped_value = deque.head.value
        deque.head = None
        deque.size -= 1
        return popped_value
    current_element = deque.head
    for i in range(get_size(deque) - 2):
        current_element = current_element.next
    popped_value = current_element.next.value
    current_element.next = None
    deque.size -= 1
    return popped_value
