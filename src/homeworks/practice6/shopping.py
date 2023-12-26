from typing import Optional
import src.homeworks.practice6.avl_tree as avl


def add_size(avl_tree: avl.Tree, clothes_size: int, clothes_count: int) -> None:
    cell = avl.get_cell_by_key(avl_tree, clothes_size)
    if cell is None:
        avl.put_value_by_key(avl_tree, clothes_size, clothes_count)
    else:
        cell.value += clothes_count


def get_count_by_size(avl_tree: avl.Tree, clothes_size: int) -> int:
    try:
        return avl.get_value_by_key(avl_tree, clothes_size)
    except ValueError:
        return 0


def select_thing_by_size(avl_tree: avl.Tree, clothes_size: int) -> Optional[int]:
    try:
        needed_size = avl.get_lower_bound(avl_tree, clothes_size)
    except ValueError:
        return None
    needed_cell = avl.get_cell_by_key(avl_tree, needed_size)
    needed_cell.value -= 1
    if needed_cell.value == 0:
        avl.remove_value_by_key(avl_tree, needed_cell.key)
    return needed_size


def write_store_balance(avl_tree: avl.Tree) -> None:
    with open("my_shop_balance.txt", "w") as file:
        all_cells = avl.traverse_cells(avl_tree, "inorder")
        for cell in all_cells:
            print(cell.key, cell.value, file=file)


def main() -> None:
    size_tree = avl.create_tree()
    with open("shop_logs.txt") as file:
        res_results = open("my_shop_results.txt", "w")
        for string in file:
            command = string.strip().split(" ")
            command_len = len(command)
            if command[0] == "ADD" and command_len == 3:
                add_size(size_tree, int(command[1]), int(command[2]))
            elif command[0] == "GET" and command_len == 2:
                print(get_count_by_size(size_tree, int(command[1])), file=res_results)
            elif command[0] == "SELECT" and command_len == 2:
                result = select_thing_by_size(size_tree, int(command[1]))
                if result is None:
                    print("SORRY", file=res_results)
                else:
                    print(result, file=res_results)
        res_results.close()
    write_store_balance(size_tree)


if __name__ == "__main__":
    main()
