import pytest
from src.test.test2.fibonacci import *
from io import StringIO


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("11", True),
        ("81723", True),
        ("114.3", False),
        ("", False),
        (" ", False),
        ("01", False),
        ("0", True),
    ],
)
def test_is_int(input_str: str, expected: bool) -> None:
    assert is_int(input_str) == expected


@pytest.mark.parametrize(
    "num_of_fib,expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (18, 2584),
        (22, 17711),
        (90, 2880067194370816120),
    ],
)
def test_count_n_fibonacci(num_of_fib: int, expected: int) -> None:
    result = count_n_fibonacci(num_of_fib)
    assert result == expected


@pytest.mark.parametrize(
    "user_input,expected",
    [
        ("0", ANSWER.format("0", "0")),
        ("1", ANSWER.format("1", "1")),
        ("2", ANSWER.format("2", "1")),
        ("3", ANSWER.format("3", "2")),
        ("18", ANSWER.format("18", "2584")),
        ("22", ANSWER.format("22", "17711")),
        ("90", ANSWER.format("90", "2880067194370816120")),
        ("EgorSergeevichDontKickMe", ERROR_MESSAGE),
        (" ", ERROR_MESSAGE),
        ("-1", ERROR_MESSAGE),
        ("91", ERROR_MESSAGE),
    ],
)
def test_main(monkeypatch, user_input, expected) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    assert output == expected + "\n"
