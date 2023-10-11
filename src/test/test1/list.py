from dataclasses import dataclass


@dataclass
class List:
    length: int = 0
    ListElements: tuple = None


def create() -> List:
    return List()


def get_length(given_list: List) -> int:
    return given_list.length


def tail(given_list: List) -> any:
    if get_length(given_list) == 0:
        return None
    list_last_index = get_length(given_list) - 1
    return given_list.ListElements[list_last_index]


def head(given_list: List) -> any:
    if get_length(given_list) == 0:
        return None
    return given_list.ListElements[0]


def insert(given_list: List, value_to_insert: any, index: int) -> bool:
    if value_to_insert is None:
        return False
    elif get_length(given_list) == 0:
        given_list.ListElements = (value_to_insert,)
        given_list.length += 1
    elif get_length(given_list) + 1 == index:
        given_list.ListElements = given_list.ListElements + (value_to_insert,)
        given_list.length += 1
    else:
        elements_before_insert = given_list.ListElements
        given_list.ListElements = (
            elements_before_insert[:index]
            + (value_to_insert,)
            + elements_before_insert[index + 1 :]
        )
        given_list.length += 1
    return True


def locate(given_list: List, value_to_find: any) -> any:
    if get_length(given_list) > 0:
        for i in range(len(given_list.ListElements)):
            if given_list.ListElements[i] == value_to_find:
                return i
    return None


def retrieve(given_list: List, index: int) -> any:
    if get_length(given_list) == 0:
        return None
    return given_list.ListElements[index]


def delete(given_list: List, value_to_delete: any) -> bool:
    index_of_deletion = locate(given_list, value_to_delete)
    if index_of_deletion is None:
        return False
    elements_before_delete = given_list.ListElements
    given_list.ListElements = (
        elements_before_delete[:index_of_deletion]
        + elements_before_delete[index_of_deletion + 1 :]
    )
    given_list.length -= 1
    return True
