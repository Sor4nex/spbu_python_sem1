import pytest
from src.homeworks.practice4.utf_16 import *
from io import StringIO


@pytest.mark.parametrize(
    "bin_str,expected",
    [
        ("12345678", "12345678"),
        ("0000000011111111", "00000000 11111111"),
        ("00000000111111110000000011111111", "00000000 11111111 00000000 11111111"),
    ],
)
def test_divide_by_octets(bin_str: str, expected: str) -> None:
    result = divide_by_octets_bin(bin_str)
    assert result == expected


@pytest.mark.parametrize(
    "input_char,expected",
    [("H", "U+0048"), ("h", "U+0068"), ("𮗫", "U+2E5EB")],
)
def test_get_char_hex_unicode(input_char: str, expected: str) -> None:
    result = get_char_hex_unicode(input_char)
    assert result == expected


@pytest.mark.parametrize(
    "input_char,expected",
    [
        ("H", "0000000001001000"),
        ("h", "0000000001101000"),
        ("𮗫", "11011000011110011101110111101011"),
    ],
)
def test_get_char_binary_unicode(input_char: str, expected: str) -> None:
    result = get_char_binary_unicode(input_char)
    assert result == expected


@pytest.mark.parametrize(
    "user_input,expected",
    [
        (
            "Hello world!",
            "H:\tU+0048\t00000000 01001000\ne:\tU+0065\t00000000 01100101\nl:\tU+006C\t00000000 01101100\nl:\tU+006C\t00000000 01101100\no:\tU+006F\t00000000 01101111\n :\tU+0020\t00000000 00100000\nw:\tU+0077\t00000000 01110111\no:\tU+006F\t00000000 01101111\nr:\tU+0072\t00000000 01110010\nl:\tU+006C\t00000000 01101100\nd:\tU+0064\t00000000 01100100\n!:\tU+0021\t00000000 00100001\n",
        ),
        (
            "𓐥𓈴Օ",
            "𓐥:\tU+13425\t11011000 00001101 11011100 00100101\n𓈴:\tU+13234\t11011000 00001100 11011110 00110100\nՕ:\tU+0555\t00000101 01010101\n",
        ),
        (" ", " :\tU+0020\t00000000 00100000\n"),
    ],
)
def test_main(monkeypatch, user_input: str, expected: str) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    expected_output = OUTPUT_INTRO + "\n" + expected
    assert output == expected_output


def test_main_exception_case(monkeypatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "")
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    assert output == ZERO_LEN_ERROR + "\n"
