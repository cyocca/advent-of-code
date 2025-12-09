from collections.abc import Callable
from adventofcode.utils import load_list
from dataclasses import dataclass
from typing_extensions import Self
from itertools import combinations
from functools import reduce
from operator import mul
from more_itertools import quantify

@dataclass(frozen=True)
class Point:

    x: int
    y: int
    z: int

    @classmethod
    def parse(cls, line: str) -> Self:
        return cls(*(int(v) for v in line.split(",")))

    def distance_to(self, other: Self) -> int:
        return (
            ((self.x - other.x) ** 2)
            + ((self.y - other.y) ** 2)
            + ((self.z - other.z) ** 2)
        ) ** 0.5

Circuits = list[set[Point]]
Pair = tuple[Point, Point]

def load_points() -> list[Point]:
    return load_list(parser=Point.parse)

def update_circuits(circuits: Circuits, pair: Pair) -> Circuits:
    new_circuits = []
    to_merge = []

    for circuit in circuits:
        contained_count = quantify(p in circuit for p in pair)

        # Already merged.
        if contained_count == 2:
            return circuits

        # Only one point is in this circuit, we need to keep searching for the second
        # one so we can merge them.
        if contained_count == 1:
            to_merge.append(circuit)
            continue

        # Circuit didn't contain either point, preserve it.
        new_circuits.append(circuit)

    return [
        *new_circuits,
        # Create a new set containing the circuits with a member of our pair and the
        # pair itself.
        set.union(*to_merge, set(pair))
    ]

def get_pairs_by_distance(points, connection_count: int | None) -> list[Pair]:
    pairs = combinations(points, r=2)

    # We could make this a bit more efficient by using a heap to only keep the closest
    # pairs, but it's not necessary to solve the problem in a reasonable amount of time.
    return sorted(
        pairs,
        key=lambda pair: Point.distance_to(*pair)
    )[:connection_count]


def connect(points: list[Point], *, connection_count: int, done: Callable[[Circuits], bool]) -> tuple[Circuits, Pair]:
    by_distance = get_pairs_by_distance(points, connection_count)

    # Start with the first pair as a circuit, then process the rest.
    circuits = [set(by_distance[0])]
    for pair in by_distance[1:]:
        circuits = update_circuits(circuits, pair)

        if done(circuits):
            return circuits, pair

    return circuits, pair

def part1() -> int:
    points = load_points()
    circuits, _ = connect(
        points,
        connection_count=1000,
        # We need to process all circuits.
        done=lambda _: False
    )

    largest_circuit_counts = sorted(
        (len(c) for c in circuits),
        reverse=True
    )[:3]

    return reduce(mul, largest_circuit_counts)

def part2() -> int:
    points = load_points()
    _, pair = connect(
        points,
        connection_count=None,
        # There can be multiple instances where we only have one circuit.
        # We need to make sure all points are included.
        done=lambda circuits: len(circuits) == 1 and len(circuits[0]) == len(points)
    )

    return reduce(mul, (p.x for p in pair))

print(part1())
print(part2())
