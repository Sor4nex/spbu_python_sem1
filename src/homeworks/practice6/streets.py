from typing import Optional
import src.homeworks.practice6.avl_tree as avl
from os.path import isfile


INPUT_FILE_EXISTENCE_ERROR = "Error: input file does not exist"
MODE_EXISTENCE_ERROR = "Error: such mode does not exist. Choose between given options"
INTERACTIVE_MODE_REMINDER = """Interactive mode. Available commands: CREATE, GET, RENAME, DELETE_BLOCK, DELETE_HOUSE, DELETE_STREET, LIST.
To exit program type EXIT"""
STRING_RESULT = "Result:"
STRING_SUCCESSFUL = "successful"
DELETE_ERROR = "Error: such object not found"
COMMAND_EXISTENCE_ERROR = "Error: such command does not exist"
ARGUMENT_COUNT_ERROR = "Error: wrong number of arguments"


def check_argument_count(user_input: list, needed_count) -> bool:
    return len(user_input) == needed_count


def clear_street(tree_map: avl.Tree, street: avl.TreeNode) -> None:
    if len(street.value) == 0:
        avl.remove_value_by_key(tree_map, street.key)


def create_house(
    tree_map: avl.Tree, street_name: str, house: int, housing: int, index: int
) -> None:
    street = avl.get_cell_by_key(tree_map, street_name)
    if street is None:
        avl.put_value_by_key(tree_map, street_name, [(house, housing, index)])
        return
    street.value.append((house, housing, index))


def get_house(
    tree_map: avl.Tree, street_name: str, house: int, housing: int
) -> Optional[int]:
    street = avl.get_cell_by_key(tree_map, street_name)
    if street is None:
        return None
    for houses in street.value:
        if houses[0] == house and houses[1] == housing:
            return houses[2]


def rename_street(tree_map: avl.Tree, street_name: str, new_name: str) -> None:
    street = avl.get_cell_by_key(tree_map, street_name)
    all_houses = street.value
    avl.remove_value_by_key(tree_map, street_name)
    avl.put_value_by_key(tree_map, new_name, all_houses)


def delete_block(
    tree_map: avl.Tree, street_name: str, house: int, housing: int
) -> None:
    street = avl.get_cell_by_key(tree_map, street_name)
    if street is None:
        raise ValueError(f"no street ", street_name)
    for houses in street.value:
        if houses[0] == house and houses[1] == housing:
            street.value.remove(houses)
            return
    clear_street(tree_map, street)
    raise ValueError(f"no house on ", street_name, house, housing)


def delete_house(tree_map: avl.Tree, street_name: str, house: int) -> None:
    street = avl.get_cell_by_key(tree_map, street_name)
    for houses in street.value:
        if houses[0] == house:
            street.value.remove(houses)
    clear_street(tree_map, street)


def delete_street(tree_map: avl.Tree, street_name: str) -> None:
    avl.remove_value_by_key(tree_map, street_name)


def list_houses(
    tree_map: avl.Tree, address_left: list, address_right: list
) -> list[str]:
    result = []
    all_streets = avl.traverse_cells(tree_map)
    for street in all_streets:
        for houses in street.value:
            address = [street.key] + list(houses[:-1])
            if address_left <= address < address_right:
                result.append(address)
    return list(
        map(
            lambda address: address[0] + " " + str(address[1]) + " " + str(address[2]),
            sorted(result),
        )
    )


