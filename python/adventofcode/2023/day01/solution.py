from typing import Callable, Final, Optional

from adventofcode.utils import load_input

DIGITS: Final = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

MatchT = Callable[[str, int, bool], Optional[str]]


def get_digit(line: str, index: int, is_reversed: bool) -> Optional[str]:
    """Return True if the char at `index` in `line` is a digit."""
    return line[index] if line[index].isdigit() else None


def get_written_digit(line: str, index: int, is_reversed: bool) -> Optional[str]:
    """Return True if a written digit starts at `index` in `line`."""
    for digit_index, digit in enumerate(DIGITS):
        adjusted_index = index
        # For example, when going backwards and starting at 't',
        # we want to compare where indicated
        #   abcone2threexyz
        #          ^
        #          -----
        if is_reversed:
            adjusted_index -= len(digit) - 1

        if digit == line[adjusted_index : adjusted_index + len(digit)]:
            return str(digit_index + 1)

    return None


def get_first_digit(line: str, match: MatchT, is_reversed: bool) -> str:
    indexes = range(len(line))

    if is_reversed:
        indexes = reversed(indexes)

    for index in indexes:
        if digit := match(line, index, is_reversed):
            return digit

    raise ValueError(f"Couldn't find first digit (reversed {is_reversed}): {line}")


def get_number(line: str, match: MatchT) -> int:
    # The general idea is that we don't want to look from only one side.
    # If we do that, we're guaranteed to go through the whole line or we won't know
    # if there's a digit later on.
    # If we get the first digit from the left and last digit from the right, worst case
    # we go through the whole line, but often we can stop early.
    first = get_first_digit(line, match, is_reversed=False)
    last = get_first_digit(line, match, is_reversed=True)

    return int(f"{first}{last}")


def sum_numbers(match: MatchT) -> int:
    return sum(get_number(l, match) for l in load_input().splitlines())


def part_1() -> int:
    return sum_numbers(get_digit)


def part_2() -> int:
    return sum_numbers(lambda *args: get_digit(*args) or get_written_digit(*args))


print(part_1())
print(part_2())
