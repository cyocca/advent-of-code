from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from adventofcode.utils import load_input


def get_init_sequence() -> list[str]:
    return load_input().split(",")


def hash(value: str) -> int:
    current = 0

    for char in value:
        current += ord(char)
        current *= 17
        current %= 256

    return current


def part_1() -> int:
    return sum(hash(v) for v in get_init_sequence())


@dataclass
class Box:

    index: int
    lenses: dict[str, int] = field(default_factory=dict)

    @property
    def focusing_power(self) -> int:
        return sum(
            (self.index + 1) * (lense_index + 1) * value
            for lense_index, (_, value) in enumerate(self.lenses.items())
        )


@dataclass
class Instruction(ABC):

    key: str

    @classmethod
    def parse(cls, value: str) -> Instruction:
        if "=" in value:
            parts = value.split("=")
            return InsertionInstruction(parts[0], int(parts[1]))

        if "-" in value:
            return DeletionInstruction(value[:-1])

        raise ValueError(f"Unknown instruction `{value}`")

    @abstractmethod
    def modify(self, box: Box) -> None:
        ...


@dataclass
class InsertionInstruction(Instruction):

    value: int

    def modify(self, box: Box) -> None:
        box.lenses[self.key] = self.value


class DeletionInstruction(Instruction):
    def modify(self, box: Box) -> None:
        box.lenses.pop(self.key, None)


def get_instructions() -> list[Instruction]:
    return [Instruction.parse(v) for v in load_input().split(",")]


def part_2() -> int:
    boxes = [Box(i) for i in range(256)]

    for instruction in get_instructions():
        box_index = hash(instruction.key)
        instruction.modify(boxes[box_index])

    return sum(b.focusing_power for b in boxes)


print(part_1())
print(part_2())
