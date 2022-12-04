from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Tuple

from more_itertools import quantify

from adventofcode.utils import load_list


@dataclass
class Assignment:

    start: int
    end: int

    @classmethod
    def parse(cls, value: str) -> Assignment:
        return Assignment(*(int(x) for x in value.split("-")))

    def fully_overlaps(self, other: Assignment) -> bool:
        # Two assignments fully overlap if one is contained in the
        # other. For example
        # ...aaa....
        # ...bbbb...
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other: Assignment) -> bool:
        # Two assignments overlap if at least one section is shared.
        # For example
        # ...aaa....
        # .....bb...
        # or
        # ...aaa....
        # ..bb......
        start_contained = self.start >= other.start and self.start <= other.end
        end_contained = self.end <= other.end and self.end >= other.start

        return start_contained or end_contained


def get_assignments() -> List[Tuple[Assignment, Assignment]]:
    return [
        (Assignment.parse(left), Assignment.parse(right))
        for left, right in load_list(parser=lambda line: line.split(","))
    ]


def count_overlaps(comparison: Callable[[Assignment, Assignment], bool]) -> int:
    return quantify(
        comparison(left, right) or comparison(right, left)
        for left, right in get_assignments()
    )


def part_1() -> int:
    return count_overlaps(lambda a, b: a.fully_overlaps(b))


print(part_1())


def part_2() -> int:
    return count_overlaps(lambda a, b: a.overlaps(b))


print(part_2())
