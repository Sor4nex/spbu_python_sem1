import io
import warnings

import pytest
from src.test.test3.safe_cell import *


@safe_cell
def func_test_normal(x, y):
    return x / y


@safe_cell
def func_test_other_exceptions(x):
    return x[1]


@safe_cell
def func_test_nest(x, y):
    def foo1(x, y):
        def foo2(x, y):
            return x / y

        return foo2(x, y)

    return foo1(x, y)


@pytest.mark.parametrize(
    "stacktrace,expected",
    [
        (
            """Traceback (most recent call last):
  File "/home/sor4nex/python/spbu/spbu_python_sem1/src/forte.py", line 12, in foo
    5 / 0
    ~~^~~
ZeroDivisionError: division by zero
""",
            ("ZeroDivisionError: division by zero", "foo", "12", "5 / 0"),
        ),
        (
            """Traceback (most recent call last):
  File "/home/sor4nex/python/spbu/spbu_python_sem1/src/forte.py", line 19, in <module>
    func_test_nest(1, 0)
  File "/home/sor4nex/python/spbu/spbu_python_sem1/src/forte.py", line 15, in func_test_nest
    return foo1(x, y)
           ^^^^^^^^^^
  File "/home/sor4nex/python/spbu/spbu_python_sem1/src/forte.py", line 14, in foo1
    return foo2(x, y)
           ^^^^^^^^^^
  File "/home/sor4nex/python/spbu/spbu_python_sem1/src/forte.py", line 13, in foo2
    return x / y
           ~~^~~
ZeroDivisionError: division by zero
""",
            ("ZeroDivisionError: division by zero", "foo2", "13", "return x / y"),
        ),
        (
            """Traceback (most recent call last):
  File "/home/sor4nex/python/spbu/spbu_python_sem1/src/forte.py", line 22, in <module>
    func_test_other_exceptions([5])
  File "/home/sor4nex/python/spbu/spbu_python_sem1/src/forte.py", line 18, in func_test_other_exceptions
    return x[1]
           ~^^^
IndexError: list index out of range
""",
            (
                "IndexError: list index out of range",
                "func_test_other_exceptions",
                "18",
                "return x[1]",
            ),
        ),
    ],
)
def test_parse_exception_stacktrace(stacktrace: str, expected) -> None:
    result = parse_exception_stacktrace(stacktrace)
    assert result == expected


@pytest.mark.parametrize(
    "stacktrace,expected",
    [
        (
            ("ZeroDivisionError: division by zero", "foo", "12", "5 / 0"),
            """error occurred during the execution of the program.
error: ZeroDivisionError: division by zero
function name: foo
line number: 12
line: 5 / 0
""",
        ),
        (
            ("ZeroDivisionError: division by zero", "foo2", "13", "return x / y"),
            """error occurred during the execution of the program.
error: ZeroDivisionError: division by zero
function name: foo2
line number: 13
line: return x / y
""",
        ),
        (
            (
                "IndexError: list index out of range",
                "func_test_other_exceptions",
                "18",
                "return x[1]",
            ),
            """error occurred during the execution of the program.
error: IndexError: list index out of range
function name: func_test_other_exceptions
line number: 18
line: return x[1]
""",
        ),
    ],
)
def test_make_message(stacktrace, expected) -> None:
    result = make_warning_message(stacktrace)
    assert result == expected


@pytest.mark.parametrize(
    "function,args,expected",
    [
        (func_test_normal, [10, 5], "2.0\n"),
        (func_test_other_exceptions, [[1, 2]], "2\n"),
        (func_test_other_exceptions, [[1]], "None\n"),
        (func_test_nest, [3, 3], "1.0\n"),
    ],
)
def test_safe_cell(monkeypatch, function, args, expected) -> None:
    fake_output = io.StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    print(function(*args))
    result = fake_output.getvalue()
    assert result == expected


@pytest.mark.parametrize(
    "function,args,expected",
    [
        (
            func_test_normal,
            [1, 0],
            WARNING_MESSAGE.format(
                "ZeroDivisionError: division by zero",
                "func_test_normal",
                "10",
                "return x / y",
            ),
        ),
        (
            func_test_other_exceptions,
            [[3]],
            WARNING_MESSAGE.format(
                "IndexError: list index out of range",
                "func_test_other_exceptions",
                "15",
                "return x[1]",
            ),
        ),
        (
            func_test_other_exceptions,
            [3],
            WARNING_MESSAGE.format(
                "TypeError: 'int' object is not subscriptable",
                "func_test_other_exceptions",
                "15",
                "return x[1]",
            ),
        ),
        (
            func_test_nest,
            [3, 0],
            WARNING_MESSAGE.format(
                "ZeroDivisionError: division by zero", "foo2", "22", "return x / y"
            ),
        ),
        (
            func_test_nest,
            [3],
            WARNING_MESSAGE.format(
                "TypeError: func_test_nest() missing 1 required positional argument: 'y'",
                "substitution",
                "40",
                "result = input_function(*args, **kwargs)",
            ),
        ),
    ],
)
def test_safe_cell_exception_cases(function, args, expected) -> None:
    with warnings.catch_warnings(record=True) as test_warning:
        warnings.simplefilter("always")
        function(*args)
        assert str(test_warning[-1].message) == expected
