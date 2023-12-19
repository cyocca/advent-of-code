from __future__ import annotations

from dataclasses import dataclass
from functools import cache

from adventofcode.utils import load_list


@cache
def get_arrangements(
    springs: str, contiguous_group_counts: tuple[int, ...], in_dots=True
) -> int:
    index = 0

    while index != len(springs):
        spring = springs[index]
        index += 1

        if spring == "#":
            in_dots = False

            # If we don't need to match any more groups, there were too many broken
            # springs
            if not contiguous_group_counts:
                return 0

            # Otherwise, remove one from the next group
            contiguous_group_counts = (
                contiguous_group_counts[0] - 1,
                *contiguous_group_counts[1:],
            )

            # There were too many broken springs in this group
            if contiguous_group_counts[0] < 0:
                return 0

        elif spring == ".":
            # We perform the necessary steps on the first dot in a run of dots
            if in_dots:
                continue

            in_dots = True

            # If we're moving to the next group but we didn't have enough
            # broken springs, we can't match
            if contiguous_group_counts[0] != 0:
                return 0

            # We finished this group, remove it
            contiguous_group_counts = contiguous_group_counts[1:]

        elif spring == "?":
            # We need to consider replacing this question mark with a dot and with a
            # broken spring
            return get_arrangements(
                f"#{springs[index:]}",
                contiguous_group_counts,
                in_dots=in_dots,
            ) + get_arrangements(
                f".{springs[index:]}",
                contiguous_group_counts,
                in_dots=in_dots,
            )

        else:
            raise ValueError(f"Unknown char `{spring}`")

    # When we get through all of the springs, we matched if there are no groups left
    # or the only group that's left has 0 remaining broken springs.
    return (
        1
        if (
            not contiguous_group_counts
            or len(contiguous_group_counts) == 1
            and contiguous_group_counts[0] == 0
        )
        else 0
    )


@dataclass
class Row:
    springs: str
    contiguous_group_counts: tuple[int, ...]

    @classmethod
    def parse(cls, line: str) -> Row:
        springs, group_counts = line.split()

        return cls(springs, tuple(int(v) for v in group_counts.split(",")))

    def unfold(self, copies: int) -> Row:
        return type(self)(
            springs="?".join(self.springs for _ in range(copies)),
            contiguous_group_counts=self.contiguous_group_counts * copies,
        )

    def get_arrangements(self) -> int:
        return get_arrangements(self.springs, self.contiguous_group_counts)


def part_1() -> int:
    rows = load_list(parser=Row.parse)

    return sum(r.get_arrangements() for r in rows)


def part_2() -> int:
    rows = load_list(parser=Row.parse)

    return sum(r.unfold(5).get_arrangements() for r in rows)


print(part_1())
print(part_2())
