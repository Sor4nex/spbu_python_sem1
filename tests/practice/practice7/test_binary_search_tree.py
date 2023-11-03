import pytest
from pytest import *
from src.practice.practice7.binary_search_tree import *


def make_dummy(input_keys_list: list, input_values_list: list) -> Tree:
    tree = create_tree()
    for i in range(len(input_keys_list)):
        put_value_by_key(tree, input_keys_list[i], input_values_list[i])
    return tree


@pytest.mark.parametrize(
    "key_type,expected",
    [
        (type("abc"), True),
        (type("123"), True),
        (type(1), True),
        (type(2.1), True),
        (type([1, 2, 3]), True),
        (type((1, 2, 3)), True),
        (type({"1": 2, "2": 3}), False),
        (type(create_tree()), False),
    ],
)
def test_is_valid_key_type(key_type: type, expected: bool) -> None:
    result = is_valid_key_type(key_type)
    assert result == expected


@pytest.mark.parametrize(
    "tree_type,new_key,expected",
    [
        (make_dummy([1, 2, 3], ["foo", "foo", "foo"]).type, 55, True),
        (make_dummy(["1", "2", "3"], ["foo", "foo", "foo"]).type, "4", True),
        (make_dummy([1, 2, 3], ["foo", "foo", "foo"]).type, "4", False),
        (make_dummy([1, 2, 3], ["foo", "foo", "foo"]).type, [1, 2, 3], False),
        (
            make_dummy([[1, 2, 3], [2, 3, 4], [5]], ["foo", "foo", "foo"]).type,
            [1, 2, 3],
            True,
        ),
        (make_dummy([1, 2, 3], ["foo", "foo", "foo"]).type, 4.3, True),
        (make_dummy([1.3, 2.2, 3.4], ["foo", "foo", "foo"]).type, 4, True),
        (make_dummy([[1], [2], [3]], ["foo", "foo", "foo"]).type, (5, 9), False),
    ],
)
def test_check_correct_value_type(
    tree_type: type, new_key: Any, expected: bool
) -> None:
    result = check_correct_key_type(tree_type, new_key)
    assert result == expected


@pytest.mark.parametrize(
    "tree_map,key,expected",
    [
        (make_dummy([5, 4, 6], ["a", "b", "c"]), 4, "b"),
        (
            make_dummy([5, 4, 6, 10, 9, 8, 7], ["a", "b", "c", "d", "e", "f", "g"]),
            7,
            "g",
        ),
        (make_dummy([1], [0]), 1, 0),
    ],
)
def test_get_value_by_key(tree_map: Tree, key: Any, expected: Any) -> None:
    result = get_value_by_key(tree_map, key)
    assert result == expected


@pytest.mark.parametrize(
    "tree_map,key",
    [
        (make_dummy([5, 4, 6], ["a", "b", "c"]), 1),
        (make_dummy([], []), 5),
        (make_dummy([1], [1]), 5),
    ],
)
def test_get_value_by_key_exception_case(tree_map: Tree, key: Any) -> None:
    with pytest.raises(ValueError):
        get_value_by_key(tree_map, key)


@pytest.mark.parametrize(
    "tree_map,key,expected",
    [
        (make_dummy([5, 4, 6], ["a", "b", "c"]), 4, True),
        (
            make_dummy([5, 4, 6, 10, 9, 8, 7], ["a", "b", "c", "d", "e", "f", "g"]),
            7,
            True,
        ),
        (make_dummy([1], [0]), 1, True),
        (make_dummy([5, 4, 6], ["a", "b", "c"]), 1, False),
        (make_dummy([], []), 5, False),
        (make_dummy([1], [1]), 5, False),
    ],
)
def test_has_key(tree_map: Tree, key: Any, expected: bool) -> None:
    result = has_key(tree_map, key)
    assert result == expected


