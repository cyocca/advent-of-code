from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from adventofcode.utils import load_list


@dataclass
class CubeCounts:

    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def parse(cls, value: str) -> CubeCounts:
        color_counts = value.split(", ")
        colors_and_counts = [c.split(" ") for c in color_counts]

        return cls(**{color: int(count) for count, color in colors_and_counts})

    @cached_property
    def power(self) -> int:
        return self.red * self.green * self.blue


@dataclass
class Game:

    id: int
    cube_counts: list[CubeCounts]

    @classmethod
    def parse(cls, value: str) -> Game:
        game, cube_counts = value.split(": ")
        game_id = int(game.split(" ")[1])

        return cls(game_id, [CubeCounts.parse(c) for c in cube_counts.split("; ")])

    def get_impossible_cube_counts(self, totals: CubeCounts) -> list[CubeCounts]:
        return [
            c
            for c in self.cube_counts
            if c.red > totals.red or c.green > totals.green or c.blue > totals.blue
        ]

    def get_minimum_cube_counts(self) -> CubeCounts:
        return CubeCounts(
            red=max(c.red for c in self.cube_counts),
            green=max(c.green for c in self.cube_counts),
            blue=max(c.blue for c in self.cube_counts),
        )


def get_games() -> list[Game]:
    return [Game.parse(line) for line in load_list()]


def part_1() -> int:
    totals = CubeCounts(red=12, green=13, blue=14)

    return sum(
        game.id for game in get_games() if not game.get_impossible_cube_counts(totals)
    )


def part_2() -> int:
    return sum(game.get_minimum_cube_counts().power for game in get_games())


print(part_1())
print(part_2())
