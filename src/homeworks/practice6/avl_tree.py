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

    def find_minimal_son(tree_node: TreeNode[K, V]) -> TreeNode[K, V]:
        if tree_node.left is not None:
            return find_minimal_son(tree_node.left)
        return tree_node

    def remove_recursion(
        tree_node: TreeNode[K, V], key: K
    ) -> tuple[Optional[TreeNode[K, V]], V]:
        if tree_node.key < key:
            new_right_child, value = remove_recursion(tree_node.right, key)
            tree_node.right = new_right_child
            balance_tree(tree_node)
            tree_node.height = update_height(tree_node)
            return tree_node, value
        elif tree_node.key > key:
            new_left_child, value = remove_recursion(tree_node.left, key)
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
            new_node_right, value = remove_recursion(tree_node.right, minimal.key)
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

    tree_map.root, value = remove_recursion(tree_map.root, key)
    tree_map.size -= 1
    return value


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
