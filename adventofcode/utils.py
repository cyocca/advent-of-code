from __future__ import annotations

import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Generator, List, Optional, TypeVar

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


@dataclass
class Point:

    x: int
    y: int

    def translate(self, x: int = 0, y: int = 0) -> Point:
        return Point(self.x + x, self.y + y)

    def relative_to(self, point: Point) -> Point:
        return Point(self.x - point.x, self.y - point.y)


@dataclass
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
