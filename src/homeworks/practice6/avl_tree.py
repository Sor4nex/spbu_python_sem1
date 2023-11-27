import copy
from dataclasses import dataclass
from numbers import Number
from typing import Optional, TypeVar, Generic, Callable, Iterable

AVAILABLE_TYPES = (int, float, str, tuple, list)
K = TypeVar("K", int, float, str, tuple, list)
V = TypeVar("V")


@dataclass
class TreeNode(Generic[K, V]):
    key: K
    value: V
    height: int = 1
    left: Optional["TreeNode[K, V]"] = None
    right: Optional["TreeNode[K, V]"] = None


@dataclass
class Tree(Generic[K, V]):
    type: Optional[type] = None
    root: Optional[TreeNode[K, V]] = None
    size: int = 0


def is_valid_key_type(key_type: type) -> bool:
    return key_type in AVAILABLE_TYPES


def check_correct_key_type(tree_map: Tree[K, V], new_key: K) -> bool:
    return (
        tree_map.type is None
        or isinstance(new_key, tree_map.type)
        or (tree_map.type == int or tree_map.type == float)
        and isinstance(new_key, Number)
    )


def update_height(tree_node: TreeNode[K, V]) -> int:
    left_height = tree_node.left.height if tree_node.left is not None else 0
    right_height = tree_node.right.height if tree_node.right is not None else 0
    return max(left_height, right_height) + 1


def calculate_height_difference(tree_node: TreeNode[K, V]) -> int:
    left_height = tree_node.left.height if tree_node.left is not None else 0
    right_height = tree_node.right.height if tree_node.right is not None else 0
    height_diff = right_height - left_height
    return height_diff


def balance_tree(tree_node: TreeNode[K, V]) -> None:
    def _rebalance_right(tree_node: TreeNode[K, V]) -> None:
        if tree_node.right.right is None and tree_node.left is None:
            tree_node.left = TreeNode(tree_node.key, tree_node.value, 1)
            tree_node.key = tree_node.right.left.key
            tree_node.value = tree_node.right.left.value
            tree_node.right.left = None
            tree_node.right.height = 1
            return None
        tree_node.left = TreeNode(
            tree_node.key,
            tree_node.value,
            tree_node.height,
            tree_node.left,
            tree_node.right.left,
        )
        tree_node.left.height = update_height(tree_node.left)
        tree_node.key = tree_node.right.key
        tree_node.value = tree_node.right.value
        tree_node.right = tree_node.right.right

    def _rebalance_left(tree_node: TreeNode[K, V]) -> None:
        if tree_node.left.left is None and tree_node.right is None:
            tree_node.right = TreeNode(tree_node.key, tree_node.value, 1)
            tree_node.key = tree_node.left.right.key
            tree_node.value = tree_node.left.right.value
            tree_node.left.right = None
            tree_node.left.height = 1
            return None
        tree_node.right = TreeNode(
            tree_node.key,
            tree_node.value,
            tree_node.height - 1,
            tree_node.left.right,
            tree_node.right,
        )
        tree_node.right.height = update_height(tree_node.right)
        tree_node.key = tree_node.left.key
        tree_node.value = tree_node.left.value
        tree_node.left = tree_node.left.left

    height_diff = calculate_height_difference(tree_node)
    if height_diff >= 2:
        _rebalance_right(tree_node)
    elif height_diff <= -2:
        _rebalance_left(tree_node)


def create_tree() -> Tree[K, V]:
    return Tree()


def delete_tree_map(tree_map: Tree[K, V]) -> None:
    def delete_recursively(tree_node: TreeNode[K, V]) -> None:
        if tree_node.right is None and tree_node.left is None:
            del tree_node
        else:
            if tree_node.right is not None:
                delete_recursively(tree_node.right)
                del tree_node.right
            if tree_node.left is not None:
                delete_recursively(tree_node.left)
                del tree_node.left

    if tree_map.size == 0:
        return None
    delete_recursively(tree_map.root)
    del tree_map.size
    del tree_map.type
    del tree_map.root


def put_value_by_key(tree: Tree[K, V], key: K, value_to_put: V) -> None:
    def put_recursively(tree_node: TreeNode[K, V], key: K, value_to_put: V) -> None:
        if key == tree_node.key:
            tree_node.value = value_to_put
        elif key < tree_node.key:
            if tree_node.left is None:
                tree_node.left = TreeNode(key, value_to_put)
            else:
                put_recursively(tree_node.left, key, value_to_put)
        else:
            if tree_node.right is None:
                tree_node.right = TreeNode(key, value_to_put)
            else:
                put_recursively(tree_node.right, key, value_to_put)
        balance_tree(tree_node)
        tree_node.height = update_height(tree_node)

    if not is_valid_key_type(type(key)):
        raise ValueError("this type cannot be used as a BST key")
    if tree.type is not None and not check_correct_key_type(tree, key):
        raise ValueError("this type cannot not be compared with the tree data type")
    if tree.root is None:
        tree.type = type(key)
        tree.root = TreeNode(key, value_to_put)
    else:
        put_recursively(tree.root, key, value_to_put)
    tree.size += 1


