from io import StringIO

import pytest
from src.homeworks.practice6.streets import *


def test_mode_static() -> None:
    mode_static("streets_logs.txt", "my_results.txt")
    actual_results = open("streets_results.txt", "r", encoding="utf-8").read()
    my_results = open("my_results.txt", "r", encoding="utf-8").read()
    assert actual_results == my_results


@pytest.mark.parametrize("user_input,expected", [
    (["1", "EXIT"], INTERACTIVE_MODE_REMINDER + "\n"),
    (["1", "Ilovepython", "EXIT"], INTERACTIVE_MODE_REMINDER + "\n" + COMMAND_EXISTENCE_ERROR + "\n"),
    (["1", "CREATE ONLY THREE ARGS", "EXIT"], INTERACTIVE_MODE_REMINDER + "\n" + ARGUMENT_COUNT_ERROR + "\n")
])
def test_main(monkeypatch, user_input, expected) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input.pop(0))
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    assert output == expected
