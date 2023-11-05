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
        if tree_node.key is None:
            tree_node.key = key
            tree_node.value = value_to_put
        elif key == tree_node.key:
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


def traverse(tree_map: Tree[K, V], order: str = "preorder") -> list[V]:
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
                result_values.append(node.value)

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
            return tree_node, value
        elif tree_node.key > key:
            new_left_child, value = remove_recursion(tree_node.left, key)
            tree_node.left = new_left_child
            return tree_node, value
        if tree_node.left is None and tree_node.right is None:
            return None, tree_node.value
        if tree_node.left is None or tree_node.right is None:
            new_node = tree_node.left if tree_node.left is not None else tree_node.right
            return new_node, tree_node.value
        else:
            minimal = find_minimal_son(tree_node.right)
            new_node, value = remove_recursion(tree_node, minimal.key)
            new_node.value = minimal.value
            new_node.key = minimal.key
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
