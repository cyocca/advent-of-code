from abc import ABC, abstractmethod
from dataclasses import dataclass
from operator import add, floordiv, mul, sub
from typing import Dict, Final

from adventofcode.utils import load_list


class Monkey(ABC):
    @abstractmethod
    def get_value(self) -> int:
        pass


@dataclass
class ValueMonkey(Monkey):

    value: int

    def get_value(self) -> int:
        return self.value


OPERATORS: Final = {"+": add, "-": sub, "*": mul, "/": floordiv}
OPPOSITE_OPERATORS: Final = {"-": add, "+": sub, "/": mul, "*": floordiv}


@dataclass
class CalculationMonkey(Monkey):

    left: Monkey
    operation: str
    right: Monkey

    def get_value(self) -> int:
        return OPERATORS[self.operation](self.left.get_value(), self.right.get_value())


def get_root(raise_for_human: bool) -> Dict[str, Monkey]:
    monkeys = {}
    lines = load_list()

    for line in lines:
        parts = line.split(": ")
        monkey_id = parts[0]

        try:
            monkey = ValueMonkey(int(parts[1]))
        except ValueError:
            monkey = CalculationMonkey(*parts[1].split(" "))

        monkeys[monkey_id] = monkey

        if monkey_id == "humn" and raise_for_human:

            def raise_ex() -> None:
                raise ValueError("Can't calculate human value")

            monkey.get_value = raise_ex

    for monkey in monkeys.values():
        if isinstance(monkey, ValueMonkey):
            continue

        # Replace the ID with the actual object
        monkey.left = monkeys[monkey.left]
        monkey.right = monkeys[monkey.right]

    return monkeys["root"]


def part_1() -> int:
    return get_root(raise_for_human=False).get_value()


print(part_1())


def part_2() -> int:
    cur = get_root(raise_for_human=True)

    # We'll start at the root of the tree and make our way down. Start by calculating
    # the value on the left or right. If we get an exception, we know the human was on
    # that side, so we need to go that way.
    try:
        result = cur.right.get_value()
        cur = cur.left
    except ValueError:
        result = cur.left.get_value()
        cur = cur.right

    # Loop until we get to the human
    while not isinstance(cur, ValueMonkey):
        try:
            value = cur.right.get_value()
            operation = cur.operation
            cur = cur.left
        except ValueError:
            value = cur.left.get_value()
            operation = cur.operation
            cur = cur.right

        if value > result and operation in ("-", "/"):
            # If our value is larger than our result and we're doing a reduction
            # operation, we should use the same operator but swap our args. Consider
            # result = 563
            #      -
            # 4000   x
            # Which should give us 3437
            result = OPERATORS[operation](value, result)
        else:
            # Typically, we need to use the opposite operation. Consider
            # result=301
            #   -
            # x   3
            # Which should give us 298
            result = OPPOSITE_OPERATORS[operation](result, value)

    return result


print(part_2())
