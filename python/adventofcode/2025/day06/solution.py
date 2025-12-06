from adventofcode.utils import load_input
from dataclasses import dataclass
from operator import mul, add
from collections.abc import Callable
from functools import reduce

@dataclass
class Problem:

    values: list[int]
    operator: Callable[[int, int], int]

    @property
    def solution(self) -> int:
        return reduce(self.operator, self.values)

def parse_problems() -> list[Problem]:
    lines = load_input().splitlines()
    # Operators are on the last line.
    # We can simply split by any whitespace (the default).
    rows = [l.split() for l in lines[:-1]]
    operators = lines[-1].split()

    return [
        Problem(
            # For each row, get the value in the current column.
            [int(row[col]) for row in rows],
            mul if operators[col] == "*" else add
        )
        # Go through each column
        for col in range(len(rows[0]))
    ]

def get_values(column: list[str]) -> list[int]:
    max_length = max(len(v) for v in column)

    # Go from left to right, getting the digit at the index.
    # If there isn't one, that works out fine since we essentially parse a number with
    # whitespace at the beginning, e.g. '   5'.
    # These come out backwards, but the operators are commutative.
    return [
        int(''.join(
            # Go from top to bottom, i.e. 123, 45, 6 in
            # 123
            # 45
            # 6
            # *
            # When we get to the end of the input, our line might not be long enough
            # for the max length, so make sure to check the index.
            value[i] if i < len(value) else ''
            for value in column
        ))
        for i in range(max_length)
    ]

def parse_column(start: int, end: int | None, all_values: list[list[str]]) -> list[str]:
    return [values[start:end] for values in all_values]

def parse_cephalopod_problems() -> list[Problem]:
    lines = load_input().splitlines()
    rows = lines[:-1]
    operators = lines[-1]

    # Find where each operator starts, this is also where the column starts.
    starting_indexes = [i for i, operator in enumerate(operators) if operator != ' ']

    return [
        Problem(
            get_values(parse_column(
                start,
                # The end of a column is the position right before the next operator.
                starting_indexes[index + 1] - 1
                # For the last column, we don't have a next operator.
                if index + 1 < len(starting_indexes)
                else None,
                rows
            )),
            mul if operators[start] == "*" else add
        )
        for index, start in enumerate(starting_indexes)
    ]

def part1() -> int:
    return sum(p.solution for p in parse_problems())

def part2() -> int:
    return sum(p.solution for p in parse_cephalopod_problems())


print(part1())
print(part2())
