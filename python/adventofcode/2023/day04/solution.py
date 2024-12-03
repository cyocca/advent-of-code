from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from adventofcode.utils import load_list


@dataclass
class ScratchCard:

    winning: set[int]
    yours: set[int]

    @staticmethod
    def _parse_numbers(value: str) -> set[int]:
        return {int(n) for n in value.split()}

    @classmethod
    def parse(cls, value: str) -> ScratchCard:
        numbers = value.split(": ")[1]
        winning, yours = numbers.split(" | ")

        return ScratchCard(cls._parse_numbers(winning), cls._parse_numbers(yours))

    @cached_property
    def matching_numbers(self) -> set[int]:
        return self.winning & self.yours

    @cached_property
    def score(self) -> int:
        if matching_numbers := self.matching_numbers:
            return 2 ** (len(matching_numbers) - 1)

        return 0


def get_scratch_cards() -> list[ScratchCard]:
    lines = load_list()
    return [ScratchCard.parse(l) for l in lines]


def part_1() -> int:
    return sum(c.score for c in get_scratch_cards())


def update_copies(scratch_card: ScratchCard, copies: list[int], index: int) -> None:
    current_copies = copies[index]
    for _ in range(len(scratch_card.matching_numbers)):
        index += 1
        if index >= len(copies):
            break
        copies[index] += current_copies


def part_2() -> int:
    # It would take way too long to actually generate and process the copies.
    # Instead, just count how many we would have.
    # Start with one copy of each.
    # Add the number of copies the current scratch card has to each of the next
    # scratch cards in the range of matching numbers.
    scratch_cards = get_scratch_cards()
    copies = [1] * len(scratch_cards)
    for index in range(len(copies)):
        update_copies(scratch_cards[index], copies, index)

    return sum(copies)


print(part_1())
print(part_2())
