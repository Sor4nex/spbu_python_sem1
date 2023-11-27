import pytest
from src.homeworks.practice6.avl_tree import *


def make_dummy(input_keys_list: list[K], input_values_list: list[V]) -> Tree[K, V]:
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
    "tree_map,new_key,expected",
    [
        (make_dummy([1, 2, 3], ["foo", "foo", "foo"]), 55, True),
        (make_dummy(["1", "2", "3"], ["foo", "foo", "foo"]), "4", True),
        (make_dummy([1, 2, 3], ["foo", "foo", "foo"]), "4", False),
        (make_dummy([1, 2, 3], ["foo", "foo", "foo"]), [1, 2, 3], False),
        (
            make_dummy([[1, 2, 3], [2, 3, 4], [5]], ["foo", "foo", "foo"]),
            [1, 2, 3],
            True,
        ),
        (make_dummy([1, 2, 3], ["foo", "foo", "foo"]), 4.3, True),
        (make_dummy([1.3, 2.2, 3.4], ["foo", "foo", "foo"]), 4, True),
        (make_dummy([[1], [2], [3]], ["foo", "foo", "foo"]), (5, 9), False),
    ],
)
def test_check_correct_value_type(
    tree_map: Tree[K, V], new_key: K, expected: bool
) -> None:
    result = check_correct_key_type(tree_map, new_key)
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
def test_get_value_by_key(tree_map: Tree[K, V], key: K, expected: V) -> None:
    result = get_value_by_key(tree_map, key)
    assert result == expected


@pytest.mark.parametrize(
    "tree_map,key",
    [
        (make_dummy([5, 4, 6], ["a", "b", "c"]), 1),
        (make_dummy([], []), 5),
        (create_tree(), 0),
        (make_dummy([1], [1]), 5),
    ],
)
def test_get_value_by_key_exception_case(tree_map: Tree[K, V], key: K) -> None:
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
        (create_tree(), 4, False),
        (make_dummy([1], [1]), 5, False),
    ],
)
def test_has_key(tree_map: Tree[K, V], key: K, expected: bool) -> None:
    result = has_key(tree_map, key)
    assert result == expected


@pytest.mark.parametrize(
    "tree_map,order,expected",
    [
        (
            make_dummy(
                [10, 5, 1, 4, 35, 20, 99, 31, 17], [10, 5, 1, 4, 35, 20, 99, 31, 17]
            ),
            "preorder",
            [5, 1, 4, 20, 10, 17, 35, 31, 99],
        ),
        (
            make_dummy([8, 3, 10, 1, 6, 14, 4, 7, 13], [8, 3, 10, 1, 6, 14, 4, 7, 13]),
            "preorder",
            [8, 3, 1, 6, 4, 7, 13, 10, 14],
        ),
        (
            make_dummy(
                [20, 5, 30, 1, 15, 25, 40, 9, 7, 12],
                [20, 5, 30, 1, 15, 25, 40, 9, 7, 12],
            ),
            "inorder",
            [1, 5, 7, 9, 12, 15, 20, 25, 30, 40],
        ),
        (
            make_dummy(
                [10, 5, 1, 4, 35, 20, 99, 31, 17], [10, 5, 1, 4, 35, 20, 99, 31, 17]
            ),
            "inorder",
            [1, 4, 5, 10, 17, 20, 31, 35, 99],
        ),
        (
            make_dummy(
                [10, 5, 1, 4, 35, 20, 99, 31, 17], [10, 5, 1, 4, 35, 20, 99, 31, 17]
            ),
            "postorder",
            [4, 1, 17, 10, 31, 99, 35, 20, 5],
        ),
        (
            make_dummy(
                [20, 5, 30, 1, 15, 25, 40, 9, 7, 12],
                [20, 5, 30, 1, 15, 25, 40, 9, 7, 12],
            ),
            "postorder",
            [1, 7, 5, 12, 15, 9, 25, 40, 30, 20],
        ),
        (make_dummy([1], [1]), "preorder", [1]),
    ],
)
def test_traverse(tree_map: Tree[K, V], order: str, expected: list[V]) -> None:
    result = traverse(tree_map, order)
    assert result == expected


@pytest.mark.parametrize(
    "tree_map,order",
    [(create_tree(), "preorder"), (make_dummy([1, 2, 3], [3, 4, 5]), "monkeflipPOG:D")],
)
def test_traverse_exception_case(tree_map: Tree[K, V], order: str) -> None:
    with pytest.raises(ValueError):
        traverse(tree_map, order)


