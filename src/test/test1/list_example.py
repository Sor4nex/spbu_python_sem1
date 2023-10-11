from list import *


def print_brief_info(given_list: List) -> None:
    print(get_length(given_list))
    print(head(given_list))
    print(tail(given_list))


if __name__ == "__main__":
    list1 = create()
    print_brief_info(list1)
    insert(list1, "hello", 0)
    print_brief_info(list1)
    insert(list1, "im here", 1)
    print_brief_info(list1)
    delete(list1, 0)
    print_brief_info(list1)
    insert(list1, "1", 1)
    insert(list1, "2", 2)
    print(locate(list1, "1"))
    print(retrieve(list1, "2"))
