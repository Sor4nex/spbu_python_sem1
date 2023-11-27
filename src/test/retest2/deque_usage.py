import src.test.retest2.deque as deque


def print_status(input_deque: deque.Deque[deque.V]) -> None:
    print(
        f"""deque size: {deque.get_size(input_deque)}
deque is empty: {deque.is_empty(input_deque)}"""
    )


def operation_is_correct(
    input_deque: deque.Deque[deque.V], needed_size: int, is_really_empty: bool
) -> bool:
    return (
        deque.get_size(input_deque) == needed_size
        and deque.is_empty(input_deque) == is_really_empty
    )


if __name__ == "__main__":
    print("Создание двусторонней очереди")
    deque1 = deque.create_deque()
    print_status(deque1)
    print(f"Операция корректна: {operation_is_correct(deque1, 0, True)}\n")
    print("Добавления элемента 5 в начало")
    deque.pushFront(deque1, 5)
    print_status(deque1)
    print(f"Операция корректна: {operation_is_correct(deque1, 1, False)}\n")
    print("Добавление элемента 4 в начало")
    deque.pushFront(deque1, 4)
    print_status(deque1)
    print(f"Операция корректна: {operation_is_correct(deque1, 2, False)}\n")
    print("Добавление элемента 3 в начало")
    deque.pushFront(deque1, 3)
    print_status(deque1)
    print(f"Операция корректна: {operation_is_correct(deque1, 3, False)}\n")
    print("Добавления элементов 6 и 7 в конец")
    deque.pushBack(deque1, 6)
    deque.pushBack(deque1, 7)
    print_status(deque1)
    print(f"Операция корректна: {operation_is_correct(deque1, 5, False)}\n")
    first1 = deque.popFront(deque1)
    last1 = deque.popBack(deque1)
    last2 = deque.popBack(deque1)
    print(
        f"""Элементы в очереди: 3 4 5 6 7
Удаления элемента из начала очереди и двух элементов с конца:
Первый элемент из начала: {first1},
последний элемент: {last1},
предпоследний элемент: {last2}\n"""
    )
    print_status(deque1)
    print(
        f"Операция корректна: {operation_is_correct(deque1, 2, False) and first1 == 3 and last1 == 7 and last2 == 6}\n"
    )
    last1 = deque.popBack(deque1)
    first1 = deque.popFront(deque1)
    print(
        f"""Удаление последнего и первого элементов:
последний элемент: {last1},
первый элемент: {first1}"""
    )
    print_status(deque1)
    print(
        f"Операция корректна: {operation_is_correct(deque1, 0, True) and last1 == 5 and first1 == 4}\n"
    )
    print("Добавление элемента 5 в конец")
    deque.pushFront(deque1, 5)
    print_status(deque1)
    print(f"Операция корректна: {operation_is_correct(deque1, 1, False)}\n")
    print("Удаление последнего элемента")
    last1 = deque.popBack(deque1)
    print_status(deque1)
    print(
        f"Операция корректна: {operation_is_correct(deque1, 0, True) and last1 == 5}\n"
    )
