import json
from functools import cmp_to_key
from typing import List, Tuple

from more_itertools import flatten

from adventofcode.utils import load_input


def get_packet_pairs() -> List[Tuple[List, List]]:
    raw_pairs = load_input().split("\n\n")
    pairs = []

    for pair in raw_pairs:
        first, second = pair.split("\n")
        pairs.append((json.loads(first), json.loads(second)))

    return pairs


def compare_packets(first: List, second: List) -> int:
    index = 0
    while index < len(first) and index < len(second):
        # Both values are integers
        if isinstance(first[index], int) and isinstance(second[index], int):
            first_value = int(first[index])
            second_value = int(second[index])

            if first_value == second_value:
                index += 1
                continue

            return first_value - second_value

        # If both values aren't ints, we'll need to compare lists

        # Wrap the first if necessary
        first_value = first[index]
        if not isinstance(first[index], list):
            first_value = [first_value]

        # Wrap the second if necessary
        second_value = second[index]
        if not isinstance(second[index], list):
            second_value = [second_value]

        result = compare_packets(first_value, second_value)

        if result == 0:
            index += 1
            continue

        return result

    # If we got here, one or both of the lists ran out of items
    if len(first) < len(second):
        return -1

    if len(first) > len(second):
        return 1

    return 0


def part_1() -> int:
    return sum(
        index + 1
        for index, pair in enumerate(get_packet_pairs())
        if compare_packets(*pair) < 0
    )


print(part_1())


def part_2() -> int:
    first_divider_packet = [[2]]
    second_divider_packet = [[6]]

    in_order = sorted(
        [first_divider_packet, second_divider_packet, *flatten(get_packet_pairs())],
        key=cmp_to_key(compare_packets),
    )

    return (in_order.index(first_divider_packet) + 1) * (
        in_order.index(second_divider_packet) + 1
    )


print(part_2())
