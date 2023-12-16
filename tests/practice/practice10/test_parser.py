from io import StringIO

import pytest
from src.practice.practice10.parser_main import *


@pytest.mark.parametrize(
    "user_input, expected",
    [
        (
            "5 + 3 * 8",
            [
                (0, "START"),
                (4, "T"),
                (8, "TOKEN"),
                (12, "id(5)"),
                (8, "PROD"),
                (12, "eps"),
                (4, "SUM"),
                (8, "+"),
                (8, "T"),
                (12, "TOKEN"),
                (16, "id(3)"),
                (12, "PROD"),
                (16, "*"),
                (16, "TOKEN"),
                (20, "id(8)"),
                (16, "PROD"),
                (20, "eps"),
                (8, "SUM"),
                (12, "eps"),
            ],
        ),
        (
            "5",
            [
                (0, "START"),
                (4, "T"),
                (8, "TOKEN"),
                (12, "id(5)"),
                (8, "PROD"),
                (12, "eps"),
                (4, "SUM"),
                (8, "eps"),
            ],
        ),
        (
            "12345",
            [
                (0, "START"),
                (4, "T"),
                (8, "TOKEN"),
                (12, "id(12345)"),
                (8, "PROD"),
                (12, "eps"),
                (4, "SUM"),
                (8, "eps"),
            ],
        ),
        (
            "( 5 + 3 )",
            [
                (0, "START"),
                (4, "T"),
                (8, "TOKEN"),
                (12, "("),
                (12, "START"),
                (16, "T"),
                (20, "TOKEN"),
                (24, "id(5)"),
                (20, "PROD"),
                (24, "eps"),
                (16, "SUM"),
                (20, "+"),
                (20, "T"),
                (24, "TOKEN"),
                (28, "id(3)"),
                (24, "PROD"),
                (28, "eps"),
                (20, "SUM"),
                (24, "eps"),
                (12, ")"),
                (8, "PROD"),
                (12, "eps"),
                (4, "SUM"),
                (8, "eps"),
            ],
        ),
    ],
)
def test_main(monkeypatch, user_input, expected) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    expected_output = ""
    for elem in expected:
        expected_output += "." * elem[0] + " " + elem[1] + "\n"
    assert output == RESULT + "\n" + expected_output


@pytest.mark.parametrize(
    "user_input", ["3 +", "3 *", "( ) ( )", "(3)", "", "3 + 3 + 3 + 3 + 3 + 3 + 3 +"]
)
def test_main_expections(monkeypatch, user_input) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    assert output == ERROR + "\n"
