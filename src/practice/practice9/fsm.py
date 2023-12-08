from dataclasses import dataclass
from typing import Optional


@dataclass
class State:
    transitions: dict[str:int]
    number: int


@dataclass
class FSMachine:
    states: dict[int:State]
    zero_position: int
    accepted_positions: list[int]


def create_fs_machine(
    given_states: dict[int : dict[str : Optional[int]]],
    start_pos: int,
    accepted_pos: list[int],
) -> FSMachine:
    all_states = dict()
    for single_given_state in given_states.keys():
        another_state = State(given_states[single_given_state], single_given_state)
        all_states[single_given_state] = another_state
    return FSMachine(all_states, start_pos, accepted_pos)


def validate_string(fsm: FSMachine, input_str: str) -> bool:
    current_pos = fsm.states[fsm.zero_position]
    for symbol in input_str:
        if symbol not in current_pos.transitions.keys():
            if "*" in current_pos.transitions.keys():
                current_pos = fsm.states[current_pos.transitions["*"]]
                continue
            return False
        current_pos = fsm.states[current_pos.transitions[symbol]]
    return current_pos.number in fsm.accepted_positions
