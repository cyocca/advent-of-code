# https://adventofcode.com/2021/day/6

from typing import List

from adventofcode.utils import load_list


def parser(line: str) -> List[int]:
    return [int(x) for x in line.split(",")]


# Since there's only one line, take the first value
fish = load_list(parser=parser)[0]


def simulate(days: int) -> int:
    # Each index is the number of days left (0-8), the value at that index is the number
    # of fish with that count
    counts = [0] * 9

    # Initial population, count the number of fish for each number of remaining days
    # from  0 to 8
    for count in fish:
        counts[count] += 1

    # For each day...
    for _ in range(days):
        # Keep track of the number of fish that will produce a new fish
        zero_count = counts[0]

        # Shift each fish count down by one, essentially subtracting one day from each
        # fish
        for index in range(8):
            counts[index] = counts[index + 1]

        # Add the number of fish that had zero days to the number of fish that have 6
        # days, since counters reset to 6 after producing a new fish
        counts[6] += zero_count
        # The number of fish with 8 days left is the same as the number of fish that
        # previously had zero days left
        counts[8] = zero_count

    # Count all of the fish (i.e. the sum of the fish at each day count)
    return sum(counts)


def part_1() -> int:
    return simulate(80)


print(part_1())


def part_2() -> int:
    return simulate(256)


print(part_2())
