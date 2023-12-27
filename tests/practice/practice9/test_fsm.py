import string
import pytest
from src.practice.practice9.fsm import *


def make_table1() -> FSMachine:
    fsm_table = {
        0: {string.digits: 1},
        1: {"E": 4, string.digits: 1, ".": 2},
        2: {string.digits: 3},
        3: {"E": 4, string.digits: 3},
        4: {"+": 5, "-": 5, string.digits: 6},
        5: {string.digits: 6},
        6: {string.digits: 6},
    }
    return create_fs_machine(fsm_table, 0, [1, 3, 6])


def make_table2() -> FSMachine:
    fsm_table = {
        0: {"a": 1, "b": 1},
        1: {"a": 2, "b": 1},
        2: {"b": 3, "a": 2},
        3: {"b": 4, "a": 2},
        4: {"a": 2, "b": 1},
    }
    return create_fs_machine(fsm_table, 0, [4])


@pytest.mark.parametrize(
    "fsm, start_pos, accepted_pos, expected_len_states",
    [(make_table1(), 0, [4], 7)],
)
def test_create_fsm_machine(fsm, start_pos, accepted_pos, expected_len_states) -> None:
    assert (
        len(fsm.states.keys()) == expected_len_states
        and fsm.start_state_ind == start_pos
    )


@pytest.mark.parametrize(
    "fsm, start_pos, accepted_pos, input_string, expected",
    [
        (make_table1(), 0, [1, 3, 6], "123.33E333", True),
        (make_table1(), 0, [1, 3, 6], "11.1234E-3", True),
        (make_table1(), 0, [1, 3, 6], "123.76E+10", True),
        (make_table1(), 0, [1, 3, 6], "123E+1234", True),
        (make_table1(), 0, [1, 3, 6], ".13E+3", False),
        (make_table1(), 0, [1, 3, 6], "1.23+5435", False),
        (make_table1(), 0, [1, 3, 6], "4.1234E", False),
        (make_table1(), 0, [1, 3, 6], "3.123", True),
        (make_table1(), 0, [1, 3, 6], "4", True),
        (make_table1(), 0, [1, 3, 6], "4.3E3.3", False),
        (make_table2(), 0, [4], "aILOVEPYTHONVERYMUCHabb", False),
        (make_table2(), 0, [4], "PLEASESAVEMEFROMPYTHON", False),
        (make_table2(), 0, [4], "abb", False),
        (make_table2(), 0, [4], "aabb", True),
        (make_table2(), 0, [4], "babb", True),
        (make_table2(), 0, [4], "bbabb", True),
        (make_table2(), 0, [4], "aabbabbabbbbabbabb", True),
    ],
)
def test_validate_string(fsm, start_pos, accepted_pos, input_string, expected) -> None:
    assert validate_string(fsm, input_string) == expected
