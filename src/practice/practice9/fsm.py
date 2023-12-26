from dataclasses import dataclass
from typing import Optional


@dataclass
class State:
    transitions: dict[str, int]
    is_terminal: bool = False


@dataclass
class FSMachine:
    states: dict[int, State]
    start_state_ind: int


def create_fs_machine(
    given_states: dict[int, dict[str, Optional[int]]],
    start_pos: int,
    terminal_pos: list[int],
) -> FSMachine:
    all_states = dict()
    for single_given_state in given_states.keys():
        another_state = State(
            given_states[single_given_state], single_given_state in terminal_pos
        )
        all_states[single_given_state] = another_state
    return FSMachine(all_states, start_pos)


def validate_string(fsm: FSMachine, input_str: str) -> bool:
    current_pos = fsm.states[fsm.start_state_ind]
    for symbol in input_str:
        for transposition in current_pos.transitions.keys():
            if symbol in transposition:
                current_pos = fsm.states[current_pos.transitions[transposition]]
                break
        else:
            return False
    return current_pos.is_terminal