@pytest.mark.parametrize(
    "tree_map,order,expected",
    [
        (
            make_dummy(
                [20, 5, 1, 15, 9, 7, 12, 30, 25, 40], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ),
            "preorder",
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ),
        (
            make_dummy(
                [40, 25, 10, 3, 17, 32, 30, 38, 78, 50, 64, 93],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ),
            "preorder",
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        ),
        (
            make_dummy(
                [20, 5, 1, 15, 9, 7, 12, 30, 25, 40], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ),
            "inorder",
            [3, 2, 6, 5, 7, 4, 1, 9, 8, 10],
        ),
        (
            make_dummy(
                [40, 25, 10, 3, 17, 32, 30, 38, 78, 50, 64, 93],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ),
            "inorder",
            [4, 3, 5, 2, 7, 6, 8, 1, 10, 11, 9, 12],
        ),
        (
            make_dummy(
                [20, 5, 1, 15, 9, 7, 12, 30, 25, 40], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ),
            "postorder",
            [3, 6, 7, 5, 4, 2, 9, 10, 8, 1],
        ),
        (
            make_dummy(
                [40, 25, 10, 3, 17, 32, 30, 38, 78, 50, 64, 93],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ),
            "postorder",
            [4, 5, 3, 7, 8, 6, 2, 11, 10, 12, 9, 1],
        ),
        (make_dummy([1], [1]), "preorder", [1]),
    ],
)
def test_traverse(tree_map: Tree[V], order: str, expected: list[V]) -> None:
    result = traverse(tree_map, order)
    assert result == expected


def test_traverse_exception_case() -> None:
    with pytest.raises(ValueError):
        traverse(make_dummy([], []), "preorder")


@pytest.mark.parametrize(
    "tree_map,key,value_to_put,expected",
    [
        (
            make_dummy(
                [20, 5, 1, 15, 9, 7, 12, 30, 25, 40], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ),
            6,
            "11",
            [1, 2, 3, 4, 5, 6, "11", 7, 8, 9, 10],
        ),
        (
            make_dummy(
                [20, 5, 1, 15, 9, 7, 12, 30, 25, 40], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ),
            49,
            "11",
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "11"],
        ),
        (
            make_dummy(
                [40, 25, 10, 3, 17, 32, 30, 38, 78, 50, 93],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            ),
            64.4,
            "abdsf",
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "abdsf", 11],
        ),
        (
            make_dummy(
                [40, 25, 10, 3, 17, 32, 30, 38, 78, 50, 93],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            ),
            64,
            12,
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11],
        ),
        (make_dummy([], []), 1, 4, [4]),
        (make_dummy([1], [1]), 2, 5, [1, 5]),
    ],
)
def test_put_value_by_key(
    tree_map: Tree[V], key: Any, value_to_put: Any, expected: list[V]
) -> None:
    put_value_by_key(tree_map, key, value_to_put)
    result = traverse(tree_map, "preorder")
    assert result == expected


@pytest.mark.parametrize(
    "tree_map,key,value_to_put",
    [
        (
            make_dummy(
                [20, 5, 1, 15, 9, 7, 12, 30, 25, 40], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ),
            "ads",
            "11",
        ),
        (
            make_dummy(
                [20, 5, 1, 15, 9, 7, 12, 30, 25, 40], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ),
            {"1": 1, "2": 2},
            "11",
        ),
    ],
)
def test_put_value_by_key_exception_cases(
    tree_map: Tree[V], key: Any, value_to_put: Any
) -> None:
    with pytest.raises(ValueError):
        put_value_by_key(tree_map, key, value_to_put)


@pytest.mark.parametrize(
    "tree_map,key,expected",
    [
        (make_dummy([0, 1, 2], [0, 1, 2]), 2, [0, 1]),
        (make_dummy([0, 1, 3, 2], [0, 1, 3, 2]), 3, [0, 1, 2]),
        (
            make_dummy(
                [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
                [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
            ),
            9,
            [5, 0, -10, 3, 7, 11, 8, 14, 12, 13, 15],
        ),
        (
            make_dummy(
                [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
                [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
            ),
            0,
            [5, 3, -10, 7, 9, 8, 14, 12, 11, 13, 15],
        ),
    ],
)
def test_remove_value_by_key(tree_map: Tree[V], key: Any, expected) -> None:
    remove_value_by_key(tree_map, key)
    result = traverse(tree_map)
    assert result == expected


@pytest.mark.parametrize(
    "tree_map,key",
    [
        (make_dummy([0, 1, 2], [0, 1, 2]), 5),
        (make_dummy([0, 1, 3, 2], [0, 1, 3, 2]), 123),
        (
            make_dummy(
                [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
                [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
            ),
            981234,
        ),
        (
            make_dummy(
                [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
                [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
            ),
            -1,
        ),
    ],
)
def test_remove_value_by_key(tree_map: Tree[V], key: Any) -> None:
    with pytest.raises(ValueError):
        remove_value_by_key(tree_map, key)


def test_delete_tree_map() -> None:
    tree_map = make_dummy(
        [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
        [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
    )
    delete_tree_map(tree_map)
    assert tree_map == create_tree()


def test_delete_tree_map_exception_case() -> None:
    tree_map = make_dummy([], [])
    with pytest.raises(ValueError):
        delete_tree_map(tree_map)
