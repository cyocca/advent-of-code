import operator
from functools import reduce
from math import ceil
from typing import Callable

from adventofcode.utils import load_list


def get_time_to_record(parser: Callable[[str], list[str]]) -> dict[int, int]:
    data = load_list()

    times = (int(v) for v in parser(data[0].lstrip("Time:")))
    records = (int(v) for v in parser(data[1].lstrip("Distance:")))

    return dict(zip(times, records))


def get_distance(hold_time: int, total_time: int) -> int:
    # The speed of the boat is the amount of time the button is held.
    # It can travel for the remaining time.
    return hold_time * (total_time - hold_time)


def get_first_winning_hold_time(total_time: int, record: int) -> int:
    # We only have to look at the left half of the curve since it's symmetric.
    # If the record is the horizontal line, we want to find where it intersects on
    # the left.
    #        .
    #     .     .
    # ----------------
    #   .         .
    #  .           .
    #  ^^^^^^^
    lower = 0
    # Start in the middle
    upper = ceil(total_time / 2)

    # Binary search
    while lower != upper:
        hold_time = ceil((lower + upper) / 2)
        distance = get_distance(hold_time, total_time)

        # We want to make sure this is the first hold time past the record.
        # i.e. if we were to hold it one second less we wouldn't beat the record.
        if distance > record and get_distance(hold_time - 1, total_time) <= record:
            return hold_time

        if distance > record:
            upper = hold_time
        else:
            lower = hold_time

    raise ValueError("Couldn't find the right hold time")


def get_ways_to_win(total_time: int, record: int) -> int:
    first_winning_hold_time = get_first_winning_hold_time(total_time, record)

    # We want the are above the arrows.
    #        .
    #     .     .
    #   . |     | .
    #  .  |     |  .
    #  ^^^^     ^^^^
    return total_time - (first_winning_hold_time * 2) + 1


def get_multiplied_ways_to_win(parser: Callable[[str], list[str]]) -> int:
    time_to_record = get_time_to_record(parser=parser)

    return reduce(
        operator.mul,
        (get_ways_to_win(time, record) for time, record in time_to_record.items()),
    )


def part_1() -> int:
    return get_multiplied_ways_to_win(parser=lambda v: v.split())


def part_2() -> int:
    return get_multiplied_ways_to_win(parser=lambda v: [v.replace(" ", "")])


print(part_1())
print(part_2())
