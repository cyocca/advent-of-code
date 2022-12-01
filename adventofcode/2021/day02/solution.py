from __future__ import annotations

from dataclasses import dataclass

from adventofcode.utils import load_list


@dataclass
class Instruction:

    direction: str
    magnitude: int

    @staticmethod
    def from_line(line: str) -> Instruction:
        parts = line.split(" ")

        # `split` should produce (direction, magnitude)
        # We need magnitude to be an int
        return Instruction(parts[0], int(parts[1]))


instructions = load_list(parser=Instruction.from_line)


def part_1() -> int:
    horizontal = 0
    depth = 0

    for instruction in instructions:
        if instruction.direction == "forward":
            horizontal += instruction.magnitude
        elif instruction.direction == "down":
            depth += instruction.magnitude
        elif instruction.direction == "up":
            depth -= instruction.magnitude
        else:
            raise ValueError(f"Unknown direction `{instruction.direction}`")

    return horizontal * depth


print(part_1())


def part_2() -> int:
    horizontal = 0
    depth = 0
    aim = 0

    for instruction in instructions:
        if instruction.direction == "forward":
            horizontal += instruction.magnitude
            depth += aim * instruction.magnitude
        elif instruction.direction == "down":
            aim += instruction.magnitude
        elif instruction.direction == "up":
            aim -= instruction.magnitude
        else:
            raise ValueError(f"Unknown direction `{instruction.direction}`")

    return horizontal * depth


print(part_2())
