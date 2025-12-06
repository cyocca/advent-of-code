from adventofcode.utils import load_input
from dataclasses import dataclass, asdict
from typing_extensions import Self
from pprint import pprint
from more_itertools import quantify
from functools import total_ordering

@dataclass
@total_ordering
class Range:

    start: int
    end: int

    @classmethod
    def parse(cls, line: str) -> Self:
        start, end = line.split("-")

        return cls(int(start), int(end))

    def contains(self, value: int) -> bool:
        return self.start <= value <= self.end

    def __lt__(self, other: Self) -> int:
        if self.start < other.start:
            return True

        if self.start > other.start:
            return False

        # Start must be equal
        return self.end < other.end

    def merge(self, other: Self) -> list[Self]:
        if other.start < self.start:
            raise ValueError(f"Following ranges in incorrect order: {self}, {other}")

        # s:   #####
        # o:      ####
        if other.start <= self.end:
            return [type(self)(
                self.start,
                # Although we sorted by end, we may have a situation like this
                # 1-3
                # 1-5
                # 2-3
                # If we always used `other.end`, we'd get 1-3 rather than 1-5
                max(self.end, other.end)
            )]

        return [self, other]

    @property
    def count(self) -> int:
        return self.end - self.start + 1

@dataclass
class Cafeteria:

    fresh_ranges: list[range]
    ingredient_ids: list[int]

    @classmethod
    def parse(cls, raw_ranges: str, raw_ingredient_ids: str) -> Self:
        return cls(
            fresh_ranges=[Range.parse(r) for r in raw_ranges.split("\n")],
            ingredient_ids=[int(id_) for id_ in raw_ingredient_ids.split("\n")]
        )

    @classmethod
    def from_input(cls) -> Self:
        return cls.parse(*load_input().split("\n\n"))

    @property
    def fresh_ingredient_count(self) -> int:
        return quantify(any(r.contains(id_) for r in self.fresh_ranges) for id_ in self.ingredient_ids)

    @property
    def merged_fresh_ranges(self) -> list[Range]:
        # We need to sort so we can merge from left to right.
        # Otherwise, we would need to do a lot more work since segments that need
        # merged may not be next to each other.
        sorted_ranges = sorted(self.fresh_ranges)
        result = []
        cur = sorted_ranges[0]
        index = 1

        while index < len(sorted_ranges):
            new_ranges = cur.merge(sorted_ranges[index])

            if len(new_ranges) > 1:
                # We couldn't merge.
                # Add the left range to the result, and now consider the right range and
                # the range at the next index.
                result.append(new_ranges[0])
                cur = new_ranges[1]
            else:
                # We merged.
                # We'll consider the merged range and the range at the next index.
                cur = new_ranges[0]

            index += 1

        result.append(cur)

        return result

    @property
    def total_fresh_ingredient_count(self) -> int:
        return sum(r.count for r in self.merged_fresh_ranges)

def part1() -> int:
    return Cafeteria.from_input().fresh_ingredient_count

def part2() -> int:
    return Cafeteria.from_input().total_fresh_ingredient_count

print(part1())
print(part2())
