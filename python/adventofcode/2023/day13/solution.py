from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

from more_itertools import quantify

from adventofcode.utils import load_input


class ReflectionType(Enum):
    HORIZONTAL = "horizontal"
    VERITCAL = "vertical"


@dataclass
class Reflection:

    type: ReflectionType
    index: int

    @property
    def value(self) -> int:
        if self.type is ReflectionType.VERITCAL:
            return self.index

        if self.type is ReflectionType.HORIZONTAL:
            return 100 * self.index

        raise ValueError(f"Unknown reflection type `{self.type}`")


def get_difference_count(a: list, b: list) -> int:
    # Go value by value in both lists and count how many pairs are different
    return quantify(c != d for c, d in zip(a, b))


def is_reflection(
    grid: list[str],
    get_values: Callable[[list[str]], list[str]],
    max_value_length: int,
    index: int,
    tolerance: int,
) -> bool:
    # There's nothing on the left side of this to compare to
    if index == 0:
        return False

    # How many rows/columns should we compare in either direction?
    # If we're closer to the beginning, use the index.
    # Otherwise, use the distance to the opposite side.
    max_offset = min(index, max_value_length - index)

    # There is a reflection if the total number of differences between all of the
    # rows/columns compared equals the tolerance
    return (
        sum(
            # Start in the middle and move outward, comparing rows/columns equally
            # distant from where we started
            get_difference_count(
                get_values(grid, index - offset - 1), get_values(grid, index + offset)
            )
            for offset in range(max_offset)
        )
        == tolerance
    )


def get_row(grid: list[str], index: int) -> list[str]:
    return grid[index]


def get_horizontal_reflection(grid: list[str], tolerance: int) -> Optional[Reflection]:
    max_value_length = len(grid)

    for index in range(max_value_length):
        if is_reflection(grid, get_row, max_value_length, index, tolerance):
            return Reflection(ReflectionType.HORIZONTAL, index)

    return None


def get_column(grid: list[str], index: int) -> list[str]:
    return [row[index] for row in grid]


def get_vertical_reflection(grid: list[str], tolerance: int) -> Optional[Reflection]:
    max_value_length = len(grid[0])

    for index in range(max_value_length):
        if is_reflection(grid, get_column, max_value_length, index, tolerance):
            return Reflection(ReflectionType.VERITCAL, index)

    return None


def get_reflection(grid: list[str], tolerance: int) -> Reflection:
    return get_horizontal_reflection(grid, tolerance) or get_vertical_reflection(
        grid, tolerance
    )


def get_patterns() -> list[list[str]]:
    data = load_input()
    blocks = data.split("\n\n")

    return [b.splitlines() for b in blocks]


def summarize(tolerance: int) -> int:
    return sum(get_reflection(p, tolerance=tolerance).value for p in get_patterns())


def part_1() -> int:
    # We can't have any differences
    return summarize(tolerance=0)


def part_2() -> int:
    # We can have exactly one difference because of the smudge
    return summarize(tolerance=1)


print(part_1())
print(part_2())