def get_value_by_key(tree_map: Tree[K, V], key: K) -> V:
    key_cell = get_cell_by_key(tree_map, key)
    if key_cell is None:
        raise ValueError(f"no key {key} was found")
    return key_cell.value


def get_minimum(tree_map: Tree[K, V]) -> K:
    if tree_map.size == 0:
        raise ValueError("tree is empty")
    return traverse_cells(tree_map, "inorder")[0].key


def get_maximum(tree_map: Tree[K, V]) -> K:
    if tree_map.size == 0:
        raise ValueError("tree is empty")
    return traverse_cells(tree_map, "inorder")[-1].key


def get_all_keys(tree_map: Tree[K, V]) -> list[K]:
    if tree_map.size == 0:
        raise ValueError("tree is empty")
    return list(map(lambda cell: cell.key, traverse_cells(tree_map, "inorder")))


def getAll(tree_map: Tree[K, V], left: K, right: K) -> list[K]:
    return list(filter(lambda key: left <= key <= right, get_all_keys(tree_map)))


def get_lower_bound(tree_map: Tree[K, V], key: K) -> K:
    all_keys = get_all_keys(tree_map)
    keys_lower_bound = list(filter(lambda elem: elem >= key, all_keys))
    if len(keys_lower_bound) == 0:
        raise ValueError("such key does not exist")
    return keys_lower_bound[0]


def get_upper_bound(tree_map: Tree[K, V], key: K) -> K:
    all_keys = get_all_keys(tree_map)
    keys_upper_bound = list(filter(lambda elem: elem > key, all_keys))
    if len(keys_upper_bound) == 0:
        raise ValueError("such key does not exist")
    return keys_upper_bound[0]


def traverse_cells(
    tree_map: Tree[K, V], order: str = "preorder"
) -> list[TreeNode[K, V]]:
    result_values = []

    def _preorder_comparator(tree_node: TreeNode[K, V]) -> Iterable[TreeNode[K, V]]:
        return filter(None, (tree_node, tree_node.left, tree_node.right))

    def _inorder_comparator(tree_node: TreeNode[K, V]) -> Iterable[TreeNode[K, V]]:
        return filter(None, (tree_node.left, tree_node, tree_node.right))

    def _postorder_comparator(tree_node: TreeNode[K, V]) -> Iterable[TreeNode[K, V]]:
        return filter(None, (tree_node.left, tree_node.right, tree_node))

    def traverse_recursion(
        tree_node: TreeNode[K, V],
        order_function: Callable[[TreeNode[K, V]], Iterable[TreeNode[K, V]]],
    ) -> None:
        node_order = order_function(tree_node)
        for node in node_order:
            if node is not tree_node:
                traverse_recursion(node, order_function)
            else:
                result_values.append(node)

    if tree_map.root is None:
        raise ValueError("cannot traverse empty Tree")
    if order == "preorder":
        traverse_recursion(tree_map.root, _preorder_comparator)
    elif order == "inorder":
        traverse_recursion(tree_map.root, _inorder_comparator)
    elif order == "postorder":
        traverse_recursion(tree_map.root, _postorder_comparator)
    else:
        raise ValueError(
            f"no such order: {order}. Valid orders are: preorder, inorder, postorder"
        )
    return result_values


def traverse(tree_map: Tree[K, V], order: str = "preorder") -> list[V]:
    return list(map(lambda cell: cell.value, traverse_cells(tree_map, order)))


def remove_value_by_key(tree_map: Tree[K, V], key: K) -> V:
    if not has_key(tree_map, key):
        raise ValueError(f"No such key {key}")
    tree_map.root, value = _remove_recursion(tree_map.root, key)
    tree_map.size -= 1
    return value


def _remove_recursion(tree_node: TreeNode[K, V], key: K) -> tuple[Optional[TreeNode[K, V]], V]:
    def find_minimal_son(tree_node: TreeNode[K, V]) -> TreeNode[K, V]:
        if tree_node.left is not None:
            return find_minimal_son(tree_node.left)
        return tree_node

    if tree_node.key < key:
        new_right_child, value = _remove_recursion(tree_node.right, key)
        tree_node.right = new_right_child
        balance_tree(tree_node)
        tree_node.height = update_height(tree_node)
        return tree_node, value
    elif tree_node.key > key:
        new_left_child, value = _remove_recursion(tree_node.left, key)
        tree_node.left = new_left_child
        balance_tree(tree_node)
        tree_node.height = update_height(tree_node)
        return tree_node, value
    if tree_node.left is None and tree_node.right is None:
        return None, tree_node.value
    if tree_node.left is None or tree_node.right is None:
        new_node = tree_node.left if tree_node.left is not None else tree_node.right
        return new_node, tree_node.value
    else:
        minimal = find_minimal_son(tree_node.right)
        new_node_right, value = _remove_recursion(tree_node.right, minimal.key)
        new_node = TreeNode(
            minimal.key,
            minimal.value,
            tree_node.height,
            tree_node.left,
            new_node_right,
        )
        balance_tree(tree_node)
        new_node.height = update_height(tree_node)
        return new_node, value


