from collections import deque
from dataclasses import dataclass
from functools import partial
from operator import add, mul
from typing import Callable, Deque, List

from adventofcode.utils import load_input


@dataclass
class Monkey:

    items: Deque[int]
    operation: Callable[[int], int]
    divisible_arg: int
    true_monkey: int
    false_monkey: int

    def test(self, new_item: int) -> int:
        """Return the monkey `new_item` should go to."""
        if new_item % self.divisible_arg == 0:
            return self.true_monkey

        return self.false_monkey


def get_monkeys() -> List[Monkey]:
    raw_monkeys = load_input().split("\n\n")
    monkeys = []

    for monkey in raw_monkeys:
        # Skip the first line, since it's just the monkey number
        lines = monkey.split("\n")[1:]

        items = deque(int(x) for x in lines[0].split("items: ")[1].split(","))
        operation_parts = lines[1].split(" = ")[1].split(" ")

        if operation_parts[1] == "+":
            operator = add
        else:
            operator = mul

        if operation_parts[2] == "old":
            operation = lambda op, x: op(x, x)
            operation = partial(operation, operator)
        else:
            operation = partial(operator, int(operation_parts[2]))

        divisible_arg = int(lines[2].split("by ")[1])
        true_monkey = int(lines[3].split("monkey ")[1])
        false_monkey = int(lines[4].split("monkey ")[1])
        monkeys.append(
            Monkey(items, operation, divisible_arg, true_monkey, false_monkey)
        )

    return monkeys


def simulate(monkeys: List[Monkey], rounds: int, reduce_worry: bool) -> int:
    inspection_counts = [0] * len(monkeys)

    mod = 1
    for m in monkeys:
        mod *= m.divisible_arg

    for _ in range(rounds):
        for index, monkey in enumerate(monkeys):
            while monkey.items:
                inspection_counts[index] += 1
                item = monkey.items.popleft()
                new_item = monkey.operation(item)

                if reduce_worry:
                    new_item //= 3
                else:
                    new_item %= mod

                new_monkey = monkeys[monkey.test(new_item)]
                new_monkey.items.append(new_item)

    largest_inspection_counts = sorted(inspection_counts, reverse=True)
    return largest_inspection_counts[0] * largest_inspection_counts[1]


def part_1() -> int:
    return simulate(get_monkeys(), rounds=20, reduce_worry=True)


print(part_1())


def part_2() -> int:
    return simulate(get_monkeys(), rounds=10_000, reduce_worry=False)


print(part_2())
