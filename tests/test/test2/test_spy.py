import pytest
from src.test.test2.spy import *


@spy
def foo(a, b, **kwargs):
    return a, b


@spy
def foo2():
    return True


foo3 = lambda x: x


@spy
def foo4(x, **kwargs):
    return x


def test_print_usage_statistic() -> None:
    arguments = [("a", "b"), ("b", 4), ("b", 4), ("b", 4), ("b", 4)]
    use_count = 5
    for i in range(use_count):
        foo(*arguments[i])
    result = list(print_usage_statistic(foo))
    assert len(result) == use_count and all(
        result[i][1]["positional arguments"] == arguments[i] for i in range(use_count)
    )


def test_print_usage2() -> None:
    for _ in range(54):
        foo2()
    result = list(print_usage_statistic(foo2))
    assert len(result) == 54


def test_print_usage3() -> None:
    foo4("a", imlesha=True)
    result = list(print_usage_statistic(foo4))
    assert (
        len(result) == 1
        and result[0][1]["positional arguments"] == ("a",)
        and result[0][1]["imlesha"] == True
    )


def test_print_usage_exception() -> None:
    for _ in range(3):
        foo3("aaa")
    with pytest.raises(AttributeError):
        list(print_usage_statistic(foo3))
