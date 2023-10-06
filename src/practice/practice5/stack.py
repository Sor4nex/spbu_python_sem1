from collections import namedtuple
from dataclasses import dataclass
from typing import Optional


StackElement = namedtuple("StackElement", ["current_value", "next_value"])


@dataclass
class Stack:
    size: int
    head: Optional[StackElement]


def create_new_stack() -> Stack:
    return Stack(0, None)


def empty(given_stack: Stack) -> bool:
    return not bool(size(given_stack))


def size(given_stack: Stack) -> int:
    return given_stack.size


def top(given_stack: Stack) -> any:
    if empty(given_stack):
        return None
    return given_stack.head.current_value


def push(given_stack: Stack, new_value: any) -> None:
    current_head = given_stack.head
    given_stack.head = StackElement(new_value, current_head)
    given_stack.size += 1


def pop(given_stack: Stack) -> None:
    if empty(given_stack):
        return None
    current_head = given_stack.head
    given_stack.head = current_head.next_value
    given_stack.size -= 1


if __name__ == "__main__":
    stack_1 = create_new_stack()
    print(top(stack_1)) # None
    push(stack_1, 34)
    print(empty(stack_1))  # False
    print(size(stack_1))  # 1
    print(top(stack_1))  # 34
    push(stack_1, 35)
    print(empty(stack_1))  # False
    print(size(stack_1))  # 2
    print(top(stack_1))  # 35
    pop(stack_1)
    print(empty(stack_1))  # False
    print(size(stack_1))  # 1
    print(top(stack_1))  # 34
    pop(stack_1)
    print(empty(stack_1))  # True
    print(size(stack_1))  # 0
    print(top(stack_1))  # None
    pop(stack_1)
