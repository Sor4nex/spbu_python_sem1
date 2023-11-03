from dataclasses import dataclass
from typing import Any, Optional, TypeVar, Generic, Callable, Iterable

AVAILABLE_TYPES = (type(int()), type(float()), type(str()), type(list()), type(tuple()))
V = TypeVar("V")


@dataclass
class TreeNode(Generic[V]):
    left: Optional["TreeNode[V]"] = None
    right: Optional["TreeNode[V]"] = None
    value: Optional[Any] = None
    key: Optional[Any] = None


@dataclass
class Tree(Generic[V]):
    type: Optional[Any] = None
    root: Optional[TreeNode[V]] = None
    size: int = 0


def is_valid_key_type(key_type: type) -> bool:
    if key_type in AVAILABLE_TYPES:
        return True
    return False


def check_correct_key_type(tree_type: type, new_key: Any) -> bool:
    if tree_type is None or isinstance(new_key, tree_type):
        return True
    if (tree_type == type(float()) and isinstance(new_key, type(int()))) or (
        tree_type == type(int()) and isinstance(new_key, type(float()))
    ):
        return True
    return False


def create_tree() -> Tree[V]:
    return Tree()


def delete_tree_map(tree_map: Tree[V]) -> None:
    try:
        all_keys = traverse(tree_map, "inorder")
        for key in all_keys:
            remove_value_by_key(tree_map, key)
        tree_map.type = None
    except ValueError:
        raise ValueError("tree is already empty")


def put_value_by_key(tree: Tree[V], key: Any, value_to_put: Any) -> None:
    def put_recursively(tree_node: TreeNode[V], key: Any, value_to_put: Any) -> None:
        if tree_node.key is None:
            tree_node.key = key
            tree_node.value = value_to_put
        elif key == tree_node.key:
            tree_node.value = value_to_put
        elif key < tree_node.key:
            if tree_node.left is None:
                tree_node.left = TreeNode()
            put_recursively(tree_node.left, key, value_to_put)
        else:
            if tree_node.right is None:
                tree_node.right = TreeNode()
            put_recursively(tree_node.right, key, value_to_put)

    if not is_valid_key_type(type(key)):
        raise ValueError("this type cannot be used as a BST key")
    if tree.type is not None and not check_correct_key_type(tree.type, key):
        raise ValueError("this type cannot not be compared with the tree data type")
    if tree.root is None:
        tree.type = type(key)
        tree.root = TreeNode(key=key, value=value_to_put)
    else:
        put_recursively(tree.root, key, value_to_put)
    tree.size += 1


def get_value_by_key(tree_map: Tree[V], key: Any) -> Any:
    def get_value_recursively(tree_node: TreeNode[V], key: Any) -> Any:
        if tree_node.key == key:
            return tree_node.value
        elif key < tree_node.key:
            if tree_node.left is None:
                raise ValueError(f"key {key} does not exist")
            return get_value_recursively(tree_node.left, key)
        else:
            if tree_node.right is None:
                raise ValueError(f"key {key} does not exist")
            return get_value_recursively(tree_node.right, key)

    if tree_map.size == 0:
        raise ValueError(f"key {key} does not exist")
    try:
        return get_value_recursively(tree_map.root, key)
    except ValueError:
        raise


def traverse(tree_map: Tree[V], order: str = "preorder") -> list[V]:
    result_values = []

    def _preorder_comparator(tree_node: TreeNode[V]) -> Iterable[TreeNode[V]]:
        return filter(None, (tree_node, tree_node.left, tree_node.right))

    def _inorder_comparator(tree_node: TreeNode[V]) -> Iterable[TreeNode[V]]:
        return filter(None, (tree_node.left, tree_node, tree_node.right))

    def _postorder_comparator(tree_node: TreeNode[V]) -> Iterable[TreeNode[V]]:
        return filter(None, (tree_node.left, tree_node.right, tree_node))

    def traverse_recursion(tree_node: TreeNode[V], order_function: Callable):
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
    return result_values


def remove_value_by_key(tree_map: Tree[V], key: Any) -> Any:
    if not has_key(tree_map, key):
        raise ValueError(f"No such key {key}")

    def find_minimal_son(tree_map: TreeNode[V]) -> Any:
        if tree_map.left is not None:
            return find_minimal_son(tree_map.left)
        return tree_map

    def remove_recursion(
        tree_node: TreeNode[V], key: Any
    ) -> tuple[Optional[TreeNode[V]], key]:
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


def has_key(tree_map: Tree[V], key: Any) -> bool:
    try:
        get_value_by_key(tree_map, key)
    except ValueError:
        return False
    return True
