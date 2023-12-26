import src.practice.practice9.fsm as fsm


INPUT_INVITE = "enter a string: "
RESULT_FLOAT_FSM = 'Result: belongs to "digit+(.digit+)?(E(+|-)?digit+)?"'
RESULT_NOTHING = "Result: does not belong to any fsm"


def maks_fsm_float() -> fsm.FSMachine:
    fsm_table = {
        0: {"d": 1},
        1: {"E": 4, "d": 1, ".": 2},
        2: {"d": 3},
        3: {"E": 4, "d": 3},
        4: {"+": 5, "-": 5, "d": 6},
        5: {"d": 6},
        6: {"d": 6},
    }
    return fsm.create_fs_machine(fsm_table, 0, [1, 3, 6])


def validate_string_float(given_fsm: fsm.FSMachine, input_string: str) -> bool:
    input_string = list(input_string)
    if "d" in input_string:
        return False
    for i in range(len(input_string)):
        if input_string[i].isdigit():
            input_string[i] = "d"
    return fsm.validate_string(given_fsm, "".join(input_string))


def main() -> None:
    fsm_float = maks_fsm_float()
    user_input = input(INPUT_INVITE)
    if validate_string_float(fsm_float, user_input):
        print(RESULT_FLOAT_FSM)
    else:
        print(RESULT_NOTHING)


if __name__ == "__main__":
    main()
