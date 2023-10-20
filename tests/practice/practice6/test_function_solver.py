from io import StringIO
import pytest
from src.practice.practice6.function_solver import *


test_main_parameters = [
    ("2 -1 -15", "Ответ: 3.0 -2.5"),
    ("1 -2 1", "Ответ: 1.0"),
    ("0 1 2", "Ответ: -2.0"),
    ("0 0 1", "Ответ: корня данного уравнения не существует"),
    ("0 0 0", "Ответ: корень - любое вещественное число"),
    ("1 2 3", "Ответ: дискриминант уравнения меньше 0, решений нет"),
    ("abd     ", f"Ответ: {BAD_INPUT}"),
    ("2 3", f"Ответ: {BAD_INPUT}"),
]
test_float_number_parameters = [
    ("123", True),
    ("123.4", True),
    ("-123", True),
    ("-123.4", True),
    ("abc", False),
]
test_linear_parameters = [
    (1, 2, (-2,)),
    (0, 3, ("корня данного уравнения не существует",)),
    (0, 0, ("корень - любое вещественное число",)),
]
test_quadratic_parametrs = [
    (1, -2, 1, (1, 1)),
    (1, 2, 3, ("дискриминант уравнения меньше 0, решений нет",)),
    (1, -3, 2, (1, 2)),
    (2, -1, -15, (-2.5, 3)),
]


@pytest.mark.parametrize("test_input,expected", test_float_number_parameters)
def test_is_float_number(test_input: str, expected: bool) -> None:
    result = is_float_number(test_input)
    assert result == expected


@pytest.mark.parametrize(
    "first_argument,second_argument,expected", test_linear_parameters
)
def test_solve_linear_function(
    first_argument: float, second_argument: float, expected
) -> None:
    result = solve_linear_function(first_argument, second_argument)
    assert result == expected


@pytest.mark.parametrize(
    "first_argument,second_argument,third_argument,expected", test_quadratic_parametrs
)
def solve_quadratic_function(
    first_argument: float, second_argument: float, third_argument: float, expected
) -> None:
    result = solve_quadratic_function(first_argument, second_argument, third_argument)
    assert result == expected


@pytest.mark.parametrize("user_input,expected", test_main_parameters)
def test_main(monkeypatch, user_input, expected) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue().strip().split("\n")
    for single_string in output:
        if single_string not in [GREET_USER, INFO_STRING, INPUT_INVITATION, BAD_INPUT]:
            assert single_string == expected
