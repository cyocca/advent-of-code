# https://adventofcode.com/2021/day/13

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pprint import pprint
from typing import List, Set, Tuple

from adventofcode.utils import load_list


class Direction(Enum):

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


@dataclass
class Fold:

    position: int
    direction: Direction

    @staticmethod
    def from_line(line: str) -> Fold:
        """Parse input like `fold along y=7`."""
        line = line.replace("fold along ", "")
        axis, position = line.split("=")
        position = int(position)

        # If the axis is x, the line is horizontal, so we're folding vertically
        if axis == "x":
            return Fold(position, Direction.VERTICAL)
        elif axis == "y":
            return Fold(position, Direction.HORIZONTAL)

        raise ValueError(f"Unknown axis `{axis}`")


lines = load_list()


def get_dots_and_folds() -> Tuple[Set[Tuple[int, int]], List[Fold]]:
    # Store the dots as a set of (x, y) points
    dots: Set[Tuple[int, int]] = set()

    for index, line in enumerate(lines):
        # There's a space between the dots and the fold instructions
        if not line:
            break

        # Convert "x,y" to (x, y)
        dots.add(tuple(int(x) for x in line.split(",")))

    # Folds start one index after the blank line
    folds = [Fold.from_line(line) for line in lines[index + 1 :]]

    return dots, folds


dots, folds = get_dots_and_folds()


def fold(dots: Set[Tuple[int, int]], instruction: Fold) -> Set[Tuple[int, int]]:
    """
    Return the remaining dots after folding `dots` with `instruction`.

    Note that we will only ever lose dots, not gain them. When you fold the paper,
    either the dot doesn't overlap another and stays visible, or it overlaps another
    and now only one is visble (we lost a dot).
    """
    remaining_dots = set()

    for dot in dots:
        x, y = dot

        # If we're folding vertically, we care about the x pos
        #           |
        #   x . . . | . . . x
        #           |
        if instruction.direction is Direction.VERTICAL:
            distance_from_fold = x - instruction.position
        else:
            distance_from_fold = y - instruction.position

        # If we're on the side that isn't being folded, just keep the dot
        if distance_from_fold <= 0:
            remaining_dots.add(dot)
            continue

        # Otherwise, we need to add the new point.
        # If we're folding vertically, the y value is the same but the new x value is
        # twice the distance to the fold to the left (see picture above)
        if instruction.direction is Direction.VERTICAL:
            remaining_dots.add((x - (distance_from_fold * 2), y))
        else:
            remaining_dots.add((x, y - (distance_from_fold * 2)))

    return remaining_dots


def part_1() -> int:
    return len(fold(dots, folds[0]))


print(part_1())


def print_dots(dots: Set[Tuple[int, int]]) -> None:
    max_x = max(p[0] for p in dots)
    max_y = max(p[1] for p in dots)

    grid = [[" "] * (max_x + 1) for _ in range(max_y + 1)]
    for dot in dots:
        x, y = dot
        grid[y][x] = "#"

    # Print a grid where ' ' means empty and '#' means a dot is present
    pprint(["".join(col) for col in grid])


def part_2() -> None:
    updated = dots

    for instruction in folds:
        updated = fold(updated, instruction)

    print_dots(updated)


# We'll need to manually read the output from this to get the solution
part_2()
