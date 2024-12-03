from dataclasses import dataclass
from functools import reduce
from typing import Iterable

from adventofcode.utils import Line, Point, is_valid_point, load_list


@dataclass(frozen=True)
class PartNumber:

    value: int
    points: tuple[Point]


@dataclass
class Schematic:

    grid: list[list[str]]

    def is_symbol(self, x: int, y: int) -> bool:
        value = self.grid[y][x]

        return not value.isdigit() and value != "."

    def is_gear_symbol(self, x: int, y: int) -> bool:
        value = self.grid[y][x]

        return value == "*"

    def is_digit(self, point: Point) -> bool:
        if not is_valid_point(point.x, point.y, self.grid):
            return False

        return self.grid[point.y][point.x].isdigit()

    def get_symbol_locations(self) -> list[Point]:
        return [
            Point(x, y)
            for y, _ in enumerate(self.grid)
            for x, _ in enumerate(self.grid[0])
            if self.is_symbol(x, y)
        ]

    def get_gear_symbol_locations(self) -> list[Point]:
        return [
            Point(x, y)
            for y, _ in enumerate(self.grid)
            for x, _ in enumerate(self.grid[0])
            if self.is_gear_symbol(x, y)
        ]

    def get_part_digit_locations(
        self, symbol_locations: Iterable[Point]
    ) -> list[Point]:
        # Look in the 8 spaces around a symbol for digits
        return [
            p
            for symbol in symbol_locations
            for p in symbol.neighbors
            if self.is_digit(p)
        ]

    def find_part_bound(self, start: Point, translation: Point) -> Point:
        # Go left or right starting at a digit until there are no digits left.
        # For example, in
        #   12345
        #      ^
        # We'll end at 1 or 5
        bound = start
        while True:
            next_ = bound.translate(x=translation.x, y=translation.y)
            if not self.is_digit(next_):
                break
            bound = next_

        return bound

    def get_part_number(self, part_digit: Point) -> PartNumber:
        start = self.find_part_bound(part_digit, Point(x=-1, y=0))
        end = self.find_part_bound(part_digit, Point(x=1, y=0))

        return PartNumber(
            value=int("".join(self.grid[part_digit.y][start.x : end.x + 1])),
            points=tuple(Line(start, end).points),
        )

    def get_part_numbers(self, symbol_locations: Iterable[Point]) -> set[PartNumber]:
        # We return a set to make sure we don't double count parts.
        # Part numbers can be repeated though, so we make sure the hash of a part
        # number includes the coordinates.
        return {
            self.get_part_number(p)
            for p in self.get_part_digit_locations(symbol_locations)
        }


def get_grid() -> list[list[str]]:
    return load_list(parser=lambda l: list(l))


def part_1() -> int:
    schematic = Schematic(get_grid())
    part_numbers = schematic.get_part_numbers(schematic.get_symbol_locations())

    return sum(p.value for p in part_numbers)


def part_2() -> int:
    schematic = Schematic(get_grid())
    gear_symbol_locations = schematic.get_gear_symbol_locations()
    possible_gears = [schematic.get_part_numbers((p,)) for p in gear_symbol_locations]
    gears = [g for g in possible_gears if len(g) == 2]

    return sum(reduce(lambda a, b: a.value * b.value, g) for g in gears)


print(part_1())
print(part_2())
