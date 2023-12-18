from io import StringIO

import pytest
from src.practice.practice9.main_fsm import *


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
        ("aILOVEPYTHONVERYMUCHabb", RESULT_AB_FSM),
        ("PLEASESAVEMEFROMPYTHON", RESULT_NOTHING),
        ("abb", RESULT_NOTHING),
        ("aabb", RESULT_AB_FSM),
        ("babb", RESULT_AB_FSM),
        ("bbabb", RESULT_AB_FSM),
        ("aabbabbabbbbabccbabb", RESULT_AB_FSM),
    ],
)
def test_main(monkeypatch, user_input, expected) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    assert output == expected + "\n"
