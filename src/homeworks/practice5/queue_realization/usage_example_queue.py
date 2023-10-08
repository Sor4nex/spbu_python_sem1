from queue import *


def print_queue_characteristics(given_queue: Queue) -> None:
    print("\nОчередь пуста:", empty(given_queue))
    print("Количество элементов очереди:", size(given_queue))
    print("Первый элемент очереди:", top(given_queue), "\n")


if __name__ == "__main__":
    # создание очереди
    queue1 = create_new_queue()
    print_queue_characteristics(queue1)

    # добавление 1 элемента
    push(queue1, "hi")
    print_queue_characteristics(queue1)

    # добавление 2 элемента
    push(queue1, "Mark!")
    print_queue_characteristics(queue1)

    # удаление 1 элемента
    pop(queue1)
    print_queue_characteristics(queue1)

    # добавление 3 элемента
    push(queue1, "oh hey")
    print_queue_characteristics(queue1)

    # добавление 4 элемента
    push(queue1, "Billy!")
    print_queue_characteristics(queue1)

    # удаление 2 элемента
    pop(queue1)
    print_queue_characteristics(queue1)

    # удаление 3 элемента
    pop(queue1)
    print_queue_characteristics(queue1)

    # удаление 4 элемента
    pop(queue1)
    print_queue_characteristics(queue1)
