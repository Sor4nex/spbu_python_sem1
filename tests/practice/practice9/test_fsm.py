import pytest
from src.practice.practice9.fsm import *


test_table1 = {
    0: {"d": 1},
    1: {"E": 4, "d": 1, ".": 2},
    2: {"d": 3},
    3: {"E": 4, "d": 3},
    4: {"+": 5, "-": 5, "d": 6},
    5: {"d": 6},
    6: {"d": 6},
}
test_table2 = {
    0: {"a": 1, "b": 1},
    1: {"a": 2, "*": 1},
    2: {"b": 3, "*": 1},
    3: {"b": 4, "*": 1},
    4: {"*": 1},
}


@pytest.mark.parametrize(
    "table, start_pos, accepted_pos, expected_len_states",
    [(test_table1, 0, [1, 3, 6], 7), (test_table2, 0, [4], 5)],
)
def test_create_fsm_machine(
    table, start_pos, accepted_pos, expected_len_states
) -> None:
    fsm = create_fs_machine(table, start_pos, accepted_pos)
    assert (
        len(fsm.states.keys()) == expected_len_states and fsm.zero_position == start_pos
    )


@pytest.mark.parametrize(
    "table, start_pos, accepted_pos, input_string, expected",
    [
        (test_table1, 0, [1, 3, 6], "ddd.ddEddddd", True),
        (test_table1, 0, [1, 3, 6], "ddd.ddE-ddddd", True),
        (test_table1, 0, [1, 3, 6], "ddd.ddE+ddddd", True),
        (test_table1, 0, [1, 3, 6], "dddE+ddddd", True),
        (test_table1, 0, [1, 3, 6], ".dddE+ddddd", False),
        (test_table1, 0, [1, 3, 6], "d.ddd+ddddd", False),
        (test_table1, 0, [1, 3, 6], "d.dddE", False),
        (test_table1, 0, [1, 3, 6], "d.ddd", True),
        (test_table1, 0, [1, 3, 6], "d", True),
        (test_table1, 0, [1, 3, 6], "d.dEd.d", False),
        (test_table2, 0, [4], "aILOVEPYTHONVERYMUCHabb", True),
        (test_table2, 0, [4], "PLEASESAVEMEFROMPYTHON", False),
        (test_table2, 0, [4], "abb", False),
        (test_table2, 0, [4], "aabb", True),
        (test_table2, 0, [4], "babb", True),
        (test_table2, 0, [4], "bbabb", True),
        (test_table2, 0, [4], "aabbabbabbbbabccbabb", True),
    ],
)
def test_validate_string(
    table, start_pos, accepted_pos, input_string, expected
) -> None:
    fsm = create_fs_machine(table, start_pos, accepted_pos)
    assert validate_string(fsm, input_string) == expected
