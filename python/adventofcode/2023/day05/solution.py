from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from more_itertools import chunked, flatten

from adventofcode.utils import load_input


@dataclass
class Range:

    start: int
    count: int

    @classmethod
    def from_end(cls, start: int, end: int) -> Range:
        return cls(start, end - start)

    @property
    def end(self) -> int:
        return self.start + self.count

    def with_offset(self, offset: int) -> Range:
        return Range(self.start + offset, self.count)


@dataclass
class RangeGroup:

    source: Range
    destination: Range

    @classmethod
    def parse(cls, value: str) -> RangeGroup:
        parts = [int(v) for v in value.split(" ")]

        return cls(
            source=Range(parts[1], parts[2]), destination=Range(parts[0], parts[2])
        )

    @property
    def offset(self) -> int:
        return self.destination.start - self.source.start

    def map(self, other: Range) -> tuple[list[Range], list[Range]]:
        """
        Map `other` onto this range group.

        Return mapped ranges, unmapped ranges.
        """
        # No overlap
        # self
        #           other
        if self.source.end <= other.start:
            return [], [other]

        # No overlap
        #           self
        # other
        if self.source.start >= other.end:
            return [], [other]

        # Complete overlap
        #    self
        # oootherrrrr
        if self.source.start >= other.start and self.source.end <= other.end:
            return [self.source.with_offset(self.offset)], [
                Range.from_end(other.start, self.source.start),
                Range.from_end(self.source.end, other.end),
            ]

        # Complete overlap
        # sssselffff
        #   other
        if self.source.start <= other.start and self.source.end >= other.end:
            return [other.with_offset(self.offset)], []

        # Partial overlap
        # self
        #   other
        if self.source.start < other.start and self.source.end < other.end:
            return [
                Range.from_end(other.start, self.source.end).with_offset(self.offset),
            ], [
                Range.from_end(self.source.end, other.end),
            ]

        # Partial overlap
        #    self
        # other
        if self.source.start > other.start and self.source.end > other.end:
            return [
                Range.from_end(self.source.start, other.end).with_offset(self.offset),
            ], [
                Range.from_end(other.start, self.source.start),
            ]

        raise ValueError(f"Did not handle case {self} and {other}")


@dataclass
class Map:

    source_name: str
    destination_name: str
    range_groups: list[RangeGroup]

    @classmethod
    def parse(cls, value: list[str]) -> Map:
        source_name, destination_name = value[0].rstrip(" map:").split("-to-")

        return cls(
            source_name=source_name,
            destination_name=destination_name,
            range_groups=[RangeGroup.parse(l) for l in value[1:]],
        )


def get_seed_ranges_and_maps(
    convert_seeds: Callable[[Iterable[int]], list[Range]]
) -> tuple[list[Range], dict[str, Map]]:
    blocks = load_input().split("\n\n")
    seed_ranges = convert_seeds(int(v) for v in blocks[0].lstrip("seeds: ").split())
    maps = [Map.parse(block.splitlines()) for block in blocks[1:]]
    maps = {m.source_name: m for m in maps}

    return seed_ranges, maps


def map_all(
    range_group: RangeGroup, ranges: list[Range]
) -> tuple[list[Range], list[Range]]:
    results = [range_group.map(r) for r in ranges]

    mapped = flatten(r[0] for r in results)
    unmapped = flatten(r[1] for r in results)

    return mapped, unmapped


def get_location_ranges(seed_ranges: list[Range], maps: dict[str, Map]) -> list[Range]:
    mapped, unmapped = [], seed_ranges
    map_ = maps["seed"]

    while True:
        # For each map, go through all of the ranges and try to remap our seed ranges.
        # Keep track of the ones that were successfully mapped and only try to map
        # the remaining values in the next round.
        for range_group in map_.range_groups:
            newly_mapped, unmapped = map_all(range_group, unmapped)
            mapped.extend(newly_mapped)

        # If we got through all of the maps, return all of the values.
        # Seeds that weren't mapped are just themselves.
        if map_.destination_name == "location":
            return [*mapped, *unmapped]

        # Move to the next map.
        # We'll consider all seeds unmapped again.
        map_ = maps[map_.destination_name]
        mapped, unmapped = [], [*mapped, *unmapped]


def get_lowest_location(convert_seeds: Callable[[Iterable[int]], list[Range]]) -> int:
    seed_ranges, maps = get_seed_ranges_and_maps(convert_seeds)

    return min(r.start for r in get_location_ranges(seed_ranges, maps))


def part_1() -> int:
    # In this case, we can think of each seed as a range with only one value
    return get_lowest_location(lambda seeds: [Range(s, 1) for s in seeds])


def part_2() -> int:
    # In this case, each pair of seeds is a range
    return get_lowest_location(lambda seeds: [Range(*c) for c in chunked(seeds, 2)])


print(part_1())
print(part_2())
