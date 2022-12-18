from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, List, Set, Tuple

from more_itertools import quantify

from adventofcode.utils import load_list


@dataclass
class Volcano:

    valves: Dict[str, Valve]
    graph: Dict[str, List[Valve]]

    def get_valve(self, name: str) -> Valve:
        return self.valves[name]

    def get_neighbors(self, name: str) -> Set[Valve]:
        return self.graph[name]

    @cached_property
    def count_of_valves_with_positive_flow(self) -> int:
        return quantify(v.flow_rate > 0 for v in self.valves.values())


@dataclass
class Valve:

    name: str
    flow_rate: int


def get_volcano() -> Volcano:
    lines = load_list()
    valves = {}
    graph = defaultdict(list)

    for line in lines:
        halves = line.split(";")
        valve_parts = halves[0].split(" ")
        name = valve_parts[1]
        flow_rate = int(valve_parts[4].split("=")[1])
        # Sometimes `valve` is used instead of `valves`
        neighbors = (
            halves[1]
            .replace("valves ", "")
            .replace("valve ", "")
            .split("to ")[1]
            .split(", ")
        )

        valves[name] = (Valve(name=name, flow_rate=flow_rate), neighbors)

    for valve, neighbors in valves.values():
        graph[valve.name].extend(valves[n][0] for n in neighbors)

    return Volcano(
        valves={valve.name: valve for valve, _ in valves.values()}, graph=graph
    )


def simulate(
    volcano: Volcano,
    valves_opened: Set[str],
    minutes_remaining: int,
    pressure_released: int,
    cache: Dict[Tuple[int, str], int],
    pos: str,
) -> int:
    # If we ran out of time or we opened all the valves that have flow, we're done
    if (
        minutes_remaining <= 0
        or len(valves_opened) == volcano.count_of_valves_with_positive_flow
    ):
        return pressure_released

    # It took a minute to move here
    minutes_remaining -= 1

    # If we've been here with the same amount of time remaining and valves open, we'll
    # only continue if we're the path that has the most pressure released
    key = ("-".join(sorted(valves_opened)), minutes_remaining, pos)
    cached_result = cache.get(key, -1)
    if cached_result >= pressure_released:
        return cached_result

    def next_step(
        valves_opened: Set[str], minutes_remaining: int, pressure_released: int
    ) -> int:
        return max(
            simulate(
                volcano,
                valves_opened,
                minutes_remaining,
                pressure_released,
                cache,
                new_pos,
            )
            # Visit all of the neighbors of this valve
            for new_pos in (n.name for n in volcano.get_neighbors(pos))
        )

    # If we're at a valve that will release pressure and we haven't opened it, simulate
    # the difference between opening it and not. Sometimes, it's better to wait to open
    # it since it takes a minute to do so.
    valve = volcano.get_valve(pos)
    max_pressure_release_open = -1
    if pos not in valves_opened and valve.flow_rate > 0:
        max_pressure_release_open = next_step(
            # Make sure to include the valve we just opened
            valves_opened={*valves_opened, pos},
            # It takes a minute to open the valve
            minutes_remaining=minutes_remaining - 1,
            # Add the cumulative pressure released from this valve
            pressure_released=pressure_released + valve.flow_rate * minutes_remaining,
        )
    max_pressure_release_closed = next_step(
        # Make a copy; paths shouldn't interfere with each other
        valves_opened=set(valves_opened),
        minutes_remaining=minutes_remaining,
        pressure_released=pressure_released,
    )
    max_pressure_release = max(max_pressure_release_open, max_pressure_release_closed)
    cache[key] = max_pressure_release

    return max_pressure_release


def part_1() -> int:
    return simulate(
        volcano=get_volcano(),
        valves_opened=set(),
        minutes_remaining=30,
        pressure_released=0,
        cache={},
        pos="AA",
    )


print(part_1())
