import pytest
from src.practice.practice8.hash import *


def dummy_hashmap(input_list: list[tuple[K, V]]) -> HashMap[K, V]:
    hash_map = create_hash_table()
    for entry in input_list:
        put_value_by_key(hash_map, entry[0], entry[1])
    return hash_map


@pytest.mark.parametrize(
    "hash_table,key,expected",
    [
        (dummy_hashmap([(1, "a"), (2, "b"), (3, "c")]), 3, (hash(3) % 100, (3, "c"))),
        (dummy_hashmap([(1, "a"), (2, "b"), (3, "c")]), 4, (hash(4) % 100, None)),
        (
            dummy_hashmap([("a", 1), ("b", 2), ("c", 3)]),
            "b",
            (hash("b") % 100, ("b", 2)),
        ),
        (
            dummy_hashmap([((1, 2, 3), "a"), ((2, 3, 4), "b")]),
            (2, 3, 4),
            (hash((2, 3, 4)) % 100, ((2, 3, 4), "b")),
        ),
        (
            dummy_hashmap([((1, 2, 3), "a"), ((2, 3, 4), "b")]),
            (2, 3, 4, 5),
            (hash((2, 3, 4, 5)) % 100, None),
        ),
    ],
)
def test_get_entry_by_key(
    hash_table: HashMap[K, V], key: K, expected: tuple[int, Optional[tuple[K, V]]]
) -> None:
    result = get_entry_from_bucket(hash_table, key)[::2]
    if result[1] is not None:
        result = (result[0], (result[1].key, result[1].value))
    assert result == expected


@pytest.mark.parametrize(
    "hash_table,expected",
    [
        (
            dummy_hashmap(
                [(1, "a"), (102, ("1", 2, True)), (2, ["a", "b", "c"]), (101, "d")]
            ),
            [(1, "a"), (101, "d"), (102, ("1", 2, True)), (2, ["a", "b", "c"])],
        ),
        (
            dummy_hashmap([((1, 2, 3), "a"), ((4, 5, 6, 7), "b")]),
            [((1, 2, 3), "a"), ((4, 5, 6, 7), "b")],
        ),
        (dummy_hashmap([]), []),
    ],
)
def test_get_items(hash_table: HashMap[K, V], expected: list[tuple[K, V]]) -> None:
    result = list(get_items(hash_table))
    assert result == expected


@pytest.mark.parametrize(
    "hash_table,key,expected",
    [
        (dummy_hashmap([(1, "a"), (2, "b"), (3, "c")]), 3, True),
        (dummy_hashmap([(1, "a"), (2, "b"), (3, "c")]), 4, False),
        (dummy_hashmap([("a", 1), ("b", 2), ("c", 3)]), "b", True),
        (dummy_hashmap([((1, 2, 3), "a"), ((2, 3, 4), "b")]), (2, 3, 4), True),
        (dummy_hashmap([((1, 2, 3), "a"), ((2, 3, 4), "b")]), (2, 3, 4, 5), False),
        (dummy_hashmap([]), "hello?", False),
    ],
)
def test_has_key(hash_table: HashMap[K, V], key: K, expected: bool) -> None:
    result = has_key(hash_table, key)
    assert result == expected


@pytest.mark.parametrize(
    "hash_table,key,expected",
    [
        (dummy_hashmap([(1, "a"), (2, "b"), (3, "c")]), 3, "c"),
        (dummy_hashmap([("a", 1), ("b", 2), ("c", 3)]), "b", 2),
        (dummy_hashmap([((1, 2, 3), "a"), ((2, 3, 4), "b")]), (2, 3, 4), "b"),
    ],
)
def test_get_value_by_key(hash_table: HashMap[K, V], key: K, expected: V) -> None:
    result = get_value_by_key(hash_table, key)
    assert result == expected


@pytest.mark.parametrize(
    "hash_table,key",
    [
        (dummy_hashmap([(1, "a"), (2, "b"), (3, "c")]), 4),
        (dummy_hashmap([((1, 2, 3), "a"), ((2, 3, 4), "b")]), (2, 3, 4, 5)),
        (dummy_hashmap([]), "hello???"),
    ],
)
def test_get_value_by_key_expception_case(hash_table: HashMap[K, V], key: K) -> None:
    with pytest.raises(ValueError):
        get_value_by_key(hash_table, key)


@pytest.mark.parametrize(
    "hash_table,key,value,expected",
    [
        (dummy_hashmap([]), 1, "a", [(1, "a")]),
        (
            dummy_hashmap([(1, "A"), (2, "b")]),
            5,
            "aaaa",
            [(1, "A"), (2, "b"), (5, "aaaa")],
        ),
        (dummy_hashmap([(1, "a")]), 1, "b", [(1, "b")]),
        (dummy_hashmap([(1, "a"), (3, "b")]), 2, "c", [(1, "a"), (3, "b"), (2, "c")]),
        (
            dummy_hashmap([((1, 2, 3), "a")]),
            (4, 5, 6, 7),
            "b",
            [((1, 2, 3), "a"), ((4, 5, 6, 7), "b")],
        ),
    ],
)
def test_put_by_key(
    hash_table: HashMap[K, V], key: K, value: V, expected: list[tuple[K, V]]
) -> None:
    put_value_by_key(hash_table, key, value)
    result = list(get_items(hash_table))
    assert result == expected


@pytest.mark.parametrize(
    "hash_table,key,expected,removed",
    [
        (dummy_hashmap([(1, "a")]), 1, [], "a"),
        (dummy_hashmap([(1, "A"), (2, "b")]), 2, [(1, "A")], "b"),
        (dummy_hashmap([(1, "a"), (3, "b"), (2, "c")]), 2, [(1, "a"), (3, "b")], "c"),
        (
            dummy_hashmap([((1, 2, 3), "a"), ((4, 5, 6, 7), "b")]),
            (4, 5, 6, 7),
            [((1, 2, 3), "a")],
            "b",
        ),
    ],
)
def test_remove_by_key(
    hash_table: HashMap[K, V], key: K, expected: list[tuple[K, V]], removed: V
) -> None:
    removed_actual = remove_by_key(hash_table, key)
    result = list(get_items(hash_table))
    assert result == expected and removed_actual == removed


@pytest.mark.parametrize(
    "hash_table,key",
    [
        (dummy_hashmap([]), 1),
        (dummy_hashmap([(1, "a")]), 2),
        (dummy_hashmap([((1, 2, 3), "a"), ((4, 5, 6, 7), "b")]), (4, 5, 6)),
    ],
)
def test_remove_by_key_expection_case(hash_table: HashMap[K, V], key: K) -> None:
    with pytest.raises(ValueError):
        remove_by_key(hash_table, key)


def test_resize_hash_table() -> None:
    table1 = create_hash_table()
    table2 = create_hash_table()
    for i in range(79):
        put_value_by_key(table1, i, str(i))
        put_value_by_key(table2, i, str(i))
    put_value_by_key(table1, 11111111, "Hello, Tim")
    put_value_by_key(table2, 11111111, "Hello, Tim")
    put_value_by_key(table2, 79, str(79))
    assert (
        len(table1.buckets) != len(table2.buckets)
        and get_entry_from_bucket(table1, 11111111)[0]
        != get_entry_from_bucket(table2, 11111111)[0]
    )
