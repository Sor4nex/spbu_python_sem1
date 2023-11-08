import pytest
from io import StringIO
from src.homeworks.practice4.dna_compress import *


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("aabbbb", False),
        ("qqwwerwe", False),
        ("ilikebananas", False),
        ("a3bbbb", True),
        ("aaa bbbbc", True),
        ("mm,deoold", True),
        ("(aabaa)", True),
        (" ", True),
        ("/", True),
    ],
)
def test_is_input_to_compress_incorrect(input_str: str, expected: bool) -> None:
    result = is_input_to_compress_incorrect(input_str)
    assert result == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("a3b4", ["a3", "b4"]),
        ("a100b1011", ["a100", "b1011"]),
        ("a333b555", ["a333", "b555"]),
        ("p1i8p19n9", ["p1", "i8", "p19", "n9"]),
    ],
)
def test_convert_compressed_str_to_list(input_str: str, expected: list[str]) -> None:
    result = convert_compressed_str_to_list(input_str)
    assert result == expected


@pytest.mark.parametrize(
    "input_str",
    [
        "",
        "a01b1",
        "a0b1",
        "a2a33b9",
        "a3b4c",
        "aa33b4",
        "ab4c2",
        "a3,b4",
        "v9/p9",
        "a2 b2",
    ],
)
def test_convert_compressed_str_to_list_exception_cases(input_str: str) -> None:
    with pytest.raises(ValueError):
        convert_compressed_str_to_list(input_str)


@pytest.mark.parametrize(
    "input_dna,expected",
    [
        (list("aaabbbb"), "a3b4"),
        (list("acbbv"), "a1c1b2v1"),
        (list("aaabbcaa"), "a3b2c1a2"),
    ],
)
def test_compress_dna(input_dna: list[str], expected: str) -> None:
    result = "".join(compress_dna(input_dna))
    assert result == expected


@pytest.mark.parametrize(
    "input_dna,expected",
    [
        (["a3", "b4"], "aaabbbb"),
        (["a1", "c1", "b2", "v1"], "acbbv"),
        (["a4", "b2", "c1", "a2"], "aaaabbcaa"),
    ],
)
def test_decompress_dna(input_dna: list[str], expected: str) -> None:
    result = "".join(decompress_dna(input_dna))
    assert result == expected


@pytest.mark.parametrize(
    "user_input,expected",
    [
        (["3", ""], ERROR_COMMAND_INPUT),
        (["abc", ""], ERROR_COMMAND_INPUT),
        (["", ""], ERROR_COMMAND_INPUT),
        (["1", "aaaabbcaa"], SUCCESSFUL_RESULT + " a4b2c1a2"),
        (["1", "abc"], SUCCESSFUL_RESULT + " a1b1c1"),
        (["1", " "], ERROR_COMPRESS_INPUT),
        (["1", ""], ERROR_COMPRESS_INPUT),
        (["1", ","], ERROR_COMPRESS_INPUT),
        (["1", "aab/bbaa"], ERROR_COMPRESS_INPUT),
        (["2", "a3b4c1a2"], SUCCESSFUL_RESULT + " aaabbbbcaa"),
        (["2", "s1h1n1i3s1h1n1a3"], SUCCESSFUL_RESULT + " shniiishnaaa"),
        (["2", ""], ERROR_DECOMPRESS_INPUT),
        (["2", " "], ERROR_DECOMPRESS_INPUT),
        (["2", "a3,b4"], ERROR_DECOMPRESS_INPUT),
        (["2", "a3 b4"], ERROR_DECOMPRESS_INPUT),
        (["2", "a01b1"], ERROR_DECOMPRESS_INPUT),
        (["2", "a2a33b9"], ERROR_DECOMPRESS_INPUT),
        (["2", "a0b1"], ERROR_DECOMPRESS_INPUT),
        (["2", "a3b4c"], ERROR_DECOMPRESS_INPUT),
        (["2", "ab4c2"], ERROR_DECOMPRESS_INPUT),
        (["2", "v9/p9"], ERROR_DECOMPRESS_INPUT),
    ],
)
def test_main(monkeypatch, user_input: list, expected: str):
    monkeypatch.setattr("builtins.input", lambda _: user_input.pop(0))
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    assert output == INTRODUCTION + "\n" + expected + "\n"
