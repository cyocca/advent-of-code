from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable

from adventofcode.utils import Direction, Point, get_area, load_list


@dataclass
class Instruction:

    direction: Direction
    value: int
    hex_color_code: str

    @classmethod
    def parse(cls, line: str) -> Instruction:
        direction_code, value, hex_color_code = line.split()

        if direction_code == "L":
            direction = Direction.LEFT
        elif direction_code == "R":
            direction = Direction.RIGHT
        elif direction_code == "U":
            direction = Direction.UP
        elif direction_code == "D":
            direction = Direction.DOWN
        else:
            raise ValueError(f"Unknown direction code `{direction_code}`")

        return cls(
            direction=direction,
            value=int(value),
            hex_color_code=hex_color_code.lstrip("(#").rstrip(")"),
        )

    def decode(self) -> Instruction:
        direction = {
            "0": Direction.RIGHT,
            "1": Direction.DOWN,
            "2": Direction.LEFT,
            "3": Direction.UP,
        }.get(self.hex_color_code[-1])

        return replace(
            self, direction=direction, value=int(self.hex_color_code[:5], 16)
        )


def get_instructions() -> list[Instruction]:
    return load_list(parser=Instruction.parse)


def get_next_point(current_point: Point, instruction: Instruction) -> Iterable[Point]:
    # Move the point in the direction of the instruction multiplied by its value
    return current_point.translate(
        *(instruction.value * d for d in instruction.direction.value.as_tuple()),
    )


def get_perimeter(instructions: Iterable[Instruction]) -> list[Point]:
    current_point = Point(0, 0)
    perimeter = [current_point]

    for instruction in instructions:
        next_point = get_next_point(current_point, instruction)
        perimeter.append(next_point)
        current_point = next_point

    return perimeter


def get_area_from_instructions(instructions: Iterable[Instruction]) -> int:
    perimeter = get_perimeter(instructions)
    return get_area(perimeter, include_perimeter_points=True)


def part_1() -> int:
    return get_area_from_instructions(get_instructions())


def part_2() -> int:
    return get_area_from_instructions(i.decode() for i in get_instructions())


print(part_1())
print(part_2())
