from io import StringIO
import pytest
from src.practice.practice6.function_solver import *


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("123", True),
        ("+123.4", True),
        ("-123.4", True),
        ("33333e-7", True),
        ("-000000.1 ", True),
        ("nan", True),
        ("inf", True),
        ("1,23", False),
        ("abc", False),
        ("--34", False),
        ("++34", False),
        ("3..4", False),
        ("d", False),
    ],
)
def test_is_float(input_str: str, expected: bool) -> None:
    result = is_float_number(input_str)
    assert result == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("123 123 123", True),
        ("+123.4 -123.4 25", True),
        ("-000000.1 21 +33333e-7", True),
        ("-2e-3 45 45", True),
        ("nan inf nan", True),
        ("1,23 1 1", False),
        ("abc 67", False),
        ("--34 34 ++34", False),
        ("3..4 5 5", False),
        ("d", False),
        ("  3    4  5", False),
        ("1 2 3 4", False),
        ("1 2", False),
        ("1", False),
    ],
)
def test_parse_user_input(test_input: str, expected: bool) -> None:
    result = parse_user_input(test_input)
    assert result == expected


@pytest.mark.parametrize(
    "second_argument,third_argument,expected",
    [(1, 2, -2), (4, -16, 4), (5, 0, 0)],
)
def test_solve_function_linear(
    second_argument: float, third_argument: float, expected
) -> None:
    result = solve_linear_function(second_argument, third_argument)
    assert result == expected


@pytest.mark.parametrize(
    "first_argument,second_argument,third_argument,expected",
    [
        (1, -2, 1, (1,)),
        (1, -3, 2, (1, 2)),
        (2, -1, -15, (-2.5, 3)),
        (1, 0, 0, (0,)),
        (4, 0, 16, (2,)),
    ],
)
def solve_function_quadratic_valid_input(
    first_argument: float, second_argument: float, third_argument: float, expected
) -> None:
    result = solve_quadratic_function(first_argument, second_argument, third_argument)
    assert result == expected or result == expected[::-1]


@pytest.mark.parametrize(
    "first_argument,second_argument,third_argument", [(1, 2, 3), (55, 1, 99)]
)
def test_solve_quadratic_function_exception_cases(
    first_argument: float, second_argument: float, third_argument: float
) -> None:
    with pytest.raises(ArithmeticError):
        solve_quadratic_function(first_argument, second_argument, third_argument)


@pytest.mark.parametrize(
    "first_argument,second_argument,third_argument,expected",
    [
        (0, 1, 2, (-2,)),
        (0, 4, -16, (4,)),
        (0, 5, 0, (0,)),
        (1, -2, 1, (1,)),
        (1, -3, 2, (1, 2)),
        (2, -1, -15, (-2.5, 3)),
        (1, 0, 0, (0,)),
        (4, 0, 16, (2,)),
    ],
)
def test_solve_function_valid_cases(
    first_argument: float, second_argument: float, third_argument: float, expected
) -> None:
    result = solve_function(first_argument, second_argument, third_argument)
    assert result == expected or result == expected[::-1]


@pytest.mark.parametrize(
    "first_argument,second_argument,third_argument", [(0, 0, 69), (0, 0, 0)]
)
def test_solve_function_valid_cases(
    first_argument: float, second_argument: float, third_argument: float
) -> None:
    with pytest.raises(ValueError):
        solve_function(first_argument, second_argument, third_argument)


@pytest.mark.parametrize(
    "user_input,expected",
    [
        ("2 -1 -15", "Ответ: 3.0 -2.5"),
        ("+4 -5 +1", "Ответ: 1.0 0.25"),
        ("1 -2 1", "Ответ: 1.0"),
        ("0 1 2", "Ответ: -2.0"),
        ("0 0 1", "Ответ: корня данного уравнения не существует"),
        ("0 0 0", "Ответ: корень - любое вещественное число"),
        ("1 2 3", "Ответ: дискриминант уравнения меньше 0, решений нет"),
        ("abd 3 4", BAD_INPUT),
        ("1 2 3 4", BAD_INPUT),
        (" abd     ", BAD_INPUT),
        ("3 inf 3", BAD_INPUT),
        ("nan 2 3", BAD_INPUT),
        ("--2 3 3", BAD_INPUT),
        ("3,3 4 5", BAD_INPUT),
        ("3.56.3 4 3", BAD_INPUT),
        ("2 3", BAD_INPUT),
    ],
)
def test_main(monkeypatch, user_input, expected) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    expected_output = GREET_USER + "\n" + INFO_STRING + "\n" + expected + "\n"
    assert output == expected_output
