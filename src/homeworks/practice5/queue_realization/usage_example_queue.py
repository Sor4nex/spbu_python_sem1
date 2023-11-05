import queue


def print_queue_characteristics(given_queue: queue.Queue[queue.N]) -> None:
    print("1. Очередь пуста:", queue.is_empty(given_queue))
    print("2. Количество элементов очереди:", queue.get_size(given_queue))
    print("3. Первый элемент очереди:", queue.get_top(given_queue), "\n")


if __name__ == "__main__":
    print("создание очереди:")
    queue1 = queue.create_new_queue()
    print_queue_characteristics(queue1)

    print("добавление 1 элемента:")
    queue.push(queue1, "hi")
    print_queue_characteristics(queue1)

    print("добавление 2 элемента:")
    queue.push(queue1, "Mark!")
    print_queue_characteristics(queue1)

    print("удаление 1 элемента:", queue.pop(queue1))
    print_queue_characteristics(queue1)

    print("добавление 3 элемента:")
    queue.push(queue1, "oh hey")
    print_queue_characteristics(queue1)

    print("добавление 4 элемента:")
    queue.push(queue1, "Billy!")
    print_queue_characteristics(queue1)

    print("удаление 2 элемента:", queue.pop(queue1))
    print_queue_characteristics(queue1)

    print("удаление 3 элемента:", queue.pop(queue1))
    print_queue_characteristics(queue1)

    print("удаление 4 элемента:", queue.pop(queue1))
    print_queue_characteristics(queue1)

    print("попытка удаления 5 элемента (его нет):", queue.pop(queue1))
    print_queue_characteristics(queue1)
