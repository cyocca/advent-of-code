from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum

from adventofcode.utils import Point, is_valid_point, load_list


class Direction(Enum):

    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
    UP = Point(0, -1)
    DOWN = Point(0, 1)


@dataclass
class Beam:

    position: Point
    direction: Direction

    def tick(self) -> Beam:
        """Return a new beam after moving one step."""
        return Beam(
            self.position.translate(*self.direction.value.as_tuple()), self.direction
        )


class Device(ABC):
    @classmethod
    def parse(cls, value: str) -> Device:
        if value == ".":
            return EmptySpace()

        if value == "/":
            return RightAngledMirror()

        if value == "\\":
            return LeftAngledMirror()

        if value == "-":
            return HorizontalSplitter()

        if value == "|":
            return VerticalSplitter()

        raise ValueError(f"Unknown device `{value}`")

    @abstractmethod
    def process(self, beam: Beam) -> list[Beam]:
        ...


class EmptySpace(Device):
    def process(self, beam: Beam) -> list[Beam]:
        # Keep on swimming ...
        return [beam.tick()]


class RightAngledMirror(Device):
    def process(self, beam: Beam) -> list[Beam]:
        if beam.direction is Direction.LEFT:
            new_direction = Direction.DOWN
        elif beam.direction is Direction.RIGHT:
            new_direction = Direction.UP
        elif beam.direction is Direction.UP:
            new_direction = Direction.RIGHT
        elif beam.direction is Direction.DOWN:
            new_direction = Direction.LEFT
        else:
            raise ValueError(f"Unknown direction {beam.direction}")

        return [Beam(beam.position, new_direction).tick()]


class LeftAngledMirror(Device):
    def process(self, beam: Beam) -> list[Beam]:
        if beam.direction is Direction.LEFT:
            new_direction = Direction.UP
        elif beam.direction is Direction.RIGHT:
            new_direction = Direction.DOWN
        elif beam.direction is Direction.UP:
            new_direction = Direction.LEFT
        elif beam.direction is Direction.DOWN:
            new_direction = Direction.RIGHT
        else:
            raise ValueError(f"Unknown direction {beam.direction}")

        return [Beam(beam.position, new_direction).tick()]


class VerticalSplitter(Device):
    def process(self, beam: Beam) -> list[Beam]:
        if beam.direction in {Direction.UP, Direction.DOWN}:
            return EmptySpace().process(beam)

        if beam.direction in {Direction.LEFT, Direction.RIGHT}:
            return [
                Beam(beam.position, Direction.UP).tick(),
                Beam(beam.position, Direction.DOWN).tick(),
            ]

        raise ValueError(f"Unknown direction {beam.direction}")


class HorizontalSplitter(Device):
    def process(self, beam: Beam) -> list[Beam]:
        if beam.direction in {Direction.LEFT, Direction.RIGHT}:
            return EmptySpace().process(beam)

        if beam.direction in {Direction.UP, Direction.DOWN}:
            return [
                Beam(beam.position, Direction.LEFT).tick(),
                Beam(beam.position, Direction.RIGHT).tick(),
            ]

        raise ValueError(f"Unknown direction {beam.direction}")


def get_devices() -> list[list[Device]]:
    return [[Device.parse(value) for _, value in enumerate(row)] for row in load_list()]


def process_light(
    devices: list[list[Device]], starting_beam: Beam
) -> dict[Point, set[Direction]]:
    to_process = deque([starting_beam])
    seen: dict[Point, set[Direction]] = defaultdict(set)

    while to_process:
        beam = to_process.popleft()

        if (
            # We're outside of the grid
            not is_valid_point(*beam.position.as_tuple(), devices)
            # There's already a beam at this position *moving in the same direction*.
            # We can't just check that there's a beam here already, if they're moving
            # in different directions, they'll likely have different outcomes.
            or beam.direction in seen[beam.position]
        ):
            continue

        device = devices[beam.position.y][beam.position.x]

        to_process.extend(device.process(beam))
        seen[beam.position].add(beam.direction)

    return seen


def get_energized_tile_count(devices: list[list[Device]], starting_beam: Beam) -> int:
    # The number of tiles that have at least one beam moving in any direction
    return len(process_light(devices, starting_beam).values())


def part_1() -> int:
    devices = get_devices()

    return get_energized_tile_count(
        devices, starting_beam=Beam(Point(0, 0), Direction.RIGHT)
    )


def part_2() -> int:
    devices = get_devices()

    from_left = (Beam(Point(0, y), Direction.RIGHT) for y, _ in enumerate(devices))
    from_right = (Beam(Point(0, y), Direction.LEFT) for y, _ in enumerate(devices))
    from_top = (Beam(Point(x, 0), Direction.DOWN) for x, _ in enumerate(devices[0]))
    from_bottom = (Beam(Point(x, 0), Direction.UP) for x, _ in enumerate(devices[0]))

    return max(
        get_energized_tile_count(devices, starting_beam)
        for starting_beam in (*from_left, *from_right, *from_top, *from_bottom)
    )


print(part_1())
print(part_2())
