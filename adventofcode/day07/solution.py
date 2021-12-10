# https://adventofcode.com/2021/day/7

from statistics import median
from typing import Iterable, List

from adventofcode.utils import load_list


def parser(line: str) -> List[int]:
    return [int(x) for x in line.split(",")]


# Since there's only one line, take the first value
positions = load_list(parser=parser)[0]


def part_1() -> float:
    # By definition, the median is the middle value since the fuel cost is linear
    median_ = median(positions)

    return sum(abs(pos - median_) for pos in positions)


print(part_1())


def cost(start: int, end: int) -> float:
    """Return the cost to move from `start` to `end` in part 2."""
    n = abs(start - end)

    # The formula for the sum of natural numbers is (n² + n) / 2
    return ((n ** 2) + n) / 2


def part_2() -> float:
    # We sort the positions so that we start with a high cost at position zero that will
    # lower as we move to the right. Eventually, there will be an inflection point where
    # moving further right causes the cost to increase rather than decrease
    sorted_positions = sorted(positions)

    def get_costs(cur_pos: int) -> Iterable[float]:
        """Return the cost to move all crabs to `cur_pos`."""
        return (cost(cur_pos, p) for p in sorted_positions)

    cur_pos = 0
    cur_cost = sum(get_costs(cur_pos))

    while True:
        # Move to the right one and calculate the new cost
        cur_pos += 1
        new_cost = sum(get_costs(cur_pos))

        # At the beginning the new cost will lower. If the new cost is higher, we've
        # reached the inflection point. The cost won't get any lower from here
        if new_cost > cur_cost:
            return cur_cost

        cur_cost = new_cost


print(part_2())
