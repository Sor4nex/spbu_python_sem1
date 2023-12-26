from io import StringIO

import pytest
from src.practice.practice9.main_fsm import *


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("123.3E12345", True),
        ("123.23E-11111", True),
        ("123.23E+11111", True),
        ("011E+4444", True),
        (".01E+09942", False),
        ("1.123+11111", False),
        ("1.123E", False),
        ("123.123", True),
        ("321", True),
        ("1.2E2.1", False),
    ],
)
def test_validate_string_float(input_string, expected) -> None:
    fsm = maks_fsm_float()
    assert validate_string_float(fsm, input_string) == expected


@pytest.mark.parametrize(
    "user_input, expected",
    [
        ("123.3E12345", RESULT_FLOAT_FSM),
        ("123.23E-11111", RESULT_FLOAT_FSM),
        ("123.23E+11111", RESULT_FLOAT_FSM),
        ("011E+4444", RESULT_FLOAT_FSM),
        (".01E+09942", RESULT_NOTHING),
        ("1.123+11111", RESULT_NOTHING),
        ("1.123E", RESULT_NOTHING),
        ("123.123", RESULT_FLOAT_FSM),
        ("321", RESULT_FLOAT_FSM),
        ("1.2E2.1", RESULT_NOTHING),
    ],
)
def test_main(monkeypatch, user_input, expected) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    assert output == expected + "\n"
