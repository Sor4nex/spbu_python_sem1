from io import StringIO

import pytest
from src.test.test3.sprites import *


def check_vertical(matrix: list[list[int]], size: int) -> bool:
    half_size = int(size / 2)
    for i in range(size):
        if size % 2 == 0:
            if matrix[i][:half_size] != matrix[i][half_size:][::-1]:
                return False
        else:
            if matrix[i][:half_size] != matrix[i][half_size + 1 :][::-1]:
                return False
    return True


def check_horizontal(matrix: list[list[int]], size: int) -> bool:
    for i in range(size):
        for j in range(size):
            if matrix[j][i] != matrix[-j - 1][i]:
                return False
    return True


def check_both(matrix: list[list[int]], size: int) -> bool:
    half_size = int(size / 2)
    for i in range(half_size):
        if size % 2 == 0:
            if matrix[i][:half_size] != matrix[i][half_size:][::-1]:
                return False
        else:
            if matrix[i][:half_size] != matrix[i][half_size + 1 :][::-1]:
                return False
    for i in range(half_size):
        for j in range(half_size):
            if matrix[j][i] != matrix[-j - 1][i]:
                return False
    return True


def test_generate_vertical_symmetric() -> None:
    all_results = []
    for _ in range(100):
        size = random.randint(2, 30)
        matrix = generate_vertical_symmetric(size)
        all_results.append(check_vertical(matrix, size))
    assert all(all_results)


def test_generate_horizontal_symmetric() -> None:
    all_results = []
    for _ in range(100):
        size = random.randint(2, 30)
        matrix = generate_horizontal_symmetric(size)
        all_results.append(check_horizontal(matrix, size))
    assert all(all_results)


def test_generate_both_symmetric() -> None:
    all_results = []
    for _ in range(100):
        size = random.randint(2, 30)
        matrix = generate_both_symmetric(size)
        all_results.append(check_both(matrix, size))
    assert all(all_results)


@pytest.mark.parametrize(
    "sprite,expected",
    [
        ([[1, 0, 1], [0, 1, 0], [1, 0, 1]], ["█░█\n", "░█░\n", "█░█\n\n"]),
        ([[0, 0], [1, 1]], ["░░\n", "██\n\n"]),
        (
            [
                [1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
            ],
            ["█░░░░\n", "░█░░░\n", "░░█░░\n", "░░░█░\n", "░░░░█\n\n"],
        ),
    ],
)
def test_print_sprite(
    monkeypatch, sprite: list[list[int]], expected: list[str]
) -> None:
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    print_sprite(sprite)
    output = fake_output.getvalue()
    assert output == "".join(expected)


@pytest.mark.parametrize(
    "user_input,expected,expected_int",
    [
        (["3"], "", 3),
        (["900"], "", 900),
        (["1234"], "", 1234),
        (["-123", "1"], ERROR_INPUT_SIZE + "\n", 1),
        (["2.23", "1"], ERROR_INPUT_SIZE + "\n", 1),
        (
            ["aisdf", "-234.3", "0234"],
            ERROR_INPUT_SIZE + "\n" + ERROR_INPUT_SIZE + "\n",
            234,
        ),
    ],
)
def test_get_size_from_user(monkeypatch, user_input, expected, expected_int) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input.pop(0))
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    x = get_size_from_user()
    output = fake_output.getvalue()
    assert output == expected and x == expected_int


@pytest.mark.parametrize(
    "user_input,expected_len",
    [
        (["3", "enter", "exit"], 10),
        (["e", "3", "enter", "exit"], 11),
        (["3", "enter", "enter", "exit"], 14),
        (["-12", "12.3", "12", "exit"], 17),
    ],
)
def test_main(monkeypatch, user_input, expected_len) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input.pop(0))
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    assert len(output.split("\n")) == expected_len
