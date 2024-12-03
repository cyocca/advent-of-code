from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import IntEnum, auto
from functools import cached_property
from typing import Final

from more_itertools import quantify

from adventofcode.utils import load_list

J_SYMBOL: Final = "J"


class HandType(IntEnum):

    # Values go from low to high
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


@dataclass
class Card:

    symbol: str

    def _get_value(self) -> int:
        try:
            return int(self.symbol)
        except ValueError:
            pass

        return {"T": 10, J_SYMBOL: 11, "Q": 12, "K": 13, "A": 14}[self.symbol]

    @cached_property
    def value(self) -> int:
        return self._get_value()


class WildCard(Card):
    def _get_value(self) -> int:
        value = super()._get_value()

        # If it's a J, it's only worth 1 now
        return value if value != 11 else 1


@dataclass
class Hand:

    cards: tuple[Card, Card, Card, Card, Card]
    bid: int

    @classmethod
    def parse(cls, line: str) -> Hand:
        cards, bid = line.split()

        return cls(tuple(cls.get_card_type()(s) for s in cards), int(bid))

    @staticmethod
    def get_card_type() -> type[Card]:
        return Card

    @cached_property
    def type(self) -> HandType:
        symbol_counts = Counter(c.symbol for c in self.cards)

        if len(symbol_counts) == 1:
            return HandType.FIVE_OF_A_KIND

        if len(symbol_counts) == 2:
            if any(count == 4 for count in symbol_counts.values()):
                return HandType.FOUR_OF_A_KIND
            else:
                return HandType.FULL_HOUSE

        if any(count == 3 for count in symbol_counts.values()):
            return HandType.THREE_OF_A_KIND

        pair_count = quantify(count == 2 for count in symbol_counts.values())

        if pair_count == 2:
            return HandType.TWO_PAIR

        if pair_count == 1:
            return HandType.ONE_PAIR

        return HandType.HIGH_CARD

    @cached_property
    def values(self) -> tuple[int, int, int, int, int]:
        return tuple(c.value for c in self.cards)

    def __eq__(self, other: Hand) -> bool:
        return self.type == other.type and self.values == other.values

    def __lt__(self, other: Hand) -> bool:
        # Order first by hand type, then by symbol values
        return self.type < other.type or (
            self.type == other.type and self.values < other.values
        )


class WildHand(Hand):
    @staticmethod
    def get_card_type() -> type[Card]:
        # Make sure Js are worth 1
        return WildCard

    @cached_property
    def type(self) -> HandType:
        symbol_counts = Counter(c.symbol for c in self.cards)
        j_count = symbol_counts.pop(J_SYMBOL, 0)

        # All Js or all of one symbol
        if j_count == 5 or len(symbol_counts) == 1:
            return HandType.FIVE_OF_A_KIND

        # 4 Js or the count of a symbol plus Js is 4
        if j_count == 4 or any(
            count + j_count == 4 for count in symbol_counts.values()
        ):
            return HandType.FOUR_OF_A_KIND

        # Either we have (first check)
        #   11JJJ
        # or
        #   11122
        #   11JJ2
        if len(symbol_counts) == 1 or len(symbol_counts) == 2:
            return HandType.FULL_HOUSE

        # 3 Js or the count of a symbol plus Js is 3
        if j_count == 3 or any(
            count + j_count == 3 for count in symbol_counts.values()
        ):
            return HandType.THREE_OF_A_KIND

        pair_count = quantify(count == 2 for count in symbol_counts.values())

        # If we have two Js we can match them with any other two symbols
        if j_count == 2 or pair_count == 2:
            return HandType.TWO_PAIR

        # If we have one J we can match it with any other symbol
        if j_count == 1 or pair_count == 1:
            return HandType.ONE_PAIR

        return HandType.HIGH_CARD


def get_hands(hand_type: type[Hand]) -> list[Hand]:
    return load_list(parser=hand_type.parse)


def get_winnings(hand_type: type[Hand]) -> int:
    return sum(
        (index + 1) * hand.bid
        for index, hand in enumerate(sorted(get_hands(hand_type)))
    )


def part_1() -> int:
    return get_winnings(Hand)


def part_2() -> int:
    return get_winnings(WildHand)


print(part_1())
print(part_2())
