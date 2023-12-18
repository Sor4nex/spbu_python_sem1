import src.practice.practice9.fsm as fsm
from string import digits


INPUT_INVITE = "enter a string: "
RESULT_FLOAT_FSM = 'Result: belongs to "digit+(.digit+)?(E(+|-)?digit+)?"'
RESULT_AB_FSM = 'Result: belongs to "(a|b)*abb"'
RESULT_NOTHING = "Result: does not belong to any fsm"


def make_fsm_float() -> fsm.FSMachine:
    fsm_table = {
        0: {digits: 1},
        1: {"E": 4, digits: 1, ".": 2},
        2: {digits: 3},
        3: {"E": 4, digits: 3},
        4: {"+": 5, "-": 5, digits: 6},
        5: {digits: 6},
        6: {digits: 6},
    }
    return fsm.create_fs_machine(fsm_table, 0, [1, 3, 6])


def make_fsm_ab() -> fsm.FSMachine:
    fsm_table = {
        0: {"a": 1, "b": 1},
        1: {"a": 2, "*": 1},
        2: {"b": 3, "*": 1},
        3: {"b": 4, "*": 1},
        4: {"*": 1},
    }
    return fsm.create_fs_machine(fsm_table, 0, [4])


def main() -> None:
    all_fsm = [(make_fsm_float(), RESULT_FLOAT_FSM), (make_fsm_ab(), RESULT_AB_FSM)]
    user_input = input(INPUT_INVITE)
    for single_fsm in all_fsm:
        if fsm.validate_string(single_fsm[0], user_input):
            print(single_fsm[1])
            return None
    print(RESULT_NOTHING)


if __name__ == "__main__":
    main()
