from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Set, Tuple

from adventofcode.utils import load_list


class Instruction(ABC):
    def __init__(self) -> None:
        self._elapsed_cycles = 0

    @staticmethod
    @abstractmethod
    def get_cycle_count() -> int:
        pass

    def tick(self) -> None:
        self._elapsed_cycles += 1

    @property
    def complete(self) -> bool:
        return self._elapsed_cycles == self.get_cycle_count()

    @abstractmethod
    def get_result(self, register: int) -> int:
        pass


class Noop(Instruction):
    @staticmethod
    def get_cycle_count() -> int:
        return 1

    def get_result(self, register: int) -> int:
        return register


class Add(Instruction):
    def __init__(self, to_add: int) -> None:
        super().__init__()
        self._to_add = to_add

    @staticmethod
    def get_cycle_count() -> int:
        return 2

    def get_result(self, register: int) -> int:
        return register + self._to_add


def get_instructions() -> List[List]:
    raw_instructions = load_list(parser=lambda line: line.split(" "))
    instructions = []

    for instruction in raw_instructions:
        if instruction[0] == "noop":
            instructions.append(Noop())
        elif instruction[0] == "addx":
            instructions.append(Add(int(instruction[1])))

    return instructions


def execute(
    instructions: List[Instruction], signal_strength_cycles: Set[int]
) -> Tuple[int, List[str]]:
    total_signal_strength = 0
    cycle = 0
    register = 1
    instructions = iter(instructions)
    instruction = next(instructions)
    pixels = []

    while True:
        if cycle in signal_strength_cycles:
            total_signal_strength += cycle * register

        if instruction.complete:
            register = instruction.get_result(register)
            try:
                instruction = next(instructions)
            except StopIteration:
                break

        pixel_index = cycle % 40
        sprite_middle_index = register % 40
        if pixel_index in (
            sprite_middle_index - 1,
            sprite_middle_index,
            sprite_middle_index + 1,
        ):
            pixel = "#"
        else:
            pixel = "."

        pixels.append(pixel)

        cycle += 1
        instruction.tick()

    return total_signal_strength, pixels


def part_1() -> int:
    return execute(
        get_instructions(), signal_strength_cycles={20, 60, 100, 140, 180, 220}
    )[0]


print(part_1())


def draw_screen(pixels: List[str], width: int, height: int) -> None:
    screen = []
    for row in range(height):
        screen.append(pixels[row * width : (row + 1) * width])

    with open(Path(__file__).parent / "screen.txt", "w") as file:
        file.write("\n".join("".join(row) for row in screen))


def part_2() -> int:
    pixels = execute(get_instructions(), signal_strength_cycles={})[1]

    draw_screen(pixels, width=40, height=6)


part_2()
