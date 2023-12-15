from typing import Optional
from dataclasses import dataclass


@dataclass
class Node:
    name: str
    children: Optional[list["Node"]] = None


def parse_tokens(tokens: list[str]) -> Node:
    def _nonterminal_start(
        tokens: list[str], curr_token_index: int
    ) -> tuple[Node, int]:
        first_child, curr_token_index = _nonterminal_t(tokens, curr_token_index)
        second_child, curr_token_index = _nonterminal_sum(tokens, curr_token_index)
        return Node("START", [first_child, second_child]), curr_token_index

    def _nonterminal_sum(tokens: list[str], curr_token_index: int) -> tuple[Node, int]:
        try:
            first_child, new_curr_token_index = _terminal("+", tokens, curr_token_index)
            second_child, new_curr_token_index = _nonterminal_t(
                tokens, new_curr_token_index
            )
            third_child, new_curr_token_index = _nonterminal_sum(
                tokens, new_curr_token_index
            )
            return (
                Node("SUM", [first_child, second_child, third_child]),
                new_curr_token_index,
            )
        except (TypeError, IndexError):
            return Node("SUM", [Node("eps")]), curr_token_index

    def _nonterminal_t(tokens: list[str], curr_token_index: int) -> tuple[Node, int]:
        first_child, curr_token_index = _nonterminal_token(tokens, curr_token_index)
        second_child, curr_token_index = _nonterminal_prod(tokens, curr_token_index)
        return Node("T", [first_child, second_child]), curr_token_index

    def _nonterminal_prod(tokens: list[str], curr_token_index: int) -> tuple[Node, int]:
        try:
            first_child, new_curr_token_index = _terminal("*", tokens, curr_token_index)
            second_child, new_curr_token_index = _nonterminal_token(
                tokens, new_curr_token_index
            )
            third_child, new_curr_token_index = _nonterminal_prod(
                tokens, new_curr_token_index
            )
            return (
                Node("PROD", [first_child, second_child, third_child]),
                new_curr_token_index,
            )
        except (TypeError, IndexError):
            return Node("PROD", [Node("eps")]), curr_token_index

    def _nonterminal_token(
        tokens: list[str], curr_token_index: int
    ) -> tuple[Node, int]:
        try:
            first_child, new_curr_token_index = _terminal("(", tokens, curr_token_index)
            second_child, new_curr_token_index = _nonterminal_start(
                tokens, new_curr_token_index
            )
            third_child, new_curr_token_index = _terminal(
                ")", tokens, new_curr_token_index
            )
            return (
                Node("TOKEN", [first_child, second_child, third_child]),
                new_curr_token_index,
            )
        except (TypeError, IndexError):
            first_child, new_curr_token_index = _terminal(
                "id", tokens, curr_token_index
            )
            return Node("TOKEN", [first_child]), new_curr_token_index

    def _terminal(
        needed_terminal: str, tokens: list[str], curr_token_index: int
    ) -> tuple[Node, int]:
        if needed_terminal == tokens[curr_token_index]:
            return Node(needed_terminal), curr_token_index + 1
        elif (needed_terminal == "id") and tokens[curr_token_index].isdigit():
            return Node(f"id({tokens[curr_token_index]})"), curr_token_index + 1
        raise TypeError(
            f"wrong terminal: {needed_terminal} expected, {tokens[curr_token_index]} was given"
        )

    result, result_token_index = _nonterminal_start(tokens, 0)
    if result_token_index != len(tokens):
        raise TypeError
    return result


def pretty_print(parse_tree_root: Node) -> None:
    def _print_recursively(parse_tree_node: Node, depth: int) -> None:
        print("." * depth, parse_tree_node.name)
        if parse_tree_node.children is None:
            return
        for child in parse_tree_node.children:
            _print_recursively(child, depth + 4)

    _print_recursively(parse_tree_root, 0)
