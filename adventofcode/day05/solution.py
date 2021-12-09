# https://adventofcode.com/2021/day/5

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from typing import Callable, Optional, Set, Tuple

from more_itertools import ilen

from adventofcode.utils import load_list


@dataclass(frozen=True)
class Point:

    x: int
    y: int


@dataclass
class Line:

    start: Point
    end: Point

    @property
    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    @property
    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    @property
    def is_diagonal(self) -> bool:
        return not (self.is_horizontal or self.is_vertical)

    @property
    def points(self) -> Set[Point]:
        """Return all points on this line."""

        def get_delta(first: int, second: int) -> int:
            # Return the change in x or y. Since we know the lines are horizontal,
            # vertical, or have a 45 degree slope, we'll only ever increment by 0, 1, or
            # -1
            if first < second:
                return 1

            if first > second:
                return -1

            return 0

        delta_x = get_delta(self.start.x, self.end.x)
        delta_y = get_delta(self.start.y, self.end.y)

        points = set()
        cur = self.start
        while True:
            points.add(cur)

            if cur == self.end:
                break

            cur = Point(cur.x + delta_x, cur.y + delta_y)

        return points


def parser(line: str) -> Line:
    # Turn something like `0,9 -> 5,9` int a `Point` object`
    def get_ints(part: str) -> Tuple[int, int]:
        return [int(x) for x in part.split(",")]

    parts = line.split(" -> ")

    return Line(
        Point(*get_ints(parts[0])),
        Point(*get_ints(parts[1])),
    )


lines = load_list(parser=parser)


def count_overlapping_points(
    threshold: int, line_filter: Optional[Callable[[Line], bool]] = None
) -> int:
    """
    Return the number of points where `threshold` lines overlap.

    Don't count lines where `line_filter` returns True.
    """
    all_points = defaultdict(int)

    for line in lines:
        if line_filter and line_filter(line):
            continue

        for point in line.points:
            all_points[point] += 1

    return ilen(v for v in all_points.values() if v >= threshold)


def part_1() -> int:
    return count_overlapping_points(
        threshold=2, line_filter=lambda line: line.is_diagonal
    )


print(part_1())


def part_2() -> int:
    return count_overlapping_points(threshold=2)


print(part_2())
