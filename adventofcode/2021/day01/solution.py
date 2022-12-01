# https://adventofcode.com/2021/day/1

from more_itertools import quantify

from adventofcode.utils import load_list

measurements = load_list(parser=int)


def part_1() -> int:
    # Take the measurements and create pairs one index apart, then map them to a bool
    # which is True if b is greater than a. `quantify` counts the True values
    return quantify(b > a for a, b in zip(measurements, measurements[1:]))


print(part_1())


def part_2(window_size: int) -> int:
    count = 0
    # Get the sum of the first `window_size` numbers
    cur_sum = sum(measurements[:window_size])

    # Start iterating at index `window_size`
    for index, measurement in enumerate(measurements[window_size:]):
        # Add the current measurement and subtract the one `window_size` ago.
        # For example, with
        #   [..., 100, 101, 102, 103, 104, ...]
        #              -------------
        # The current sum is 306. We subtract 100 and add 104 to get 310
        next_sum = cur_sum + measurement - measurements[index]

        if next_sum > cur_sum:
            count += 1

        cur_sum = next_sum

    return count


print(part_2(window_size=3))
