from collections.abc import Iterable
from adventofcode.utils import load_input
from dataclasses import dataclass
from typing_extensions import Self
from math import ceil

@dataclass
class Range:

    start: int
    end: int

    @classmethod
    def parse(cls, token: str) -> Self:
        return cls(*token.split("-"))

def get_numbers(length: int) -> Iterable[int]:
    if length <= 0:
        return []

    if length == 1:
       return range(10)

    start = int("9" * (length - 1)) + 1
    end = int("9" * length) + 1

    return range(start, end)

def part1() -> int:
    # General idea: Generate all valid numbers with length half of the starting point,
    # then repeat once and see if it's in the range. It would be too expensive to
    # generate the entire range and check each number.
    ranges = [Range.parse(t) for t in load_input().split(",")]
    answer = 0

    for r in ranges:
        # It's not enough to just use the start length.
        # Consider 998-1012 which has the answer 1010.
        # We don't want to waste work using the same length twice (for adjacent numbers).
        lengths = {
            l // 2
            for l in range(len(r.start), len(r.end) + 1)
        }
        for length in lengths:
            for number in get_numbers(length):
                candidate = int(f"{number}{number}")
                if int(r.start) <= candidate <= int(r.end):
                    answer += candidate

    return answer

def part2() -> int:
    ranges = [Range.parse(t) for t in load_input().split(",")]
    # Make sure there are no duplicates
    invalid = set()

    for r in ranges:
        # For repeated strings
        max_length = len(r.end) // 2
        lengths = range(1, max_length + 1)
        for length in lengths:
            # The number of repeats is the length of the string divided by the length
            # of the repeat
            all_repeats = {
                full_length // length
                for full_length in range(len(r.start), len(r.end) + 1)
            }
            # There must be at least two repeats
            all_repeats = {r for r in all_repeats if r > 1}
            for number in get_numbers(length):
                for repeats in all_repeats:
                    candidate = int(str(number) * repeats)
                    if int(r.start) <= candidate <= int(r.end):
                        invalid.add(candidate)

    return sum(invalid)

print(part1())
print(part2())
