from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, List, Tuple

from more_itertools import flatten

from adventofcode.utils import load_list


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


def get_lines() -> List[Line]:
    lines = []
    raw_lines = load_list()

    for line in raw_lines:
        points = line.split(" -> ")
        points = [Point(*(int(x) for x in point.split(","))) for point in points]
        # Pair the points that are next to each other into lines
        lines.extend(Line(*pair) for pair in zip(points, points[1:]))

    return lines


def get_bounds(lines: List[Line]) -> Tuple[Point, Point]:
    get_xs = lambda: flatten((l.start.x, l.end.x) for l in lines)
    min_x = min(get_xs())
    max_x = max(get_xs())
    max_y = max(flatten((l.start.y, l.end.y) for l in lines))

    # Min y is always 0
    return Point(min_x, 0), Point(max_x, max_y)


def create_structure(
    lines: List[Line], include_floor: bool = False
) -> Tuple[List[List[str]], Tuple[Point, Point]]:
    bounds = get_bounds(lines)
    top_left, bottom_right = bounds

    width = bottom_right.x - top_left.x + 1
    height = bottom_right.y - top_left.y + 1

    extra_width, extra_height = 0, 0
    if include_floor:
        extra_height = 2
        # The width can grow by the height on each side of center
        extra_width = (height + extra_height - 1) * 2

    width += extra_width
    height += extra_height

    structure = [["."] * width for _ in range(height)]
    adjusted_top_left = top_left.translate(x=-extra_width // 2)
    adjusted_bottom_right = bottom_right.translate(x=extra_width // 2)
    relative_lines = [line.relative_to(adjusted_top_left) for line in lines]

    # Create a new line at the floor from farthest left to farthest right
    if include_floor:
        relative_lines.append(Line(Point(0, height - 1), Point(width - 1, height - 1)))

    for line in relative_lines:
        for point in line.points:
            structure[point.y][point.x] = "#"

    return structure, (adjusted_top_left, adjusted_bottom_right)


# For debugging
def format(structure: List[List[str]]) -> str:
    return "\n".join("".join(l) for l in structure)


def simulate(include_floor: bool = False) -> int:
    structure, bounds = create_structure(get_lines(), include_floor=include_floor)
    top_left, bottom_right = bounds
    source = Point(500, 0).relative_to(top_left)

    def get(point: Point) -> str:
        return structure[point.y][point.x]

    sand_units = 0
    cur = source

    while True:
        down = cur.translate(y=1)
        down_left = down.translate(x=-1)
        down_right = down.translate(x=1)

        # We may have fallen off
        if not include_floor and (
            (down.y > bottom_right.y)
            or (down_left.x < 0 or down_right.x > bottom_right.x)
        ):
            return sand_units

        for move in (down, down_left, down_right):
            if get(move) == ".":
                cur = move
                break

        if cur not in (down, down_left, down_right):
            # Settle, since everything is blocked (we didn't move)
            sand_units += 1

            # If we blocked the source, we're done
            if include_floor and cur == source:
                return sand_units

            structure[cur.y][cur.x] = "o"
            cur = source


def part_1():
    return simulate(include_floor=False)


print(part_1())


def part_2():
    return simulate(include_floor=True)


print(part_2())
