from enum import Enum, IntEnum
from typing import Callable, Final, List

from adventofcode.utils import load_list


class Choice(IntEnum):

    # The value is the associated score
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):

    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"


OUTCOMES: Final = {
    Choice.ROCK: {
        Outcome.WIN: Choice.PAPER,
        Outcome.LOSE: Choice.SCISSORS,
    },
    Choice.PAPER: {
        Outcome.WIN: Choice.SCISSORS,
        Outcome.LOSE: Choice.ROCK,
    },
    Choice.SCISSORS: {
        Outcome.WIN: Choice.ROCK,
        Outcome.LOSE: Choice.PAPER,
    },
}
# Both players make the same choice in a draw
for choice in OUTCOMES:
    OUTCOMES[choice][Outcome.DRAW] = choice


def decode_choice(value: str) -> Choice:
    return {
        "A": Choice.ROCK,
        "B": Choice.PAPER,
        "C": Choice.SCISSORS,
        "X": Choice.ROCK,
        "Y": Choice.PAPER,
        "Z": Choice.SCISSORS,
    }[value]


def decode_outcome(value: str) -> Outcome:
    return {
        "X": Outcome.LOSE,
        "Y": Outcome.DRAW,
        "Z": Outcome.WIN,
    }[value]


def score_outcome(others_choice: Choice, your_choice: Choice) -> int:
    if others_choice is your_choice:
        # draw
        return 3

    if others_choice is Choice.ROCK:
        if your_choice is Choice.PAPER:
            # win
            return 6

        # lose
        return 0

    if others_choice is Choice.PAPER:
        if your_choice is Choice.SCISSORS:
            # win
            return 6

        # lose
        return 0

    # They must have chosen scissors
    if your_choice is Choice.ROCK:
        # win
        return 6

    # lose
    return 0


def get_guide() -> List[List[str]]:
    return load_list(parser=lambda line: line.split(" "))


def score(second_decoder: Callable[[str, str], Choice]) -> int:
    # `second_decoder` decodes the value in the second column
    choices = (
        (decode_choice(first), second_decoder(first, second))
        for first, second in get_guide()
    )

    return sum(
        your_choice + score_outcome(others_choice, your_choice)
        for others_choice, your_choice in choices
    )


def part_1() -> int:
    # Adapt `decode_choice` so we only need one `score` function
    def choice_decoder(_: str, your_choice: str) -> Choice:
        return decode_choice(your_choice)

    return score(choice_decoder)


print(part_1())


def chose(others_value: str, outcome: str) -> Choice:
    # Chose based on the other player and the needed outcome
    others_choice = decode_choice(others_value)
    outcome = decode_outcome(outcome)

    return OUTCOMES[others_choice][outcome]


def part_2() -> int:
    return score(chose)


print(part_2())