def remove_keys(tree_map: Tree[K, V], left: K, right: K) -> None:
    def remove_keys_recursively(tree_node: TreeNode[K, V], left: K, right: K, deleted_keys_count: int) -> tuple[Optional[TreeNode[K, V]], int]:
        if tree_node.left is None and tree_node.right is None:
            if left <= tree_node.key <= right:
                return None, deleted_keys_count + 1
            return tree_node, deleted_keys_count
        tree_node.left, deleted_keys_count = remove_keys_recursively(tree_node.left, left, right, deleted_keys_count) if tree_node.left is not None else (None, deleted_keys_count)
        tree_node.right, deleted_keys_count = remove_keys_recursively(tree_node.right, left, right, deleted_keys_count) if tree_node.right is not None else (None, deleted_keys_count)
        if left <= tree_node.key <= right:
            tree_node = _remove_recursion(tree_node, tree_node.key)[0]
            deleted_keys_count += 1
        if tree_node is not None:
            balance_tree(tree_node)
            tree_node.height = update_height(tree_node)
        return tree_node, deleted_keys_count

    if tree_map.size == 0:
        raise ValueError("no keys in the tree")
    tree_map.root, deleted_keys_count = remove_keys_recursively(tree_map.root, left, right, 0)
    tree_map.size -= deleted_keys_count


def get_cell_by_key(tree_map: Tree[K, V], key: K) -> Optional[TreeNode[K, V]]:
    def get_cell_recursively(
        tree_node: TreeNode[K, V], key: K
    ) -> Optional[TreeNode[K, V]]:
        if key == tree_node.key:
            return tree_node
        elif tree_node.right is not None and key > tree_node.key:
            return get_cell_recursively(tree_node.right, key)
        elif tree_node.left is not None and key < tree_node.key:
            return get_cell_recursively(tree_node.left, key)
        return None

    if tree_map.size == 0:
        return None
    return get_cell_recursively(tree_map.root, key)


def has_key(tree_map: Tree[K, V], key: K) -> bool:
    key_cell = get_cell_by_key(tree_map, key)
    return key_cell is not None


def join(tree_map: Tree[K, V], another: Tree[K, V]) -> None:
    def get_min_cell(tree_node: TreeNode[K, V]) -> TreeNode[K, V]:
        return tree_node if tree_node.left is None else get_min_cell(tree_node.left)

    def get_max_cell(tree_node: TreeNode[K, V]) -> TreeNode[K, V]:
        return tree_node if tree_node.right is None else get_max_cell(tree_node.right)

    def merge_minor_major_trees(tree_minor: Tree[K, V], tree_major: Tree[K, V]) -> tuple[TreeNode[K, V], int]:
        def get_approximate_height_cell(tree_node: TreeNode[K, V], given_height: int) -> TreeNode[K, V]:
            if tree_node.height <= given_height + 1:
                return tree_node
            return get_approximate_height_cell(tree_node.left, given_height)

        new_size = tree_minor.size + tree_major.size
        tree_minor_max_cell = get_max_cell(tree_minor.root)
        remove_value_by_key(tree_minor, tree_minor_max_cell.key)
        approximate_height_cell = get_approximate_height_cell(tree_major.root, tree_minor.root.height if tree_minor.root is not None else 0)

        approximate_height_cell.right = copy.deepcopy(approximate_height_cell)
        approximate_height_cell.key, approximate_height_cell.value = tree_minor_max_cell.key, tree_minor_max_cell.value
        approximate_height_cell.left = tree_minor.root
        balance_tree(approximate_height_cell)
        approximate_height_cell.height = update_height(approximate_height_cell)
        return tree_major.root, new_size

    def merge_mixed_trees(tree1: Tree[K, V], tree2: Tree[K, V]) -> TreeNode[K, V]:
        cell_to_join = traverse_cells(tree2)
        for cell in cell_to_join:
            put_value_by_key(tree1, cell.key, cell.value)
        return tree1.root

    if tree_map.size == 0 or another.size == 0:
        raise ValueError('some tree has no elements')
    tree1_min, tree1_max = get_min_cell(tree_map.root).key, get_max_cell(tree_map.root).key
    tree2_min, tree2_max = get_min_cell(another.root).key, get_max_cell(another.root).key
    if tree1_max < tree2_min:
        tree_map.root, tree_map.size = merge_minor_major_trees(tree_map, another)
    elif tree1_min > tree2_max:
        tree_map.root, tree_map.size = merge_minor_major_trees(another, tree_map)
    if tree_map.size >= another.size:
        tree_map.root = merge_mixed_trees(tree_map, another)
    else:
        tree_map.root = merge_mixed_trees(another, tree_map)


def split(tree_map: Tree[K, V], key: K) -> tuple[Tree[K, V], Tree[K, V]]:
    all_cells = traverse_cells(tree_map, "inorder")
    tree1, tree2 = create_tree(), create_tree()
    for cell in all_cells:
        if cell.key < key:
            put_value_by_key(tree1, cell.key, cell.value)
        else:
            put_value_by_key(tree2, cell.key, cell.value)
    return tree1, tree2
