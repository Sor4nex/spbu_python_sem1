import pytest
from src.homeworks.practice6.shopping import *


def make_dummy(list_sizes: list) -> avl.Tree:
    size_tree = avl.create_tree()
    for size in list_sizes:
        avl.put_value_by_key(size_tree, size, 1)
    return size_tree


@pytest.mark.parametrize(
    "avl_tree,size,count,expected",
    [
        (make_dummy([1, 2, 3, 4, 5]), 6, 10, 10),
        (make_dummy([1, 2, 3, 4, 5]), 5, 10, 11),
        (make_dummy([1, 2, 3, 4, 5]), 99, 1, 1),
    ],
)
def test_add_size(avl_tree: avl.Tree, size: int, count: int, expected: int) -> None:
    add_size(avl_tree, size, count)
    assert avl.get_value_by_key(avl_tree, size) == expected


@pytest.mark.parametrize(
    "avl_tree,size,expected",
    [(make_dummy([1, 2, 3, 4, 5]), 5, 1), (make_dummy([1, 2, 3, 4, 5]), 6, 0)],
)
def test_get_count_by_size(avl_tree: avl.Tree, size: int, expected: int) -> None:
    pass


@pytest.mark.parametrize(
    "avl_tree,size,expected",
    [
        (make_dummy([1, 2, 3, 4, 5]), 5, 5),
        (make_dummy([100, 200, 300]), 201, 300),
        (make_dummy([100, 200, 300]), 299, 300),
        (make_dummy([100, 200, 300]), 301, None),
    ],
)
def test_select_thing_by_size(avl_tree: avl.Tree, size: int, expected: int) -> None:
    result = select_thing_by_size(avl_tree, size)
    assert result == expected