def mode_static(file_input: str, file_ouput: str) -> None:
    streets = avl.create_tree()
    with open(file_input, "r", encoding="utf-8") as input_file:
        output_file = open(file_ouput, "w", encoding="utf-8")
        for string in input_file:
            command = string.strip().split(" ")
            if len(command) == 1:
                continue
            if command[0] == "CREATE":
                create_house(
                    streets,
                    command[1],
                    int(command[2]),
                    int(command[3]),
                    int(command[4]),
                )
            elif command[0] == "GET":
                print(
                    get_house(streets, command[1], int(command[2]), int(command[3])),
                    file=output_file,
                )
            elif command[0] == "RENAME":
                rename_street(streets, command[1], command[2])
            elif command[0] == "DELETE_BLOCK":
                try:
                    delete_block(streets, command[1], int(command[2]), int(command[3]))
                except ValueError:
                    pass
            elif command[0] == "DELETE_HOUSE":
                try:
                    delete_house(streets, command[1], int(command[2]))
                except AttributeError:
                    pass
            elif command[0] == "DELETE_STREET":
                try:
                    delete_street(streets, command[1])
                except ValueError:
                    pass
            elif command[0] == "LIST":
                result = list_houses(
                    streets,
                    [command[1], int(command[2]), int(command[3])],
                    [command[4], int(command[5]), int(command[6])],
                )
                for house in result:
                    print(house, file=output_file)
                print(file=output_file)
        output_file.close()


def mode_interactive() -> None:
    streets = avl.create_tree()
    print(INTERACTIVE_MODE_REMINDER)
    command = ""
    while command != ["EXIT"]:
        command = input("Command: ")
        command = command.split(" ")
        if command[0] == "CREATE":
            if not check_argument_count(command, 5):
                print(ARGUMENT_COUNT_ERROR)
                continue
            create_house(
                streets, command[1], int(command[2]), int(command[3]), int(command[4])
            )
            print(STRING_RESULT, STRING_SUCCESSFUL)
        elif command[0] == "GET":
            if not check_argument_count(command, 4):
                print(ARGUMENT_COUNT_ERROR)
                continue
            print(
                STRING_RESULT,
                get_house(streets, command[1], int(command[2]), int(command[3])),
            )
        elif command[0] == "RENAME":
            if not check_argument_count(command, 3):
                print(ARGUMENT_COUNT_ERROR)
            rename_street(streets, command[1], command[2])
            print(STRING_RESULT, STRING_SUCCESSFUL)
        elif command[0] == "DELETE_BLOCK":
            if check_argument_count(command, 4):
                print(ARGUMENT_COUNT_ERROR)
                continue
            try:
                delete_block(streets, command[1], int(command[2]), int(command[3]))
                print(STRING_RESULT, STRING_SUCCESSFUL)
            except ValueError:
                print(STRING_RESULT, DELETE_ERROR)
        elif command[0] == "DELETE_HOUSE":
            if not check_argument_count(command, 3):
                print(ARGUMENT_COUNT_ERROR)
                continue
            try:
                delete_house(streets, command[1], int(command[2]))
                print(STRING_RESULT, STRING_SUCCESSFUL)
            except AttributeError:
                print(STRING_RESULT, DELETE_ERROR)
        elif command[0] == "DELETE_STREET":
            if not check_argument_count(command, 2):
                print(ARGUMENT_COUNT_ERROR)
                continue
            try:
                delete_street(streets, command[1])
                print(STRING_RESULT, STRING_SUCCESSFUL)
            except ValueError:
                print(STRING_RESULT, DELETE_ERROR)
        elif command[0] == "LIST":
            if not check_argument_count(command, 7):
                print(ARGUMENT_COUNT_ERROR)
                continue
            result = list_houses(
                streets,
                [command[1], int(command[2]), int(command[3])],
                [command[4], int(command[5]), int(command[6])],
            )
            print(STRING_RESULT)
            for house in result:
                print(house)
        elif command[0] != "EXIT":
            print(COMMAND_EXISTENCE_ERROR)


def main() -> None:
    command = input("mode: ")
    if command == "1":
        mode_interactive()
        return
    elif command == "2":
        file_input = input("type input file: ")
        file_output = input("type output file: ")
        if isfile(file_input):
            mode_static(file_input, file_output)
            return
        print(INPUT_FILE_EXISTENCE_ERROR)
        return
    print(MODE_EXISTENCE_ERROR)


if __name__ == "__main__":
    main()
