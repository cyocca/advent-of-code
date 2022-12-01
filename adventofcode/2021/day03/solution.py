from collections import defaultdict
from typing import Callable, Dict, Iterable, List, Tuple

from adventofcode.utils import load_list

# Convert each line into a list of 0s and 1s
numbers = load_list(parser=list)


def to_int(binary: List[str]) -> int:
    """
    Convert a list of binary digits to an integer.

    Examples:
        ["1", "0", "1"] -> 5
        ["1", "1", "0", "0"] -> 12
    """
    return int("".join(binary), 2)


def get_digit_to_numbers(
    collection: Iterable[List[str]], index: int
) -> Dict[str, List[List[str]]]:
    """
    Return a mapping from digit at `index` to numbers in `collection`.

    Example:
        get_digit_to_numbers(
            ["0", "0", "1", "0", "0"],
            ["1", "1", "1", "1", "0"],
            ["1", "0", "1", "1", "0"],
            ["1", "0", "1", "1", "1"],
            0,
        ) -> {
            "0": [["0", "0", "1", "0", "0"]],
            "1": [
                ["1", "1", "1", "1", "0"],
                ["1", "0", "1", "1", "0"],
                ["1", "0", "1", "1", "1"],
            ]
        }
    """
    digit_to_numbers = defaultdict(list)

    for number in collection:
        digit_to_numbers[number[index]].append(number)

    return digit_to_numbers


def get_gamma_and_epsilon_rate() -> Tuple[int, int]:
    digit_count = len(numbers[0])
    gamma_rate = []
    epsilon_rate = []

    for index in range(digit_count):
        digit_to_numbers = get_digit_to_numbers(numbers, index)

        # Check if there are more numbers with 1s in this position
        if len(digit_to_numbers["1"]) >= len(digit_to_numbers["0"]):
            gamma_rate.append("1")
            epsilon_rate.append("0")
        else:
            gamma_rate.append("0")
            epsilon_rate.append("1")

    return to_int(gamma_rate), to_int(epsilon_rate)


def part_1() -> int:
    gamma_rate, episolon_rate = get_gamma_and_epsilon_rate()

    return gamma_rate * episolon_rate


print(part_1())


def get_rating(one_condition: Callable[[Dict[str, List[List[str]]]], bool]) -> int:
    """
    Generic function to return a rating.

    i.e. either oxygen generator rating or co2 scrubber rating
    """
    digit_count = len(numbers[0])
    rating = numbers

    for index in range(digit_count):
        digit_to_numbers = get_digit_to_numbers(rating, index)

        # If we should keep the numbers with one in this position, narrow our collection
        # to just those numbers.
        # Ootherwise narrow to the numbers with zero in this position
        if one_condition(digit_to_numbers):
            rating = digit_to_numbers["1"]
        else:
            rating = digit_to_numbers["0"]

        # If we're down to one number, we found the solution
        if len(rating) == 1:
            return to_int(rating[0])


def get_oxygen_generator_rating() -> int:
    # The condition keeping numbers with a 1 in the current position is that there are
    # more 1s or the same number of ones
    return get_rating(
        lambda digit_to_numbers: len(digit_to_numbers["1"])
        >= len(digit_to_numbers["0"])
    )


def get_co2_scrubber_rating() -> int:
    # The condition keeping numbers with a 1 in the current position is that there are
    # less 1s
    return get_rating(
        lambda digit_to_numbers: len(digit_to_numbers["1"]) < len(digit_to_numbers["0"])
    )


def part_2() -> int:
    return get_oxygen_generator_rating() * get_co2_scrubber_rating()


print(part_2())
