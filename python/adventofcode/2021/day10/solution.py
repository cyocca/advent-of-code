# https://adventofcode.com/2021/day/10

from collections import deque
from statistics import median
from typing import Iterable, List, Union

from adventofcode.utils import load_list

lines = load_list()

opening_to_closing = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def get_closing_sequence_or_corrupted_char(line: str) -> Union[str, List[str]]:
    """
    If the line is corrupted, return the corrupted char.
    If the line is incomplete, return the completing sequence.
    """
    stack = deque()

    for char in line:
        # If this is an opening char, add it to the stack
        if char in opening_to_closing:
            stack.append(char)
            continue

        # If this is a closing char, pop the opening char from the top of the stack
        opening = stack.pop()
        # Fetch the corresponding closing char
        closing = opening_to_closing[opening]

        # The line is corrupted since the char we're looking at isn't the expected
        # closing char
        if char != closing:
            return char

    # To complete the line, find the closing char for each opening char remaining in the
    # stack
    return [opening_to_closing[c] for c in reversed(stack)]


def part_1() -> int:
    char_to_score = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    def get_score(line: str) -> int:
        result = get_closing_sequence_or_corrupted_char(line)

        # The line wasn't corrupted
        if not isinstance(result, str):
            return 0

        return char_to_score[result]

    return sum(get_score(line) for line in lines)


print(part_1())


def part_2() -> float:
    char_to_score = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    def get_score(sequence: Iterable[str]) -> int:
        score = 0

        for char in sequence:
            score *= 5
            score += char_to_score[char]

        return score

    results = (get_closing_sequence_or_corrupted_char(line) for line in lines)
    # If the line was corrupted, filter it out
    closing_sequences = (r for r in results if not isinstance(r, str))

    return median(get_score(s) for s in closing_sequences)


print(part_2())
