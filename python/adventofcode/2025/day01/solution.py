from adventofcode.utils import load_list
from dataclasses import dataclass
from typing_extensions import Self

@dataclass
class Turn:

    left: bool
    value: int

    @property
    def right(self) -> bool:
        return not self.left

    def apply(self, dial: int) -> int:
        multiplier = -1 if self.left else 1
        return (dial + (self.value * multiplier)) % 100

    @classmethod
    def from_line(cls, line: str) -> Self:
        return cls(
            left=line[0].lower() == "l",
            value=int(line[1:])
        )


def part1() -> int:
    dial = 50
    password = 0
    turns = load_list(parser=Turn.from_line)

    for turn in turns:
        dial = turn.apply(dial)

        if dial == 0:
            password += 1

    return password

def part2() -> int:
    dial = 50
    password = 0
    turns = load_list(parser=Turn.from_line)

    for turn in turns:
        password += turn.value // 100
        remaining_turn = turn.value % 100

        # If the dial is at 0, we'll double count the pass.
        if dial != 0:
            needed_turn = dial if turn.left else 100 - dial

            if needed_turn <= remaining_turn:
                password += 1

        dial = turn.apply(dial)

    return password

print(part1())
print(part2())
