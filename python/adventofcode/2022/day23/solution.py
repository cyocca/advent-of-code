from abc import ABC, abstractmethod
from collections import defaultdict, deque
from pathlib import Path
from typing import Deque, Final, Iterable, Set, Tuple

from more_itertools import collapse

from adventofcode.utils import Line, Point, load_list


def get_elves() -> Set[Point]:
    elves = set()
    lines = load_list()

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                elves.add(Point(col, row))

    return elves


class Mover(ABC):
    @staticmethod
    @abstractmethod
    def get_neighbors() -> Set[Point]:
        pass

    @staticmethod
    @abstractmethod
    def get_direction() -> Point:
        pass

    @classmethod
    def move(cls, elves: Set[Point], elf: Point) -> Point:
        if any(elf.translate(*n.as_tuple()) in elves for n in cls.get_neighbors()):
            return elf

        return elf.translate(*cls.get_direction().as_tuple())


class NorthMover(Mover):
    @staticmethod
    def get_neighbors() -> Set[Point]:
        return {DIRECTIONS["N"], DIRECTIONS["NE"], DIRECTIONS["NW"]}

    @staticmethod
    def get_direction() -> Point:
        return MOVES["N"]


class SouthMover(Mover):
    @staticmethod
    def get_neighbors() -> Set[Point]:
        return {DIRECTIONS["S"], DIRECTIONS["SE"], DIRECTIONS["SW"]}

    @staticmethod
    def get_direction() -> Point:
        return MOVES["S"]


class WestMover(Mover):
    @staticmethod
    def get_neighbors() -> Set[Point]:
        return {DIRECTIONS["W"], DIRECTIONS["NW"], DIRECTIONS["SW"]}

    @staticmethod
    def get_direction() -> Point:
        return MOVES["W"]


class EastMover(Mover):
    @staticmethod
    def get_neighbors() -> Set[Point]:
        return {DIRECTIONS["E"], DIRECTIONS["NE"], DIRECTIONS["SE"]}

    @staticmethod
    def get_direction() -> Point:
        return MOVES["E"]


MOVES: Final = {
    "N": Point(0, -1),
    "E": Point(1, 0),
    "S": Point(0, 1),
    "W": Point(-1, 0),
}

DIRECTIONS: Final = {
    **MOVES,
    "NE": Point(1, -1),  # NE
    "SE": Point(1, 1),  # SE
    "SW": Point(-1, 1),  # SW
    "NW": Point(-1, -1),  # NW
}


def get_movers() -> Deque[Mover]:
    return deque(
        [
            NorthMover,
            SouthMover,
            WestMover,
            EastMover,
        ]
    )


def get_new_position(movers: Iterable[Mover], elves: Set[Point], elf: Point) -> Point:
    for mover in movers:
        new_position = mover.move(elves, elf)
        if new_position is elf:
            continue

        return new_position

    # We couldn't move anywhere
    return elf


def get_smallest_rectangle(elves: Set[Point]) -> Tuple[Line, Line]:
    min_x = min(p.x for p in elves)
    max_x = max(p.x for p in elves)
    min_y = min(p.y for p in elves)
    max_y = max(p.y for p in elves)

    return (
        Line(Point(min_x, min_y), Point(max_x, min_y)),
        Line(Point(min_x, min_y), Point(min_x, max_y)),
    )


def tick(elves: Set[Point], movers: Deque[Mover]) -> Tuple[Set[Point], bool]:
    new_to_old = defaultdict(set)
    for elf in elves:
        # If there are no neighbors, we don't do anything
        if all(elf.translate(*n.as_tuple()) not in elves for n in DIRECTIONS.values()):
            new_to_old[elf].add(elf)
            continue

        new_to_old[get_new_position(movers, elves, elf)].add(elf)

    # If only one elf moved somewhere, keep the new spot. Otherwise, keep all of the
    # old spots, i.e. no elves that would have moved to that spot can move
    elves = set(
        collapse(
            new if len(old_positions) == 1 else old_positions
            for new, old_positions in new_to_old.items()
        )
    )
    elf_moved = any(
        len(old_positions) == 1 and new != next(iter(old_positions))
        for new, old_positions in new_to_old.items()
    )

    # Make sure the first move considered this time comes last next time
    movers.rotate(-1)
    return elves, elf_moved


def simulate(elves: Set[Point], rounds: int) -> Set[Point]:
    movers = get_movers()

    for _ in range(rounds):
        elves, _ = tick(elves, movers)

    # debug(elves)
    return elves


def simulate_until_done(elves: Set[Point]) -> int:
    rounds = 0
    movers = get_movers()
    elf_moved = True

    while elf_moved:
        rounds += 1
        elves, elf_moved = tick(elves, movers)

    return rounds


def debug(elves: Set[Point]) -> None:
    # grid = [["."] * 5 for _ in range(6)]
    grid = [["."] * 14 for _ in range(12)]

    for elf in elves:
        grid[elf.y][elf.x] = "#"

    with open(Path(__file__).parent / "debug.txt", "w") as file:
        file.write("\n".join("".join(line) for line in grid))


def get_empty_tile_count(elves: Set[Point]) -> int:
    # The area of the rectangle is its height times its width
    horizontal, vertical = get_smallest_rectangle(elves)
    total_tiles = horizontal.point_count * vertical.point_count

    # Just subtract out the number of elves we have
    return total_tiles - len(elves)


def part_1() -> int:
    return get_empty_tile_count(simulate(get_elves(), rounds=10))


print(part_1())


def part_2() -> int:
    return simulate_until_done(get_elves())


print(part_2())
