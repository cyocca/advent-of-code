from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from itertools import cycle
from math import gcd
from typing import Callable, Iterable

from adventofcode.utils import load_list


@dataclass
class Node:

    name: str
    left_name: str
    right_name: str

    @classmethod
    def parse(cls, line: str) -> Node:
        name, nodes = line[:-1].split(" = (")

        return cls(name, *nodes.split(", "))

    def get_node_name(self, instruction: str) -> Node:
        if instruction == "L":
            return self.left_name

        if instruction == "R":
            return self.right_name

        raise ValueError(f"Unknown instruction `{instruction}`")


def get_instructions_and_network():
    lines = load_list()
    network = {}

    for line in lines[2:]:
        node = Node.parse(line)
        network[node.name] = node

    # Use cycle to repeat the instructions once they run out
    return cycle(lines[0]), network


def find_path_length(
    instructions: Iterable[str],
    network: dict[str, Node],
    start: Node,
    is_end: Callable[[Node], bool],
) -> int:
    current = start
    count = 0

    while not is_end(current):
        current = network[current.get_node_name(next(instructions))]
        count += 1

    return count


def part_1() -> int:
    instructions, network = get_instructions_and_network()

    return find_path_length(
        instructions,
        network,
        start=network["AAA"],
        is_end=lambda node: node.name == "ZZZ",
    )


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def part_2() -> int:
    instructions, network = get_instructions_and_network()

    path_lengths = (
        find_path_length(
            instructions,
            network,
            start=starting_node,
            is_end=lambda node: node.name.endswith("Z"),
        )
        for starting_node in (n for n in network.values() if n.name.endswith("A"))
    )

    # We can't actually traverse the paths until all the nodes end with Z because it
    # takes way too long.
    # Instead, just find the least common multiple of all of the path lengths to line
    # them up.
    return reduce(lcm, path_lengths)


print(part_1())
print(part_2())
