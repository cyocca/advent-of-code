from typing import Callable

from adventofcode.utils import load_list


def get_histories() -> list[list[int]]:
    return load_list(parser=lambda line: [int(v) for v in line.split()])


def get_differences(values: list[int]) -> list[int]:
    return [b - a for a, b in zip(values, values[1:])]


def get_all_differences(values: list[int]) -> int:
    differences = [values]

    # See if the last row is all zeroes
    while any(d != 0 for d in differences[-1]):
        differences.append(get_differences(differences[-1]))

    return differences


def get_prediction_right(values: list[int]) -> int:
    # To get a prediction to the right, we simply sum the last value in each row.
    return sum(diffs[-1] for diffs in get_all_differences(values))


def get_prediction_left(values: list[int]) -> int:
    current = 0

    # To get a prediction to the left, we subtract the current value from the first
    # value in the next row starting at the bottom.
    for differences in reversed(get_all_differences(values)[:-1]):
        current = differences[0] - current

    return current


def sum_predictions(predictor: Callable[[list[int]], int]) -> int:
    return sum(predictor(h) for h in get_histories())


def part_1() -> int:
    return sum_predictions(get_prediction_right)


def part_2() -> int:
    return sum_predictions(get_prediction_left)


print(part_1())
print(part_2())
