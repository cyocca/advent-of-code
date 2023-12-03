from __future__ import annotations

import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Generator, Iterator, List, Optional, Tuple, TypeVar

_T = TypeVar("_T")


def load_input(file_path: Optional[str] = None) -> str:
    # If a file path isn't provided, default to an "input.txt" file in the caller's
    # directory
    if not file_path:
        # Get the file that called this function. It will be the first one that's not
        # this file
        stack = iter(inspect.stack())
        calling_module = next(stack).filename

        while calling_module == __file__:
            calling_module = next(stack).filename

        # Get a path to the `input.txt` file in the callers parent dir
        file_path = Path(calling_module).parent.joinpath("input.txt")

    with open(file_path, "r") as file:
        return file.read().rstrip()


def load_list(
    file_path: Optional[str] = None, parser: Optional[Callable[[str], _T]] = None
) -> List[_T]:
    """
    Load a list of inputs from `file_path`.

    By default, load from the file "input.txt" in the caller's directory, since that's
    where the input is typically stored.

    If `parser` is provided, it will be called on each line of input from the file.
    """
    # No-op if a parser isn't given
    parser = parser or (lambda x: x)

    return [parser(l) for l in load_input(file_path).split("\n")]


def is_valid_point(x: int, y: int, grid: List[List]) -> bool:
    """
    Return True if (x, y) is a valid point.

    Essentially make sure it's not outside the bounds of `grid`
    """
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


@dataclass(frozen=True)
class Point:

    x: int
    y: int

    def translate(self, x: int = 0, y: int = 0) -> Point:
        return Point(self.x + x, self.y + y)

    def relative_to(self, point: Point) -> Point:
        return Point(self.x - point.x, self.y - point.y)

    def distance_to(self, other: Point) -> float:
        # https://en.wikipedia.org/wiki/Euclidean_distance
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def as_tuple(self) -> Tuple[int, int]:
        return self.x, self.y

    @property
    def neighbors(self) -> Iterator[Point]:
        directions = (
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        )

        return (self.translate(*d) for d in directions)


@dataclass(frozen=True)
class Line:

    start: Point
    end: Point

    @property
    def points(self) -> Generator[Point]:
        if self.start.x - self.end.x == 0:
            x = 0
        elif self.start.x - self.end.x < 0:
            x = 1
        else:
            x = -1

        if self.start.y - self.end.y == 0:
            y = 0
        elif self.start.y - self.end.y < 0:
            y = 1
        else:
            y = -1

        cur = self.start
        while cur != self.end:
            yield cur
            cur = cur.translate(x=x, y=y)

        yield self.end

    def relative_to(self, point: Point) -> Line:
        return Line(self.start.relative_to(point), self.end.relative_to(point))

    @property
    def slope(self) -> float:
        return (self.start.y - self.end.y) / (self.start.x - self.end.x)

    @property
    def y_intercept(self) -> float:
        # y - y1 = m(x - x1)
        # y = m(x - x1) + y1
        # Find y1
        return (self.slope * -1 * self.start.x) + self.start.y

    @property
    def vertical(self) -> bool:
        return self.start.x == self.end.x

    @property
    def horizontal(self) -> bool:
        return self.start.y == self.end.y

    @property
    def point_count(self) -> int:
        # Add one since the ends are inclusive
        return (
            abs(self.start.y - self.end.y) + 1
            if self.vertical
            else abs(self.start.x - self.end.x) + 1
        )

    def find_overlapping_point_count(self, other: Line) -> int:
        for first, second in ((self, other), (other, self)):
            # Vertical overlap
            if first.start.x == first.end.x == second.start.x == second.end.x:
                if first.start.y <= second.start.y and first.end.y >= second.end.y:
                    # The first completely overlaps the second
                    return second.point_count
                elif first.start.y <= second.start.y and first.end.y >= second.start.y:
                    return Line(second.start, first.end).point_count

            # Horizontal overlapping lines
            if first.start.y == first.end.y == second.start.y == second.end.y:
                if first.start.x <= second.start.x and first.end.x >= second.end.x:
                    # The first completely overlaps the second
                    return second.point_count
                elif first.start.x <= second.start.x and first.end.x >= second.start.x:
                    return Line(second.start, first.end).point_count

        # Not overlapping
        return 0

    def contains_point(self, point: Point) -> bool:
        # For now, keep it simple and only account for horizontal and vertical lines
        return (
            self.start.y == point.y == self.end.y
            and self.start.x <= point.x <= self.end.x
        ) or (
            self.start.x == point.x == self.end.x
            and self.start.y <= point.y <= self.end.y
        )

    def intersection(self, other: Line) -> Optional[Point]:
        # Parallel lines don't intersect
        if self.slope == other.slope:
            return None

        # https://en.wikipedia.org/w/index.php?title=Line–line_intersection&section=4
        x = (other.y_intercept - self.y_intercept) / (self.slope - other.slope)
        y = self.slope * x + self.y_intercept

        min_x = min(self.start.x, self.end.x)
        max_x = max(self.start.x, self.end.x)
        min_y = min(self.start.y, self.end.y)
        max_y = max(self.start.y, self.end.y)

        # Make sure the intersection actually occurs on either line, the equation above
        # assumes they're infinitely long
        if x < min_x or x > max_x or y < min_y or y > max_y:
            return None

        return Point(x, y)
