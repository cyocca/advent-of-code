from itertools import cycle
from pathlib import Path
from typing import Iterable, Set

from adventofcode.utils import Line, Point, load_input


def get_horizontal_line(height: int) -> Set[Point]:
    return set(Line(Point(2, height), Point(5, height)).points)


def get_cross(height: int) -> Set[Point]:
    return set(
        (
            *Line(Point(2, height + 1), Point(4, height + 1)).points,
            *Line(Point(3, height), Point(3, height + 2)).points,
        )
    )


def get_backwards_l(height: int) -> Set[Point]:
    return set(
        (
            *Line(Point(2, height), Point(4, height)).points,
            *Line(Point(4, height), Point(4, height + 2)).points,
        )
    )


def get_vertical_line(height: int) -> Set[Point]:
    return set(Line(Point(2, height), Point(2, height + 3)).points)


def get_square(height: int) -> Set[Point]:
    return set(
        (Point(2, height), Point(3, height), Point(2, height + 1), Point(3, height + 1))
    )


def move(points: Iterable[Point], x: int = 0, y: int = 0) -> Set[Point]:
    return {p.translate(x=x, y=y) for p in points}


def draw(points: Set[Point], width: int, height: int) -> str:
    grid = [["."] * width for _ in range(height)]

    for point in points:
        grid[height - point.y - 1][point.x] = "#"

    with open(Path(__file__).parent / "debug.txt", "w") as file:
        file.write("\n".join("".join(l) for l in grid))


def part_1(width: int, rock_count: int) -> int:
    all_points = set()
    jets = cycle(load_input())
    shape_factories = cycle(
        iter(
            (
                get_horizontal_line,
                get_cross,
                get_backwards_l,
                get_vertical_line,
                get_square,
            )
        )
    )
    height = 0

    for _ in range(rock_count):
        cur_points = next(shape_factories)(height + 3)
        while True:
            jet = next(jets)
            # Move according to the jet
            next_points = move(cur_points, x=-1 if jet == "<" else 1)

            if all(
                0 <= p.x < width for p in next_points
            ) and not all_points.intersection(next_points):
                cur_points = next_points

            # Move down
            next_points = move(cur_points, y=-1)

            # We couldn't move down. Add the rock's points to the settled points
            if any(p.y <= 0 for p in cur_points) or all_points.intersection(
                next_points
            ):
                all_points.update(cur_points)
                break

            # Otherwise we could move down. Just keep going
            cur_points = next_points

        height = max(height, max(p.y + 1 for p in cur_points))

    return height


print(part_1(width=7, rock_count=2022))