@pytest.mark.parametrize(
    "tree_map,key,value_to_put,expected",
    [
        (
            make_dummy(
                [20, 5, 30, 25, 40, 1, 15, 9, 7, 12],
                [20, 5, 30, 25, 40, 1, 15, 9, 7, 12],
            ),
            26,
            200,
            [20, 9, 5, 1, 7, 15, 12, 30, 25, 200, 40],
        ),
        (
            make_dummy([8, 3, 10, 14, 13, 1, 6, 4, 7], [8, 3, 10, 14, 13, 1, 6, 4, 7]),
            8,
            929,
            [929, 3, 1, 6, 4, 7, 13, 10, 14],
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
    tree_map: Tree[K, V], key: K, value_to_put: V, expected: list[K, V]
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
    tree_map: Tree[K, V], key: K, value_to_put: V
) -> None:
    with pytest.raises(ValueError):
        put_value_by_key(tree_map, key, value_to_put)


@pytest.mark.parametrize(
    "tree_map,key,expected",
    [
        (
            make_dummy([50, 30, 40, 70, 60, 80], [50, 30, 40, 70, 60, 80]),
            30,
            [40, 50, 60, 70, 80],
        ),
        (
            make_dummy(
                [5, 2, 1, 3, 4, 7, 6, 9, 8, 10], [5, 2, 1, 3, 4, 7, 6, 9, 8, 10]
            ),
            2,
            [1, 3, 4, 5, 6, 7, 8, 9, 10],
        ),
        (make_dummy([10, 5], [10, 5]), 10, [5]),
    ],
)
def test_remove_value_by_key(tree_map: Tree[K, V], key: K, expected: list[V]) -> None:
    remove_value_by_key(tree_map, key)
    result = traverse(tree_map, "inorder")
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
def test_remove_value_by_key_exception_cases(tree_map: Tree[K, V], key: K) -> None:
    with pytest.raises(ValueError):
        remove_value_by_key(tree_map, key)


@pytest.mark.parametrize(
    "tree_map",
    [
        (
            make_dummy(
                [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
                [5, 0, -10, 3, 7, 9, 8, 14, 12, 11, 13, 15],
            )
        ),
        (create_tree()),
    ],
)
def test_delete_tree_map(tree_map: Tree[K, V]) -> None:
    delete_tree_map(tree_map)
    assert tree_map == create_tree()


@pytest.mark.parametrize(
    "keys,key,expected",
    [
        ([5, 3, 6, 1, 2, 4, 6, 10, 8], 4, 4),
        ([20, 5, 1, 15, 9, 7, 12, 30, 25, 40], 6, 7),
        ([40, 25, 10, 3, 17, 32, 30, 38, 78, 50, 93], 90, 93),
    ],
)
def test_get_lower_bound(keys, key, expected):
    tree = make_dummy(keys, keys)
    assert get_lower_bound(tree, key) == expected


@pytest.mark.parametrize(
    "keys,key,expected",
    [
        ([5, 3, 6, 1, 2, 4, 6, 10, 8], 4, 5),
        ([20, 5, 1, 15, 9, 7, 12, 30, 25, 40], 1, 5),
        ([40, 25, 10, 3, 17, 32, 30, 38, 78, 50, 93], 15, 17),
    ],
)
def test_get_upper_bound(keys, key, expected):
    tree = make_dummy(keys, keys)
    assert get_upper_bound(tree, key) == expected


@pytest.mark.parametrize(
    "keys,expected",
    [
        ([5, 3, 6, 1, 2, 4, 6, 10, 8], 10),
        ([20, 5, 1, 15, 9, 7, 12, 30, 25, 40], 40),
        ([40, 25, 10, 3, 17, 32, 30, 38, 78, 50, 93], 93),
    ],
)
def test_get_maximum(keys, expected):
    tree = make_dummy(keys, keys)
    assert get_maximum(tree) == expected


@pytest.mark.parametrize(
    "keys,expected",
    [
        ([5, 3, 6, 1, 2, 4, 6, 10, 8], 1),
        ([20, 5, 1, 15, 9, 7, 12, 30, 25, 40], 1),
        ([40, 25, 10, 3, 17, 32, 30, 38, 78, 50, 93], 3),
    ],
)
def test_get_minimum(keys, expected):
    tree = make_dummy(keys, keys)
    assert get_minimum(tree) == expected


@pytest.mark.parametrize("tree_map,left,right,expected,expected_keys_count", [
    (make_dummy([50, 30, 80, 20, 40, 60, 100, 15], [50, 30, 80, 20, 40, 60, 100, 15]), 40, 80, [15, 20, 30, 100], 4),
    (make_dummy([10, 5, 15, 3, 7, 12, 18], [10, 5, 15, 3, 7, 12, 18]), 6, 13, [3, 5, 15, 18], 4),
    (make_dummy([20, 10, 30, 5, 15, 25, 35],  [20, 10, 30, 5, 15, 25, 35]), 36, 40, [5, 10, 15, 20, 25, 30, 35], 7),
    (make_dummy([50, 30, 70, 20, 40, 60, 80], [50, 30, 70, 20, 40, 60, 80]), 10, 50, [60, 70, 80], 3),
    (make_dummy([40, 20, 60, 10, 30, 50, 70], [40, 20, 60, 10, 30, 50, 70]), 50, 80, [10, 20, 30, 40], 4),
    (make_dummy([5, 3, 7, 2, 4, 6, 8], [5, 3, 7, 2, 4, 6, 8]), 4, 4, [2, 3, 5, 6, 7, 8], 6)
])
def test_remove_keys(tree_map: Tree[K, V], left: K, right: K, expected: list[int], expected_keys_count: int) -> None:
    remove_keys(tree_map, left, right)
    result = traverse(tree_map, "inorder")
    assert result == expected and tree_map.size == expected_keys_count


@pytest.mark.parametrize("tree_map,left,right,expected", [
    (make_dummy([50, 30, 80, 20, 40, 60, 100, 15], [50, 30, 80, 20, 40, 60, 100, 15]), 40, 80, [40, 50, 60, 80]),
    (make_dummy([10, 5, 15, 3, 7, 12, 18], [10, 5, 15, 3, 7, 12, 18]), 6, 13, [7, 10, 12]),
    (make_dummy([20, 10, 30, 5, 15, 25, 35],  [20, 10, 30, 5, 15, 25, 35]), 36, 40, []),
    (make_dummy([5, 3, 7, 2, 4, 6, 8], [5, 3, 7, 2, 4, 6, 8]), 4, 4, [4])
])
def test_getAll(tree_map: Tree[K, V], left: K, right: K, expected: list[int]) -> None:
    result = getAll(tree_map, left, right)
    assert result == expected


@pytest.mark.parametrize("tree_map,another,expected", [
    (make_dummy([10, 5, 15], [10, 5, 15]), make_dummy([20, 17, 25], [20, 17, 25]), [5, 10, 15, 17, 20, 25]),
    (make_dummy([10, 5, 15], [10, 5, 15]), make_dummy([15, 12, 18], [15, 12, 18]), [5, 10, 12, 15, 18]),
    (make_dummy([50, 30, 70, 20, 40, 60, 80], [50, 30, 70, 20, 40, 60, 80]), make_dummy([35, 25, 45, 55, 65, 75, 85], [35, 25, 45, 55, 65, 75, 85]), [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]),
    (make_dummy([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]), make_dummy([10, 9, 8, 7, 6], [10, 9, 8, 7, 6]), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    (make_dummy([1], [1]), make_dummy([2], [2]), [1, 2]),
    (make_dummy([50, 25, 75, 10, 30, 60, 90, 5, 15, 28, 35, 55, 65, 85, 95], [50, 25, 75, 10, 30, 60, 90, 5, 15, 28, 35, 55, 65, 85, 95]),
     make_dummy([20, 18, 22], [20, 18, 22]),
     [5, 10, 15, 18, 20, 22, 25, 28, 30, 35, 50, 55, 60, 65, 75, 85, 90, 95]),
    (make_dummy([100, 50, 150, 25, 75, 125, 175], [100, 50, 150, 25, 75, 125, 175]),
     make_dummy([10, 5, 15], [10, 5, 15]),
     [5, 10, 15, 25, 50, 75, 100, 125, 150, 175]),
    (make_dummy([300, 200], [300, 200]),
     make_dummy([100, 50, 150, 25, 75, 125, 175], [100, 50, 150, 25, 75, 125, 175]),
     [25, 50, 75, 100, 125, 150, 175, 200, 300])
])
def test_join(tree_map: Tree[K, V], another: Tree[K, V], expected: list[int]):
    if expected == [1, 2]:
        pass
    join(tree_map, another)
    result = get_all_keys(tree_map)
    assert result == expected


@pytest.mark.parametrize("tree_map,key,expected1,expected2", [
    (make_dummy([20, 10, 30, 5, 15, 25, 35], [20, 10, 30, 5, 15, 25, 35]), 15, [5, 10], [15, 20, 25, 30, 35]),
    (make_dummy([15, 5, 25, 20, 30], [15, 5, 25, 20, 30]), 30, [5, 15, 20, 25], [30]),
    (make_dummy([30, 10, 50, 5, 20, 40, 60], [30, 10, 50, 5, 20, 40, 60]), 15, [5, 10], [20, 30, 40, 50, 60]),
    (make_dummy([50, 30, 70, 20, 40, 60, 80], [50, 30, 70, 20, 40, 60, 80]), 55, [20, 30, 40, 50], [60, 70, 80])
])
def test_split(tree_map: Tree[K, V], key: K, expected1: list[int], expected2: list[int]) -> None:
    tree1, tree2 = split(tree_map, key)
    result1, result2 = traverse(tree1, "inorder"), traverse(tree2, "inorder")
    assert result1 == expected1 and result2 == expected2
