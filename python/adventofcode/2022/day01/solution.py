from typing import List

from adventofcode.utils import load_input


def get_calories() -> List[int]:
    # Each elf is separated by two newlines
    elves = load_input().split("\n\n")
    # Sum the calories (each on a new line) that each elf is carying
    return [sum(int(c) for c in e.split("\n")) for e in elves]


def part_1() -> int:
    return max(get_calories())


def part_2() -> int:
    # Return the sum of the three largest calorie counts.
    # By default, sorting is from low to high, so reverse it.
    return sum(sorted(get_calories(), reverse=True)[0:3])


print(part_1())
print(part_2())
